import logging
import sys

import requests
from django.core import management
from django.db import transaction
from django.utils import dateparse

from contributors.models import (
    CommitStats,
    Contribution,
    ContributionLabel,
    Contributor,
    IssueInfo,
    Label,
    Organization,
    Repository,
)
from contributors.utils import github_lib as github
from contributors.utils import misc

# Simultaneous logging to file and stdout
logger = logging.getLogger("GitHub")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


ORGANIZATIONS = Organization.objects.filter(is_tracked=True)
IGNORED_REPOSITORIES = tuple(
    repo.name for repo in Repository.objects.filter(is_tracked=False)
)
IGNORED_CONTRIBUTORS = tuple(
    contrib.login for contrib in Contributor.objects.filter(is_tracked=False)
)
session = requests.Session()


@transaction.atomic
def create_contributions(
    repo, contrib_data, user_field="user", id_field="id", type_="iss"
):  # noqa: C901
    """
    Создает записи о контрибуциях в базе данных.
    """
    contributors = {}
    contributions = []
    issue_infos = []
    commit_stats = []
    contribution_labels = []

    for contrib in contrib_data:
        logger.info(contrib)
        contributor = None
        if _is_valid_contributor(contrib, user_field):
            login = contrib[user_field]["login"]
            if login not in contributors:
                contributor, _ = Contributor.objects.get_or_create(login=login)
                contributors[login] = contributor
            else:
                contributor = contributors[login]

        if contributor:
            contribution = _create_contribution(
                repo, contrib, contributor, id_field, type_
            )
            contributions.append(contribution)

            if type_ == "cit":
                commit_stats.append(
                    _create_commit_stats(repo, contribution, contrib, id_field)
                )
            elif type_ in {"pr", "iss"}:
                issue_infos.append(
                    _create_issue_info(repo, contribution, contrib, type_)
                )
                contribution_labels.extend(_create_contribution_labels(contrib))

    _bulk_create_records(contributions, commit_stats, issue_infos, contribution_labels)
    _link_labels_to_contributions(contributions, contrib_data)


def _is_valid_contributor(contrib, user_field):
    """Проверяет, является ли контрибуция допустимой для обработки."""
    contrib_author = contrib[user_field]
    return (
        contrib_author is not None
        and contrib_author["type"] != "Bot"
        and contrib_author["login"] not in IGNORED_CONTRIBUTORS
    )


def _create_contribution(repo, contrib, contributor, id_field, type_):
    """Создает объект Contribution."""
    true_type = "pr" if (type_ == "iss" and "pull_request" in contrib) else type_
    datetime = (
        contrib["commit"]["author"]["date"]
        if true_type == "cit"
        else contrib["created_at"]
    )

    return Contribution(
        id=contrib[id_field],
        repository=repo,
        contributor=contributor,
        type=true_type,
        html_url=contrib["html_url"],
        created_at=dateparse.parse_datetime(datetime),
    )


def _create_commit_stats(repo, contribution, contrib, id_field):
    """Создает объект CommitStats для коммита."""
    commit_data = github.get_commit_data(
        repo.organization or repo.owner, repo, contrib[id_field], session
    )
    return CommitStats(
        commit=contribution,
        additions=commit_data["stats"]["additions"],
        deletions=commit_data["stats"]["deletions"],
    )


def _create_issue_info(repo, contribution, contrib, type_):
    """Создает объект IssueInfo для issue или pull request."""
    state = (
        "merged"
        if type_ == "pr"
        and github.is_pr_merged(
            repo.organization or repo.owner, repo, contrib["number"], session
        )
        else contrib["state"]
    )

    return IssueInfo(
        issue=contribution,
        title=contrib["title"],
        state=state,
    )


def _create_contribution_labels(contrib):
    """Создает объекты ContributionLabel для вклада."""
    return [ContributionLabel(name=label["name"]) for label in contrib["labels"]]


def _bulk_create_records(contributions, commit_stats, issue_infos, contribution_labels):
    """Выполняет массовое создание записей в базе данных."""
    Contribution.objects.bulk_create(contributions, ignore_conflicts=True)
    CommitStats.objects.bulk_create(commit_stats, ignore_conflicts=True)
    IssueInfo.objects.bulk_create(issue_infos, ignore_conflicts=True)
    ContributionLabel.objects.bulk_create(contribution_labels, ignore_conflicts=True)


@transaction.atomic
def _link_labels_to_contributions(contributions, contrib_data):
    """Связывает метки с контрибуциями."""
    all_label_names = set(label["name"] for c in contrib_data for label in c["labels"])
    existing_labels = {
        label.name: label for label in Label.objects.filter(name__in=all_label_names)
    }
    new_labels = [
        Label(name=name) for name in all_label_names if name not in existing_labels
    ]
    Label.objects.bulk_create(new_labels, ignore_conflicts=True)

    all_labels = existing_labels.copy()
    all_labels.update({label.name: label for label in new_labels})

    ContributionLabel = Contribution.labels.through
    contribution_labels = []

    for contribution, labels in zip(contributions, [c["labels"] for c in contrib_data]):
        contribution_labels.extend(
            [
                ContributionLabel(
                    contribution_id=contribution.id,
                    label_id=all_labels[label["name"]].id,
                )
                for label in labels
            ]
        )

    # Удаляем существующие связи
    ContributionLabel.objects.filter(contribution__in=contributions).delete()

    # Создаем новые связи
    ContributionLabel.objects.bulk_create(contribution_labels, ignore_conflicts=True)


