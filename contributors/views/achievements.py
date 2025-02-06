from django.views import generic

from contributors.models import Contributor


class AchievementListView(generic.ListView):
    """Achievement list."""

    template_name = 'contributor/achievements_list.html'
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

        context['contributors_amount'] = self.contributors_amount
        context['contributors_with_any_contribution'] = (
            contributors.filter(contribution_amount__gte=1).count()
        )

        # Pull request achievements:
        for pr_num in self.pull_request_ranges_for_achievements:
            context[f'contributors_pull_requests_gte_{pr_num}'] = (
                contributors.filter(pull_requests__gte=pr_num).count()
            )

        # Commit achievements:
        for commit_num in self.commit_ranges_for_achievements:
            context[f'contributors_commits_gte_{commit_num}'] = (
                contributors.filter(commits__gte=commit_num).count()
            )

        # Issue achievements:
        for issue_num in self.issue_ranges_for_achievements:
            context[f'contributors_issues_gte_{issue_num}'] = (
                contributors.filter(issues__gte=issue_num).count()
            )

        # Comment achievements:
        for comment_num in self.comment_ranges_for_achievements:
            context[f'contributors_comments_gte_{comment_num}'] = (
                contributors.filter(comments__gte=comment_num).count()
            )

        # Edition achievements:
        for ed_num in self.edition_ranges_for_achievements:
            context[f'contributors_editions_gte_{ed_num}'] = (
                contributors.filter(editions__gte=ed_num).count()
            )

        return context
