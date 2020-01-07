import logging
import sys
from contextlib import suppress

import requests
from django.core import management
from django.db import IntegrityError
from django.utils import dateparse

from contributors.models import (
    CommitStats,
    Contribution,
    Contributor,
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
    repo.name for repo in Repository.objects.filter(
        is_tracked=False,
    )
)
IGNORED_CONTRIBUTORS = tuple(
    contrib.login for contrib in Contributor.objects.filter(
        is_tracked=False,
    )
)
session = requests.Session()


def get_or_create_contributor(login):
    """Return a contributor object."""
    try:
        return Contributor.objects.get(login=login)
    except Contributor.DoesNotExist:
        user_data = github.get_user_data(login, session)
        contributor, _ = misc.get_or_create_record(Contributor, user_data)
        return contributor


def create_contributions(   # noqa: C901,R701
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
        if not type_:
            pr_or_iss = 'pr' if 'pull_request' in contrib else 'iss'
        if type_ == 'cit':
            datetime = contrib['commit']['author']['date']
        else:
            datetime = contrib['created_at']

        with suppress(IntegrityError):
            contribution = Contribution.objects.create(
                repository=repo,
                contributor=get_or_create_contributor(
                    contrib_author_login,
                ),
                id=contrib[id_field],
                type=type_ or pr_or_iss,
                html_url=contrib['html_url'],
                created_at=dateparse.parse_datetime(datetime),
            )
            if type_ == 'cit':
                commit_data = github.get_commit_data(
                    repo.organization, repo, contribution.id, session,
                )
                CommitStats.objects.create(
                    commit=contribution,
                    additions=commit_data['stats']['additions'],
                    deletions=commit_data['stats']['deletions'],
                )


class Command(management.base.BaseCommand):
    """A management command for syncing with GitHub."""

    help = "Saves data from GitHub to database"  # noqa: A003

    def add_arguments(self, parser):
        """Add arguments for the command."""
        parser.add_argument(
            'org',
            nargs='*',
            default=ORGANIZATIONS,
            help='a list of organization names',
        )
        parser.add_argument(
            '--repo', nargs='*', help='a list of repository full names',
        )

    def handle(self, *args, **options):  # noqa: WPS110,WPS213
        """Collect data from GitHub."""
        logger.info("Data collection started")

        if options['repo']:
            data_of_orgs_and_repos = github.get_data_of_orgs_and_repos(
                repo_full_names=options['repo'],
            )
        elif options['org']:
            data_of_orgs_and_repos = github.get_data_of_orgs_and_repos(
                org_names=options['org'],
            )
        else:
            raise management.base.CommandError(
                "Provide a list of organizations or repositories",
            )

        for org_data in data_of_orgs_and_repos.values():
            org, _ = misc.get_or_create_record(
                Organization, org_data['details'],
            )
            logger.info(org)

            repos_to_process = [
                repo for repo in org_data['repos']
                if repo['name'] not in IGNORED_REPOSITORIES
            ]
            number_of_repos = len(repos_to_process)
            for i, repo_data in enumerate(repos_to_process, start=1):  # noqa: WPS111,E501
                repo, _ = misc.get_or_create_record(org, repo_data)
                logger.info(f"{repo} ({i}/{number_of_repos})")  # noqa: G004
                if repo_data['size'] == 0:
                    logger.info("Empty repository")
                    continue

                logger.info("Processing issues and pull requests")
                create_contributions(
                    repo,
                    github.get_repo_issues(org, repo, session),
                    user_field='user',
                    id_field='id',
                )

                logger.info("Processing commits")
                create_contributions(
                    repo,
                    github.get_repo_commits_except_merges(
                        org, repo, session=session,
                    ),
                    user_field='author',
                    id_field='sha',
                    type_='cit',
                )

                logger.info("Processing comments")
                create_contributions(
                    repo,
                    github.get_all_types_of_comments(org, repo, session),
                    user_field='user',
                    id_field='id',
                    type_='cnt',
                )

        session.close()

        logger.info(self.style.SUCCESS(
            "Data fetched from GitHub and saved to the database",
        ))
