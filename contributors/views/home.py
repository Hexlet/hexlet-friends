from dateutil import relativedelta
from django.db.models import Count, Q, Sum  # noqa: WPS347
from django.db.models.functions import Coalesce, ExtractMonth
from django.utils import timezone
from django.views.generic.base import TemplateView

from contributors.models import Contribution, Contributor
from contributors.utils import misc


class HomeView(TemplateView):
    """Home page view."""

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        dt_now = timezone.now()
        dt_month_ago = dt_now - relativedelta.relativedelta(months=1)
        eleven_months_ago = (dt_now - relativedelta.relativedelta(
            months=11, day=1,   # noqa: WPS432
        )).date()

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
        months_with_contrib_sums = Contribution.objects.filter(
            contributor__is_visible=True,
            created_at__gte=eleven_months_ago,
        ).annotate(
            month=ExtractMonth('created_at'),
        ).values('month', 'type').annotate(count=Count('id'))

        sums_of_contribs_by_months = misc.group_contribs_by_months(
            months_with_contrib_sums,
        )

        contributions = misc.get_contrib_sums_distributed_over_months(
            sums_of_contribs_by_months,
        )

        context['contributors'] = contributors_for_month
        context['since_datetime'] = dt_month_ago
        context['contributions'] = contributions
        return context
