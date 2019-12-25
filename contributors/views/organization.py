from django.db.models import Count, Q
from django.views import generic

from contributors.models import Organization


class DetailView(generic.DetailView):
    """Organization's details."""

    model = Organization
    template_name = 'organization_details.html'

    def get_context_data(self, **kwargs):
        """Add additional context for the organization."""
        context = super().get_context_data(**kwargs)

        repositories = (
            self.object.repository_set.filter(
                is_visible=True,
                contribution__contributor__is_visible=True,
            ).annotate(
                pull_requests=Count(
                    'contribution', filter=Q(contribution__type='pr'),
                ),
                issues=Count(
                    'contribution', filter=Q(contribution__type='iss'),
                ),
                contributors_count=Count(
                    'contribution__contributor', distinct=True,
                ),
            )
        )

        context['repositories'] = repositories
        return context
