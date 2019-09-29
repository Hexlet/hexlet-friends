from django.core.management.base import BaseCommand

from app.utils import fetch_info_from_github as github
from app.models import Profile


class Command(BaseCommand):
    help = 'Fetch commits and prs by user for Github Login'

    def add_arguments(self, parser):
        parser.add_argument('user', type=str, nargs='?', default='Hexlet')

    def handle(self, *args, **options):
        user = options['user']

        repos = filter(lambda x: not x['fork'], github.fetch_all_repos_for_user(user))
        user_by_commits = {}
        user_by_prs = {}

        for repo in repos:
            repo_name = repo['name']
            self.stdout.write(repo_name)
            commits = github.fetch_commits_for_repo(repo_name, user)
            user_by_commits = github.sum_dicts(user_by_commits, github.get_user_by_commits(commits))
            prs = github.fetch_pr_for_repo(repo_name, user)
            user_by_prs = github.sum_dicts(user_by_prs, github.get_user_by_prs(prs))

        for login in user_by_commits:
            obj, created = Profile.objects.get_or_create(login=login)
            obj.commits += user_by_commits[login]
            obj.save()

        for login in user_by_prs:
            obj, created = Profile.objects.get_or_create(login=login)
            obj.pull_requests += user_by_prs[login]
            obj.save()

        self.stdout.write('Ok')
