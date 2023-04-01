from django.views.generic.base import TemplateView

from contributors.models import Contribution, Contributor
from contributors.utils.misc import datetime_month_ago, datetime_week_ago

LATEST_ISSUES_COUNT = 10


def get_top10(dataset, contrib_type):
    """Return top 10 contributors of the type from the dataset."""
    return dataset.order_by('-{0}'.format(contrib_type))[:10]


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

        latest_month_issues = Contribution.objects.filter(
            repository__is_visible=True,
            type='iss',
            created_at__gte=datetime_month_ago(),
        ).distinct().order_by('-created_at')[:LATEST_ISSUES_COUNT]

        latest_week_issues = Contribution.objects.filter(
            repository__is_visible=True,
            type='iss',
            created_at__gte=datetime_week_ago(),
        ).distinct().order_by('-created_at')[:LATEST_ISSUES_COUNT]

        latest_month_pr = Contribution.objects.filter(
            repository__is_visible=True,
            type='pr',
            created_at__gte=datetime_month_ago(),
        ).distinct().order_by('-created_at')[:LATEST_ISSUES_COUNT]

        latest_week_pr = Contribution.objects.filter(
            repository__is_visible=True,
            type='pr',
            created_at__gte=datetime_week_ago(),
        ).distinct().order_by('-created_at')[:LATEST_ISSUES_COUNT]

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
