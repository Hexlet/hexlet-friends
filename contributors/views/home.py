import datetime
from collections import deque

from dateutil import relativedelta
from django.db.models import Count, Q, Sum  # noqa: WPS347
from django.db.models.functions import Coalesce, ExtractMonth
from django.utils import timezone
from django.views.generic.base import TemplateView

from contributors.models import Contribution, Contributor


def get_array_of_numbers(contribs_per_month, contrib_type):
    """
    Return an array of 12 elements for contributions of the given type.

    Each position corresponds to a month ending with the current month.
    """
    month_numbers = range(1, 13)    # noqa: WPS432
    current_month_number = datetime.date.today().month
    array = deque([
        contribs_per_month.get(month_number, {}).get(contrib_type, 0)
        for month_number in month_numbers
    ])
    array.rotate(-current_month_number)
    return list(array)


class HomeView(TemplateView):
    """Home page view."""

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        dt_now = timezone.now()
        dt_month_ago = dt_now - relativedelta.relativedelta(months=1)
        dt11months_ago = dt_now - relativedelta.relativedelta(
            years=1, months=-1, day=1, hour=0, minute=0, second=0, microsecond=0,   # noqa: E501
        )

        contributors_for_month = Contributor.objects.filter(
            is_visible=True,
            contribution__created_at__gte=dt_month_ago,
        ).annotate(
            commits=Count('id', filter=Q(contribution__type='cit')),
            additions=Coalesce(Sum('contribution__stats__additions'), 0),
            deletions=Coalesce(Sum('contribution__stats__deletions'), 0),
            pull_requests=Count(
                'contribution', filter=Q(contribution__type='pr'),
            ),
            issues=Count('contribution', filter=Q(contribution__type='iss')),
            comments=Count('contribution', filter=Q(contribution__type='cnt')),
        )
        contrib_counts_with_months = Contribution.objects.filter(
            contributor__is_visible=True,
            created_at__gte=dt11months_ago,
        ).annotate(
            month=ExtractMonth('created_at'),
        ).values('month', 'type').annotate(count=Count('id'))

        contribs_per_month = {}
        for contrib in contrib_counts_with_months:
            month = contribs_per_month.setdefault(contrib['month'], {})
            month[contrib['type']] = contrib['count']

        contributions = {
            'commits': get_array_of_numbers(contribs_per_month, 'cit'),
            'pull_requests': get_array_of_numbers(contribs_per_month, 'pr'),
            'issues': get_array_of_numbers(contribs_per_month, 'iss'),
            'comments': get_array_of_numbers(contribs_per_month, 'cnt'),
        }

        context['contributors'] = contributors_for_month
        context['since_datetime'] = dt_month_ago
        context['contributions'] = contributions
        return context
