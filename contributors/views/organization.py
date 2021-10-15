from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from contributors.models import Organization
from contributors.views import repositories


class OrgRepositoryList(repositories.ListView):
    """An organization's details."""

    template_name = 'organization_details.html'
    sortable_fields = (  # noqa: WPS317
        'name',
        'project',
        'pull_requests',
        'issues',
        ('contributors_count', _("Contributors")),
    )

    def get_queryset(self):
        """Get a dataset."""
        self.organization = get_object_or_404(
            Organization, name=self.kwargs['slug'],
        )
        self.queryset = self.queryset.filter(organization=self.organization)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)
        context['organization'] = self.organization
        return context
