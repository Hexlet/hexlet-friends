import logging
import sys

import requests
from django.core.management.base import BaseCommand, CommandError

from contributors.models import (
    Contribution,
    Contributor,
    Organization,
    Repository,
)
from contributors.utils import github_lib as github

# Simultaneous logging to file and stdout
logger = logging.getLogger('GitHub')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def get_or_create_contributor(login):
    """Return a contributor object."""
    user_data = github.get_user_data(login)
    contributor, _ = github.get_or_create_record(Contributor, user_data)
    return contributor


organizations = Organization.objects.filter(is_tracked=True)


class Command(BaseCommand):
    """A management command for syncing with GitHub."""

    help = "Saves data from GitHub to database" # noqa A003

    def add_arguments(self, parser):
        """Add arguments for the command."""
        parser.add_argument('orgs', nargs='?', default=organizations)

    def handle(self, *args, **options): # noqa WPS110
        """Collect data from GitHub."""

        org_names = options['orgs']
        if not org_names:
            raise CommandError("Provide a list of organizations")
        if isinstance(org_names, str):
            org_names = org_names.split()

        logger.info("Data collection started")

        session = requests.Session()
        for org_name in org_names:
            gh_org = github.get_org_data(org_name, session)
            org, _ = github.get_or_create_record(Organization, gh_org)
            logger.info(org)

            ignored_repos = [
                repo.name for repo in Repository.objects.filter(
                    is_tracked=False,
                )
            ]
            gh_repos = [
                repo for repo in github.get_org_repos(org)
                if repo['name'] not in ignored_repos
            ]
            number_of_repos = len(gh_repos)
            for i, gh_repo in enumerate(gh_repos, start=1): # noqa WPS111
                repo, _ = github.get_or_create_record(org, gh_repo)
                logger.info(f"{repo} ({i}/{number_of_repos})")  # noqa G004
                if gh_repo['size'] == 0:
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
                total_comments_per_user = github.merge_dicts(
                    github.get_total_comments_per_user(comments),
                    github.get_total_comments_per_user(review_comments),
                )

                logger.info("Processing commits")
                total_commits_per_user = (
                    github.get_total_commits_per_user_excluding_merges(
                        org, repo,
                    )
                )

                logger.info("Processing commits stats")
                ignored_contributors = [
                    contrib.login for contrib in Contributor.objects.filter(
                        is_tracked=False,
                    )
                ]
                contributors = [
                    contrib for contrib in github.get_repo_contributors(
                        org, repo, session,
                    ) if contrib['login'] not in ignored_contributors
                ]
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

        logger.info(self.style.SUCCESS(
            "Data fetched from GitHub and saved to the database",
        ))
