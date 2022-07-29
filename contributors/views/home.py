from django.views.generic.base import TemplateView

from contributors.models import Contribution, Contributor
from contributors.utils.misc import datetime_month_ago


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

        top10_committers = get_top10(contributors_for_month, 'commits')
        top10_requesters = get_top10(contributors_for_month, 'pull_requests')
        top10_reporters = get_top10(contributors_for_month, 'issues')
        top10_commentators = get_top10(contributors_for_month, 'comments')

        latest_issues = Contribution.objects.filter(
            repository__is_visible=True,
            type__in=['pr', 'iss'],
        ).order_by('-created_at')[:11]

        context.update(
            {
                'contributors_for_month': contributors_for_month,
                'top10_committers': top10_committers,
                'top10_requesters': top10_requesters,
                'top10_reporters': top10_reporters,
                'top10_commentators': top10_commentators,
                'dt_month_ago': datetime_month_ago(),
                'contributions_for_year': Contribution.objects.for_year(),
                'latest_issues': latest_issues,
            }
        )

        return context
