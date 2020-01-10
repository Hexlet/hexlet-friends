import datetime

from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.views.generic.base import TemplateView

from contributors.models import Contributor


class HomeView(TemplateView):
    """Home page view."""

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        num_of_days = 31
        dt_days_ago = timezone.now() - datetime.timedelta(days=num_of_days)
        recent_contributors = Contributor.objects.filter(
            is_visible=True,
            contribution__created_at__gte=dt_days_ago,
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

        context['contributors'] = recent_contributors
        context['since_datetime'] = dt_days_ago
        return context
