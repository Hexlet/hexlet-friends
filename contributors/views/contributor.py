from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce
from django.views import generic

from contributors.models import Contributor, Repository


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

        context['repositories'] = repositories
        return context
