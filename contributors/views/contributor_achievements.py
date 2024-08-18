from django.db import models
from django.db.models.functions import Coalesce
from django.views import generic

from contributors.models import Contributor, Repository

ID = 'id'


class ContributorAchievementListView(generic.ListView):
    """Achievement list."""

    template_name = 'contributor/contributor_achievements_list.html'
    model = Contributor
    contributors = Contributor.objects.with_contributions()

    pull_request_ranges_for_achievements = [1, 10, 25, 50, 100]
    commit_ranges_for_achievements = [1, 25, 50, 100, 200]
    issue_ranges_for_achievements = [1, 5, 10, 25, 50]
    comment_ranges_for_achievements = [1, 25, 50, 100, 200]
    edition_ranges_for_achievements = [1, 100, 250, 500, 1000]

    def get_context_data(self, **kwargs):
        """Add context data for achievement list."""
        self.contributors_amount = Contributor.objects.count()
        context = super().get_context_data(**kwargs)
        contributors = Contributor.objects.with_contributions()
        current_contributor = (
            Contributor.objects.get(login=self.kwargs['slug'])
        )

        repositories = Repository.objects.select_related(
            'organization',
        ).filter(
            is_visible=True,
            contribution__contributor=current_contributor,
        ).annotate(
            commits=models.Count('id', filter=models.Q(contribution__type='cit')),
            additions=Coalesce(models.Sum('contribution__stats__additions'), 0),
            deletions=Coalesce(models.Sum('contribution__stats__deletions'), 0),
            pull_requests=models.Count(
                'contribution', filter=models.Q(contribution__type='pr'),
            ),
            issues=models.Count('contribution', filter=models.Q(contribution__type='iss')),
            comments=models.Count('contribution', filter=models.Q(contribution__type='cnt')),
        ).order_by('organization', 'name')

        contributions = repositories.values().aggregate(
            contributor_deletions=models.Sum('deletions'),
            contributor_additions=models.Sum('additions'),
            contributor_commits=models.Sum('commits'),
            contributor_pull_requests=models.Sum('pull_requests'),
            contributor_issues=models.Sum('issues'),
            contributor_comments=models.Sum('comments'),
        )

        finished = []
        unfinished = []

        context['commits'] = contributions['contributor_commits']
        context['pull_requests'] = contributions['contributor_pull_requests']
        context['issues'] = contributions['contributor_issues']
        context['comments'] = contributions['contributor_comments']
        editions = sum([
            0 if edit is None else edit
            for edit in [
                contributions['contributor_additions'],
                contributions['contributor_deletions'],
            ]
        ])
        context['total_editions'] = editions

        context['total_actions'] = sum([
            0 if action is None else action
            for action in [
                contributions['contributor_commits'],
                contributions['contributor_pull_requests'],
                contributions['contributor_issues'],
                contributions['contributor_comments'],
                contributions['contributor_additions'],
                contributions['contributor_deletions'],
            ]
        ])

        context['pull_request_ranges_for_achievements'] = (
            self.pull_request_ranges_for_achievements
        )
        context['current_contributor'] = current_contributor
        context['contributors_amount'] = self.contributors_amount
        context['contributors_with_any_contribution'] = {
            'stat': (
                contributors.filter(contribution_amount__gte=1).count()
            ),
            'acomplished': True,
        }

        # Pull request achievements:
        for pr_num in self.pull_request_ranges_for_achievements:
            context[f'contributors_pull_requests_gte_{pr_num}'] = {
                'stat': (
                    contributors.filter(pull_requests__gte=pr_num).count()
                ),
                'acomplished': True,
            }
            a_data = {
                'img': f'images/achievments_icons/pull_requests-{pr_num}.svg',
                'name': f'Pull requests (equal to or more than {pr_num})',
                'description': f"Make pull requests in amount of equal to or more than {pr_num}",
                'accomplished': 'yes',
            }
            if pr_num > (
                0 if contributions['contributor_pull_requests'] is None else contributions['contributor_pull_requests']
            ):
                unfinished.append(a_data)
                context[f'contributors_pull_requests_gte_{pr_num}']['acomplished'] = False
            else:
                finished.append(a_data)

        # Commit achievements:
        for commit_num in self.commit_ranges_for_achievements:
            context[f'contributors_commits_gte_{commit_num}'] = {
                'stat': (
                    contributors.filter(commits__gte=commit_num).count()
                ),
                'acomplished': True,
            }
            a_data = {
                'img': f'images/achievments_icons/commits-{commit_num}.svg',
                'name': f'Commits (equal to or more than {commit_num})',
                'description': f"Make commits in amount of equal to or more than {commit_num}",
            }
            if commit_num > (
                0 if contributions['contributor_commits'] is None else contributions['contributor_commits']
            ):
                unfinished.append(a_data)
                context[f'contributors_commits_gte_{commit_num}']['acomplished'] = False
            else:
                finished.append(a_data)

        # Issue achievements:
        for issue_num in self.issue_ranges_for_achievements:
            context[f'contributors_issues_gte_{issue_num}'] = {
                'stat': (
                    contributors.filter(issues__gte=issue_num).count()
                ),
                'acomplished': True,
            }
            a_data = {
                'img': f'images/achievments_icons/issues-{issue_num}.svg',
                'name': f'Issues (equal to or more than {issue_num})',
                'description': f"Make issues in amount of equal to or more than {issue_num}",
            }
            if issue_num > (
                0 if contributions['contributor_issues'] is None else contributions['contributor_issues']
            ):
                unfinished.append(a_data)
                context[f'contributors_issues_gte_{issue_num}']['acomplished'] = False
            else:
                finished.append(a_data)

        # Comment achievements:
        for comment_num in self.comment_ranges_for_achievements:
            context[f'contributors_comments_gte_{comment_num}'] = {
                'stat': (
                    contributors.filter(comments__gte=comment_num).count()
                ),
                'acomplished': True,
            }
            a_data = {
                'img': f'images/achievments_icons/comments-{comment_num}.svg',
                'name': f'Comments (equal to or more than {comment_num})',
                'description': f"Make comments in amount of equal to or more than {comment_num}",
            }
            if comment_num > (
                0 if contributions['contributor_comments'] is None else contributions['contributor_comments']
            ):
                unfinished.append(a_data)
                context[f'contributors_comments_gte_{comment_num}']['acomplished'] = False
            else:
                finished.append(a_data)

        # Edition achievements:
        for ed_num in self.edition_ranges_for_achievements:
            context[f'contributors_editions_gte_{ed_num}'] = {
                'stat': (
                    contributors.filter(editions__gte=ed_num).count()
                ),
                'acomplished': True,
            }
            a_data = {
                'img': f'images/achievments_icons/code_editions-{ed_num}.svg',
                'name': f'Additions and deletions (equal to or more than {ed_num})',
                'description': f"Make additions and deletions in amount of equal to or more than {ed_num}",
            }

            if ed_num > editions:
                unfinished.append(a_data)
                context[f'contributors_editions_gte_{ed_num}']['acomplished'] = False
            else:
                finished.append(a_data)

        a_data = {
            'img': 'images/achievments_icons/friend.svg',
            'name': 'Hexlet friend',
            'description': "Make any contribution to Hexlet projects",
        }
        if finished:
            finished.insert(0, a_data)
        else:
            unfinished.insert(0, a_data)
            context['contributors_with_any_contribution']['acomplished'] = False

        context['finished'] = finished
        context['unfinished'] = unfinished
        context['closed'] = len(finished)
        context['all_achievements'] = len(finished) + len(unfinished)
        return context
