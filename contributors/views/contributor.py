from dateutil import relativedelta
from django.db.models import Count, Q, Sum  # noqa: WPS347
from django.db.models.functions import Coalesce, ExtractMonth
from django.utils import timezone
from django.views import generic

from contributors.models import Contributor, Repository
from contributors.utils import misc


class DetailView(generic.DetailView):
    """Contributor's details."""

    model = Contributor
    template_name = 'contributor_details.html'

    def get_context_data(self, **kwargs):
        """Add additional context for the contributor."""
        context = super().get_context_data(**kwargs)

        repositories = Repository.objects.select_related(
            'organization',
        ).filter(
            is_visible=True,
            contribution__contributor=self.object,
        ).annotate(
            commits=Count('id', filter=Q(contribution__type='cit')),
            additions=Coalesce(Sum('contribution__stats__additions'), 0),
            deletions=Coalesce(Sum('contribution__stats__deletions'), 0),
            pull_requests=Count(
                'contribution', filter=Q(contribution__type='pr'),
            ),
            issues=Count('contribution', filter=Q(contribution__type='iss')),
            comments=Count('contribution', filter=Q(contribution__type='cnt')),
        ).order_by('organization', 'name')

        eleven_months_ago = (timezone.now() - relativedelta.relativedelta(
            months=11, day=1,   # noqa: WPS432
        )).date()

        months_with_contrib_sums = self.object.contribution_set.filter(
            created_at__gte=eleven_months_ago,
        ).annotate(
            month=ExtractMonth('created_at'),
        ).values('month', 'type').annotate(count=Count('id'))

        monthly_sums_of_contribs = misc.group_contribs_by_months(
            months_with_contrib_sums,
        )

        contributions = misc.contrib_sums_distributed_over_months(
            monthly_sums_of_contribs,
        )

        context['repositories'] = repositories
        context['contributions'] = contributions
        return context
