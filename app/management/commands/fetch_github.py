from django.core.management.base import BaseCommand

from app.utils import fetch_info_from_github as github
from app.utils.populate_db_start_data import populate_db
from app.models import Organization, Repository


class Command(BaseCommand):
    help = 'Fetch commits and prs by user for Github Login'

    def add_arguments(self, parser):
        parser.add_argument('user', type=str, nargs='?', default='Hexlet')

    def handle(self, *args, **options):
        user = options['user']

        org = github.fetch_organization_by_name(user)
        organization, _ = Organization.objects.get_or_create(
            id=org['id'],
            name=org['name'],
            html_url=org['html_url'],
        )

        repos = filter(lambda x: not x['fork'], github.fetch_all_repos_for_user(user))
        for repo in repos:
            repository, _ = Repository.objects.get_or_create(
                pk=repo['id'],
                name=repo['name'],
                full_name=repo['full_name'],
                html_url=repo['html_url'],
                organization=organization
            )
            self.stdout.write(repository.name)
            commits = github.fetch_commits_for_repo(repository.name, organization.name)
            user_by_commits = github.get_user_by_commits(commits)

            prs = github.fetch_pr_for_repo(repository.name, organization.name)
            user_by_prs = github.get_user_by_prs(prs)

            issues = github.fetch_issues_for_repo(repository.name, organization.name)
            user_by_issues = github.get_user_by_issues(filter(lambda x: x.get('pull_request', False), issues))

            issues_comments = (github.fetch_comments_for_repo_issue(repository.name, issue['number'], organization.name)
                               for issue in issues)
            prs_comments = (github.fetch_reviews_for_repo_pr(repository.name, pr['number'], organization.name)
                            for pr in prs)
            user_by_comments = github.sum_dicts(github.get_user_by_comments(issues_comments),
                                                github.get_user_by_comments(prs_comments))

            stats = github.fetch_stats_by_repo(repository.name, organization.name)
            user_by_additions = github.get_user_by_additions(stats)
            user_by_deletions = github.get_user_by_deletions(stats)

            populate_db(user_by_commits, repository, 'commits')
            populate_db(user_by_prs, repository, 'pull_requests')
            populate_db(user_by_issues, repository, 'issues')
            populate_db(user_by_comments, repository, 'comments')
            populate_db(user_by_additions, repository, 'additions')
            populate_db(user_by_deletions, repository, 'deletions')
        self.stdout.write('Ok')
