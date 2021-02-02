from django.shortcuts import get_object_or_404

from contributors.models import Repository
from contributors.views import contributors


class RepoContributorList(contributors.ListView):
    """A repository's details."""

    template_name = 'repository_details.html'

    def get_queryset(self):
        """Get a dataset."""
        self.repository = get_object_or_404(
            Repository, full_name=self.kwargs['slug'],
        )
        return self.repository.contributors.visible().with_contributions()

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)
        context['repository'] = self.repository
        return context
