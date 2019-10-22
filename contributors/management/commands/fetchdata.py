from django.core.management.base import BaseCommand

from contributors.models import Contribution, Contributor, Organization
from contributors.utils import github_lib as github


def get_or_create_contributor(login):
    """Returns a contributor object."""
    user_data = github.get_user_data(login)
    contributor, _ = Contributor.objects.get_or_create(
        id=user_data['id'],
        defaults={
            'login': login,
            'name': user_data['name'],
            'html_url': user_data['html_url'],
            'avatar_url': user_data['avatar_url'],
        },
    )
    return contributor


class Command(BaseCommand):
    """A management command for syncing with GitHub."""

    help = 'Saves data from GitHub to database' # noqa A003

    def add_arguments(self, parser):
        """Arguments for the command."""
        parser.add_argument('org', nargs='?', default='Hexlet')

    def handle(self, *args, **options): # noqa WPS110
        """Logic of the command."""
        org_name = options['org']

        gh_org = github.get_org_data(org_name)
        org, _ = Organization.objects.get_or_create(
            id=gh_org['id'],
            defaults={
                'name': gh_org['name'],
                'html_url': gh_org['html_url'],
            },
        )
        self.stdout.write(org.name)

        gh_repos = [
            repo for repo in github.get_org_repos(org) if not repo['fork']
        ]
        for gh_repo in gh_repos:
            repo, _ = org.repository_set.get_or_create(
                id=gh_repo['id'],
                defaults={
                    'name': gh_repo['name'],
                    'full_name': gh_repo['full_name'],
                    'html_url': gh_repo['html_url'],
                },
            )
            self.stdout.write('\t{0}'.format(repo.name))

            self.stdout.write("\t\tProcessing pull requests")
            prs = github.get_repo_prs(org.name, repo.name)
            total_prs_per_user = github.get_total_prs_per_user(prs)

            self.stdout.write("\t\tProcessing issues")
            issues = github.get_repo_issues(org.name, repo.name)
            total_issues_per_user = github.get_total_issues_per_user(
                [issue for issue in issues if 'pull_request' not in issue],
            )

            self.stdout.write("\t\tProcessing comments")
            comments = github.get_repo_comments(org.name, repo.name)
            review_comments = github.get_repo_review_comments(org.name, repo.name)
            total_comments_per_user = github.merge_dicts(
                github.get_total_comments_per_user(comments),
                github.get_total_comments_per_user(review_comments),
            )

            self.stdout.write("\t\tProcessing commits")
            total_commits_per_user = github.get_total_commits_per_user_excluding_merges(
                org.name, repo.name,
            )

            self.stdout.write("\t\tProcessing commit stats")
            contributors = github.get_repo_contributors(org.name, repo.name)
            total_additions_per_user = github.get_total_additions_per_user(contributors)
            total_deletions_per_user = github.get_total_deletions_per_user(contributors)

            contributions_to_totals_mapping = {
                'commits': total_commits_per_user,
                'pull_requests': total_prs_per_user,
                'issues': total_issues_per_user,
                'comments': total_comments_per_user,
                'additions': total_additions_per_user,
                'deletions': total_deletions_per_user,
            }
            contributors_logins = [
                contributor['author']['login'] for contributor in contributors
            ]

            self.stdout.write('\t\tFinishing insertions')
            for login in contributors_logins:
                contributor = get_or_create_contributor(login)
                Contribution.objects.update_or_create(
                    repository=repo,
                    contributor=contributor,
                    defaults={
                        contrib_type: totals.get(login, 0)
                        for contrib_type, totals in contributions_to_totals_mapping.items()
                    },
                )

        self.stdout.write(self.style.SUCCESS(
            'Data fetched from GitHub and saved to the database.',
        ))
