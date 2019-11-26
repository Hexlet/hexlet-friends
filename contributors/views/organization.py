from django.db.models import Count, Sum
from django.views import generic

from contributors.models import Organization


class DetailView(generic.DetailView):
    """Organization's details."""

    model = Organization
    template_name = 'organization_details.html'

    def get_context_data(self, **kwargs):
        """Adds additional context for the organization."""
        context = super().get_context_data(**kwargs)

        repos_data = self.object.repository_set.annotate(
            pull_requests=Sum('contribution__pull_requests'),
            issues=Sum('contribution__issues'),
            contributors_count=Count('contribution'),
        )

        context['repositories'] = repos_data
        return context
