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

    pull_request_ranges_for_achievements = [100, 50, 25, 10, 1]
    commit_ranges_for_achievements = [200, 100, 50, 25, 1]
    issue_ranges_for_achievements = [50, 25, 10, 5, 1]
    comment_ranges_for_achievements = [200, 100, 50, 25, 1]
    edition_ranges_for_achievements = [1000, 500, 250, 100, 1]

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

        context['commits'] = contributions['contributor_commits']
        context['pull_requests'] = contributions['contributor_pull_requests']
        context['issues'] = contributions['contributor_issues']
        context['comments'] = contributions['contributor_comments']
        context['total_editions'] = sum([
            0 if edit is None else edit
            for edit in [
                contributions['contributor_additions'],
                contributions['contributor_deletions'],
            ]
        ])
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
        context['contributors_with_any_contribution'] = (
            contributors.filter(contribution_amount__gte=1).count()
        )

        # Pull request achievements:
        for pr_num in self.pull_request_ranges_for_achievements:
            context[f'contributor_pull_requests_gte_{pr_num}'] = pr_num
            context[f'contributors_pull_requests_gte_{pr_num}'] = (
                contributors.filter(pull_requests__gte=pr_num).count()
            )

        # Commit achievements:
        for commit_num in self.commit_ranges_for_achievements:
            context[f'contributor_commits_gte_{commit_num}'] = commit_num
            context[f'contributors_commits_gte_{commit_num}'] = (
                contributors.filter(commits__gte=commit_num).count()
            )

        # Issue achievements:
        for issue_num in self.issue_ranges_for_achievements:
            context[f'contributor_issues_gte_{issue_num}'] = issue_num
            context[f'contributors_issues_gte_{issue_num}'] = (
                contributors.filter(issues__gte=issue_num).count()
            )

        # Comment achievements:
        for comment_num in self.comment_ranges_for_achievements:
            context[f'contributor_comments_gte_{comment_num}'] = comment_num
            context[f'contributors_comments_gte_{comment_num}'] = (
                contributors.filter(comments__gte=comment_num).count()
            )

        # Edition achievements:
        for ed_num in self.edition_ranges_for_achievements:
            context[f'contributor_editions_gte_{ed_num}'] = ed_num
            context[f'contributors_editions_gte_{ed_num}'] = (
                contributors.filter(editions__gte=ed_num).count()
            )

        return context
