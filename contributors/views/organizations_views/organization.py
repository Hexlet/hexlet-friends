from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from contributors.models import Organization, Repository
from contributors.views.repositories_views import repositories


class OrgRepositoryList(repositories.ListView):
    """An organization's details."""

    template_name = 'contributors_sections/organizations/organization_details.html'
    sortable_fields = (
        'name',
        'project',
        'pull_requests',
        'issues',
        ('contributors_count', _("Contributors")),
    )
    context_object_name = 'repositories'

    def get_queryset(self):
        """Get a dataset."""
        self.organization = get_object_or_404(
            Organization.objects.prefetch_related(
                Prefetch(
                    'repository_set',
                    queryset=Repository.objects.filter(is_visible=True).annotate(
                        pull_requests=Count('contribution', filter=Q(contribution__type='pr')),  # noqa: E501
                        issues=Count('contribution', filter=Q(contribution__type='iss')),
                        contributors_count=Count('contribution__contributor', distinct=True)  # noqa: E501
                    )
                )
            ),
            name=self.kwargs['slug'],
        )
        return self.organization.repository_set.all()

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)
        context['organization'] = self.organization
        return context
