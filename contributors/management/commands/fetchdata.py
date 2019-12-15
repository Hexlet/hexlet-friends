import logging
import sys

import requests
from django.core import management

from contributors.models import (
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


def get_or_create_contributor(login):
    """Return a contributor object."""
    user_data = github.get_user_data(login)
    contributor, _ = misc.get_or_create_record(Contributor, user_data)
    return contributor


organizations = Organization.objects.filter(is_tracked=True)


class Command(management.base.BaseCommand):
    """A management command for syncing with GitHub."""

    help = "Saves data from GitHub to database"  # noqa: A003

    def __init__(self, *args, **kwargs):
        """Command initialization."""
        super().__init__(*args, **kwargs)
        self.repos_to_rehandle = []

    def add_arguments(self, parser):
        """Add arguments for the command."""
        parser.add_argument(
            'org',
            nargs='*',
            default=organizations,
            help='a list of organization names',
        )
        parser.add_argument(
            '--repo', nargs='*', help='a list of repository full names',
        )

    def handle(self, *args, **options):  # noqa: WPS
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

        session = requests.Session()

        for org_data in data_of_orgs_and_repos.values():
            org, _ = misc.get_or_create_record(
                Organization, org_data['details'],
            )
            logger.info(org)

            ignored_repos = [
                repo.name for repo in Repository.objects.filter(
                    is_tracked=False,
                )
            ]
            repos_to_process = [
                repo for repo in org_data['repos']
                if repo['name'] not in ignored_repos
            ]
            number_of_repos = len(repos_to_process)
            for i, repo_data in enumerate(repos_to_process, start=1):  # noqa: WPS111,E501
                repo, _ = misc.get_or_create_record(org, repo_data)
                logger.info(f"{repo} ({i}/{number_of_repos})")  # noqa: G004
                if repo_data['size'] == 0:
                    logger.info("Empty repository")
                    continue

                logger.info("Processing pull requests")
                prs = github.get_repo_prs(org, repo, session)
                total_prs_per_user = github.get_total_prs_per_user(prs)

                logger.info("Processing issues")
                issues_and_prs = github.get_repo_issues(org, repo, session)
                issues = [
                    issue for issue in issues_and_prs
                    if 'pull_request' not in issue
                ]
                total_issues_per_user = github.get_total_issues_per_user(
                    issues,
                )

                logger.info("Processing comments")
                comments = github.get_repo_comments(org, repo, session)
                review_comments = github.get_repo_review_comments(
                    org, repo, session,
                )
                total_comments_per_user = misc.merge_dicts(
                    github.get_total_comments_per_user(comments),
                    github.get_total_comments_per_user(review_comments),
                )

                ignored_contributors = [
                    contrib.login for contrib in Contributor.objects.filter(
                        is_tracked=False,
                    )
                ]
                try:
                    contributors = [
                        contrib for contrib in github.get_repo_contributors(
                            org, repo, session,
                        ) if contrib['login'] not in ignored_contributors
                    ]
                except github.Accepted:
                    logger.info("Data is not ready. Will retry")
                    self.repos_to_rehandle.append(repo.full_name)
                    continue

                logger.info("Processing commits")
                total_commits_per_user = {
                    contributor['login']: contributor['total']
                    for contributor in contributors
                }

                logger.info("Processing commits stats")
                total_additions_per_user = github.get_total_additions_per_user(
                    contributors,
                )
                total_deletions_per_user = github.get_total_deletions_per_user(
                    contributors,
                )

                contributions_to_totals_mapping = {
                    'commits': total_commits_per_user,
                    'pull_requests': total_prs_per_user,
                    'issues': total_issues_per_user,
                    'comments': total_comments_per_user,
                    'additions': total_additions_per_user,
                    'deletions': total_deletions_per_user,
                }
                contributors_logins = [
                    contributor['login'] for contributor in contributors
                ]

                logger.info("Finishing insertions")
                for login in contributors_logins:
                    contributor = get_or_create_contributor(login)
                    Contribution.objects.update_or_create(
                        repository=repo,
                        contributor=contributor,
                        defaults={
                            contrib_type: totals.get(login, 0)
                            for contrib_type, totals in
                            contributions_to_totals_mapping.items()
                        },
                    )
        session.close()

        if self.repos_to_rehandle:
            logger.info("Rehandling some repositories")
            management.call_command('fetchdata', repo=self.repos_to_rehandle)
        else:
            logger.info(self.style.SUCCESS(
                "Data fetched from GitHub and saved to the database",
            ))
