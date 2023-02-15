import logging
import sys

import requests
from django.core import management
from django.utils import dateparse

from contributors.models import (
    CommitStats,
    Contribution,
    Contributor,
    IssueInfo,
    ContributionLabel,
    Label,
    Organization,
    Repository,
)
from contributors.utils import github_lib as github
from contributors.utils import misc

# Simultaneous logging to file and stdout
logger = logging.getLogger('GitHub')
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


def create_contributions(   # noqa: C901,WPS231,WPS210
    repo, contrib_data, user_field=None, id_field=None, type_=None,
):
    """Create a contribution record."""
    for contrib in contrib_data:
        contrib_author = contrib[user_field]
        if contrib_author is None or contrib_author['type'] == 'Bot':
            continue
        contrib_author_login = contrib_author['login']
        if contrib_author_login in IGNORED_CONTRIBUTORS:
            continue

        type_ = 'pr' if type_ == 'iss' and 'pull_request' in contrib else type_

        if type_ == 'cit':
            datetime = contrib['commit']['author']['date']
        else:
            datetime = contrib['created_at']

        contribution, created = Contribution.objects.get_or_create(
            id=contrib[id_field],
            defaults={
                'repository': repo,
                'contributor': misc.update_or_create_record(
                    Contributor, misc.get_contributor_data(
                        contrib_author_login, session,
                    ),
                )[0],
                'type': type_,
                'html_url': contrib['html_url'],
                'created_at': dateparse.parse_datetime(datetime),
            },
        )
        if created and type_ == 'cit':
            commit_data = github.get_commit_data(
                repo.organization or repo.owner,
                repo,
                contribution.id,
                session,
            )
            commit_stats = commit_data['stats']
            CommitStats.objects.create(
                commit=contribution,
                additions=commit_stats['additions'],
                deletions=commit_stats['deletions'],
            )

        if type_ in {'pr', 'iss'}:
            state = 'merged' if type_ == 'pr' and github.is_pr_merged(
                repo.organization or repo.owner,
                repo,
                contrib['number'],
                session,
            ) else contrib['state']

            for label in contrib['labels']:
                label_name, _ = ContributionLabel.objects.get_or_create(name=label["name"])
                contribution.labels.add(label_name)

            IssueInfo.objects.update_or_create(
                issue=contribution,
                defaults={
                    'title': contrib['title'],
                    'state': state,
                },
            )


class Command(management.base.BaseCommand):
    """A management command for syncing with GitHub."""

    help = "Saves data from GitHub to database"  # noqa: WPS125

    def add_arguments(self, parser):
        """Add arguments for the command."""
        parser.add_argument(
            'owner',
            nargs='*',
            default=ORGANIZATIONS,
            help='a list of owner names',
        )
        parser.add_argument(
            '--repo', nargs='*', help='a list of repository full names',
        )

    def handle(  # noqa: C901,WPS110,WPS213,WPS231,WPS210
        self, *args, **options,
    ):
        """Collect data from GitHub."""
        logger.info("Data collection started")

        if options['repo']:
            data_of_owners_and_repos = github.get_data_of_owners_and_repos(
                repo_full_names=options['repo'],
            )
        elif options['owner']:
            data_of_owners_and_repos = github.get_data_of_owners_and_repos(
                owner_names=options['owner'],
            )
        else:
            raise management.base.CommandError(
                "Provide a list of owners or repositories",
            )

        for owner_data in data_of_owners_and_repos.values():
            table = (
                Contributor
                if owner_data['details']['type'] == 'User'
                else Organization
            )
            owner, _ = misc.update_or_create_record(
                table, owner_data['details'],
            )
            logger.info(owner)

            repos_to_process = [
                repo for repo in owner_data['repos']
                if repo['name'] not in IGNORED_REPOSITORIES
            ]
            number_of_repos = len(repos_to_process)
            for i, repo_data in enumerate(repos_to_process, start=1):  # noqa: WPS111,E501
                repo, _ = misc.update_or_create_record(Repository, repo_data)
                logger.info(f"{repo} ({i}/{number_of_repos})")
                if repo_data['size'] == 0:
                    logger.info("Empty repository")
                    continue

                language = repo_data['language']
                if language:
                    label, _ = Label.objects.get_or_create(name=language)
                    repo.labels.add(label)

                logger.info("Processing issues and pull requests")
                create_contributions(
                    repo,
                    github.get_repo_issues(owner, repo, session),
                    user_field='user',
                    id_field='id',
                    type_='iss',
                )

                logger.info("Processing commits")
                create_contributions(
                    repo,
                    github.get_repo_commits_except_merges(
                        owner, repo, session=session,
                    ),
                    user_field='author',
                    id_field='sha',
                    type_='cit',
                )

                logger.info("Processing comments")
                create_contributions(
                    repo,
                    github.get_all_types_of_comments(owner, repo, session),
                    user_field='user',
                    id_field='id',
                    type_='cnt',
                )

        session.close()

        logger.info(self.style.SUCCESS(
            "Data fetched from GitHub and saved to the database",
        ))
