from django.core.management.base import BaseCommand

from app.models import Contributor
from app.utils import fetch_info_from_github as github


class Command(BaseCommand):
    """Fetch contributors data from github api and save in db."""

    help = 'Fetch commits and prs by user for Github Login'  # noqa: A003

    def add_arguments(self, parser):
        """Extend command aruments."""
        parser.add_argument('user', type=str, nargs='?', default='Hexlet')

    def handle(self, *args, **options):  # noqa: WPS 210, D204
        user = options['user']

        repos = filter(
            lambda api_data: not api_data['fork'],
            github.fetch_all_repos_for_user(user),
        )
        user_by_commits = {}
        user_by_prs = {}

        for repo in repos:
            repo_name = repo['name']
            self.stdout.write(repo_name)
            commits = github.fetch_commits_for_repo(repo_name, user)
            user_by_commits = github.merge_dicts(
                user_by_commits,
                github.get_user_by_commits(commits),
            )
            prs = github.fetch_pr_for_repo(repo_name, user)
            user_by_prs = github.merge_dicts(
                user_by_prs,
                github.get_user_by_prs(prs),
            )

        for commit_user_login in user_by_commits:
            contributor, created = Contributor.objects.get_or_create(
                login=commit_user_login,
            )
            contributor.commits += user_by_commits[commit_user_login]
            contributor.save()

        for pr_user_login in user_by_prs:
            contributor, created = Contributor.objects.get_or_create(
                login=pr_user_login,
            )
            contributor.pull_requests += user_by_prs[pr_user_login]
            contributor.save()

        self.stdout.write('Ok')
