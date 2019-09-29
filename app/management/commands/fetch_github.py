from django.core.management.base import BaseCommand

from app.utils.fetch_info_from_github import fetch_all_repos_for_user
from app.utils.fetch_info_from_github import fetch_pr_for_repo
from app.utils.fetch_info_from_github import fetch_commits_for_repo
from app.utils.fetch_info_from_github import get_user_by_commits
from app.utils.fetch_info_from_github import get_user_by_prs
from app.utils.fetch_info_from_github import sum_dicts
from app.models import Profile


class Command(BaseCommand):
    help = 'Fetch commits and prs by user for Github Login'

    def add_arguments(self, parser):
        parser.add_argument('user', type=str, nargs='?', default='Hexlet')

    def handle(self, *args, **options):
        user = options['user']

        repos = filter(lambda x: x['fork'] is False, fetch_all_repos_for_user(user))
        user_by_commits = {}
        user_by_prs = {}

        for repo in repos:
            self.stdout.write(repo['name'])
            commits = fetch_commits_for_repo(repo['name'], user)
            user_by_commits = sum_dicts(user_by_commits, get_user_by_commits(commits))
            prs = fetch_pr_for_repo(repo['name'], user)
            user_by_prs = sum_dicts(user_by_prs, get_user_by_prs(prs))

        for login in user_by_commits:
            obj, created = Profile.objects.get_or_create(login=login)
            obj.commits += user_by_commits[login]
            obj.save()

        for login in user_by_prs:
            obj, created = Profile.objects.get_or_create(login=login)
            obj.pull_requests += user_by_prs[login]
            obj.save()

        self.stdout.write('Ok')