class Command(management.base.BaseCommand):
    """Команда управления для синхронизации с GitHub."""

    help = "Сохраняет данные из GitHub в базу данных"

    def add_arguments(self, parser):
        """Добавляет аргументы для команды."""
        parser.add_argument(
            "owner",
            nargs="*",
            default=ORGANIZATIONS,
            help="список имен владельцев",
        )
        parser.add_argument(
            "--repo",
            nargs="*",
            help="список полных имен репозиториев",
        )

    def handle(self, *args, **options):
        """Собирает данные из GitHub."""
        logger.info("Начало сбора данных")

        try:
            data_of_owners_and_repos = self._get_data_of_owners_and_repos(options)
            self._process_owners_and_repos(data_of_owners_and_repos)
        except Exception as e:
            logger.error(f"Произошла ошибка при сборе данных: {str(e)}")
        finally:
            session.close()

        logger.info(
            self.style.SUCCESS(
                "Данные получены из GitHub и сохранены в базу данных",
            )
        )

    def _get_data_of_owners_and_repos(self, options):
        """Получает данные о владельцах и репозиториях."""
        if options["repo"]:
            return github.get_data_of_owners_and_repos(
                repo_full_names=options["repo"],
            )
        elif options["owner"]:
            return github.get_data_of_owners_and_repos(
                owner_names=options["owner"],
            )
        else:
            raise management.base.CommandError(
                "Укажите список владельцев или репозиториев",
            )

    def _process_owners_and_repos(self, data_of_owners_and_repos):
        """Обрабатывает данные о владельцах и репозиториях."""
        for owner_data in data_of_owners_and_repos.values():
            owner = self._process_owner(owner_data)
            if isinstance(owner, Organization):
                self._process_organization_repos(owner, owner_data)
            else:
                self._process_user_repos(owner)

    def _process_owner(self, owner_data):
        """Обрабатывает данные о владельце."""
        owner_type = owner_data["details"]["type"]
        table = Contributor if owner_type == "User" else Organization
        owner, _ = misc.update_or_create_record(table, owner_data["details"])
        logger.info(f"Обработка {owner_type}: {owner}")
        return owner

    def _process_organization_repos(self, organization, org_data):
        """Обрабатывает репозитории организации."""
        repos_data = org_data.get("repos", [])
        number_of_repos = len(repos_data)
        for i, repo_data in enumerate(repos_data, start=1):
            self._process_repo(organization, repo_data, i, number_of_repos)

    def _process_user_repos(self, user):
        """Обрабатывает репозитории пользователя."""
        repos_to_process = self._get_repos_to_process(user)
        number_of_repos = len(repos_to_process)
        for i, repo_data in enumerate(repos_to_process, start=1):
            self._process_repo(user, repo_data, i, number_of_repos)

    def _get_repos_to_process(self, owner):
        """Получает список репозиториев для обработки."""
        return (
            Repository.objects.filter(owner=owner)
            .exclude(name__in=IGNORED_REPOSITORIES)
            .select_related("owner")
            .prefetch_related("labels")
        )

    def _process_repo(self, owner, repo_data, i, number_of_repos):
        """Обрабатывает отдельный репозиторий."""
        repo, _ = misc.update_or_create_record(Repository, repo_data)
        logger.info(f"Обработка репозитория: {repo} ({i}/{number_of_repos})")
        if repo_data["size"] == 0:
            logger.info("Пустой репозиторий, пропускаем")
            return

        self._process_repo_language(repo, repo_data)
        self._process_repo_contributions(owner, repo)

    def _process_repo_language(self, repo, repo_data):
        """Обрабатывает язык репозитория."""
        language = repo_data["language"]
        if language:
            label, _ = Label.objects.get_or_create(name=language)
            repo.labels.add(label)

    def _process_repo_contributions(self, owner, repo):
        """Обрабатывает вклады в репозиторий."""
        extra_info = {"owner": owner, "repo": repo}
        self._process_issues_and_prs(owner, repo, extra_info)
        self._process_commits(owner, repo, extra_info)
        self._process_comments(owner, repo, extra_info)

    def _process_issues_and_prs(self, owner, repo, extra_info):
        """Обрабатывает issues и pull requests."""
        logger.info("Обработка issues и pull requests")
        try:
            contrib_data = github.get_repo_issues(owner, repo, session)
            logger.info(contrib_data)
        except Exception as e:
            logger.error(
                extra=extra_info | {"ex": str(e)},
                msg="Не удалось обработать issues и pull requests",
            )
            return
        create_contributions(
            repo,
            contrib_data,
            user_field="user",
            id_field="id",
            type_="iss",
        )

    def _process_commits(self, owner, repo, extra_info):
        """Обрабатывает коммиты."""
        logger.info("Обработка коммитов")
        try:
            contrib_data = github.get_repo_commits_except_merges(
                owner,
                repo,
                session=session,
            )
        except Exception as e:
            logger.error(
                msg="Не удалось обработать коммиты",
                extra=extra_info | {"ex": str(e)},
            )
            return
        create_contributions(
            repo,
            contrib_data,
            user_field="author",
            id_field="sha",
            type_="cit",
        )

    def _process_comments(self, owner, repo, extra_info):
        """Обрабатывает комментарии."""
        logger.info("Обработка комментариев")
        try:
            contrib_data = github.get_all_types_of_comments(owner, repo, session)
        except Exception as e:
            logger.error(
                msg="Не удалось обработать комментарии",
                extra=extra_info | {"ex": str(e)},
            )
            return
        create_contributions(
            repo,
            contrib_data,
            user_field="user",
            id_field="id",
            type_="cnt",
        )
