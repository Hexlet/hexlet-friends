import os

from django.core.management.base import BaseCommand
from github import Github

from contributors.models import Commit, Contributor, Organization


class Command(BaseCommand):
    help = 'Saves data from GitHub to database'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            nargs='?',
            default=os.getenv('ORGS_LIST'),
            help='a text file with names of GitHub organizations'
            + ' (default: %(default)s)',
        )

    def handle(self, *args, **options):
        token = os.getenv('GH_TOKEN')
        github = Github(token)

        with open(options['filename']) as file:
            orgs_names = [org_name.rstrip('\n') for org_name in file.readlines()]
        for org_name in orgs_names:
            gh_org = github.get_organization(org_name)
            org, _ = Organization.objects.get_or_create(
                id=gh_org.id,
                defaults={
                    'name': gh_org.name,
                    'html_url': gh_org.html_url,
                },
            )

            gh_repos = [repo for repo in gh_org.get_repos() if not repo.fork]
            for gh_repo in gh_repos:
                repo, _ = org.repository_set.get_or_create(
                    id=gh_repo.id,
                    defaults={
                        'name': gh_repo.name,
                        'full_name': gh_repo.full_name,
                        'html_url': gh_repo.html_url,
                    },
                )

                gh_contributors = gh_repo.get_stats_contributors()
                # in case the list of contributors is empty on GitHub
                if not gh_contributors:
                    continue

                for gh_contributor in gh_contributors:
                    contributor, _ = Contributor.objects.get_or_create(
                        id=gh_contributor.author.id,
                        defaults={
                            'name': gh_contributor.author.name,
                            'login': gh_contributor.author.login,
                            'html_url': gh_contributor.author.html_url,
                        },
                    )
                    additions, deletions = (
                        sum(commit_data) for commit_data in
                        zip(*((week.a, week.d) for week in gh_contributor.weeks))
                    )
                    Commit.objects.update_or_create(
                        repository=repo,
                        contributor=contributor,
                        defaults={
                            'commits': gh_contributor.total,
                            'additions': additions,
                            'deletions': deletions,
                        },
                    )

        self.stdout.write(self.style.SUCCESS(
            'Data fetched from GitHub and saved to the database.',
        ))
