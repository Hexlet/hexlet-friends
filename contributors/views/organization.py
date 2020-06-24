from django.utils.translation import gettext_lazy as _

from contributors.models import Organization
from contributors.views import repositories


class OrgRepositoryList(repositories.ListView):
    """An organization's details."""

    template_name = 'organization_details.html'
    sortable_fields = (  # noqa: WPS317
        'name',
        ('project__name', _("Project")),
        'pull_requests',
        'issues',
        ('contributors_count', _("Contributors")),
    )

    def get_queryset(self):
        """Get a dataset."""
        self.organization = Organization.objects.get(pk=self.kwargs['pk'])
        return super().get_queryset().filter(organization=self.organization)

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)
        context['organization'] = self.organization
        return context
