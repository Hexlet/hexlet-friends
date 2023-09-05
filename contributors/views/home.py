from django.views.generic.base import TemplateView

from contributors.models import Contribution, Contributor

LATEST_COUNT = 10


def get_top10(dataset, contrib_type):
    """Return top 10 contributors of the type from the dataset."""
    return dataset.order_by(f'-{contrib_type}')[:LATEST_COUNT]


def get_latest_contributions(dataset, contrib_type):
    """Return latest contributions of contrib_type."""
    return dataset.filter(type=contrib_type).order_by(
        '-created_at',
    )[:LATEST_COUNT]


class HomeView(TemplateView):
    """Home page view."""

    template_name = 'home.html'

    def get_context_data(self, **kwargs):  # noqa: WPS210
        """Add context."""
        context = super().get_context_data(**kwargs)

        contributors_for_month = (
            Contributor.objects.visible_with_monthly_stats()
        )
        contributors_for_week = (
            Contributor.objects.visible_with_weekly_stats()
        )

        contributions_for_month = (
            Contribution.objects.visible_for_month()
        )

        contributions_for_week = (
            Contribution.objects.visible_for_week()
        )

        top10_committers_of_month = get_top10(
            contributors_for_month, 'commits',
        )
        top10_requesters_of_month = get_top10(
            contributors_for_month, 'pull_requests',
        )
        top10_reporters_of_month = get_top10(
            contributors_for_month, 'issues',
        )
        top10_commentators_of_month = get_top10(
            contributors_for_month, 'comments',
        )

        top10_committers_of_week = get_top10(
            contributors_for_week, 'commits',
        )
        top10_requesters_of_week = get_top10(
            contributors_for_week, 'pull_requests',
        )
        top10_reporters_of_week = get_top10(
            contributors_for_week, 'issues',
        )
        top10_commentators_of_week = get_top10(
            contributors_for_week, 'comments',
        )

        latest_month_issues = get_latest_contributions(
            contributions_for_month, 'iss',
        )

        latest_week_issues = get_latest_contributions(
            contributions_for_week, 'iss',
        )

        latest_month_pr = get_latest_contributions(
            contributions_for_month, 'pr',
        )

        latest_week_pr = get_latest_contributions(
            contributions_for_week, 'pr',
        )

        context.update(
            {
                'contributors_for_month': contributors_for_month,
                'top10_committers_of_month': top10_committers_of_month,
                'top10_requesters_of_month': top10_requesters_of_month,
                'top10_reporters_of_month': top10_reporters_of_month,
                'top10_commentators_of_month': top10_commentators_of_month,
                'top10_committers_of_week': top10_committers_of_week,
                'top10_requesters_of_week': top10_requesters_of_week,
                'top10_reporters_of_week': top10_reporters_of_week,
                'top10_commentators_of_week': top10_commentators_of_week,
                'contributions_for_year': Contribution.objects.for_year(),
                'latest_month_issues': latest_month_issues,
                'latest_week_issues': latest_week_issues,
                'latest_month_pr': latest_month_pr,
                'latest_week_pr': latest_week_pr,
            },
        )

        return context
