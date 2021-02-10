from contributors.models import Repository
from contributors.views import contributors


class RepoContributorList(contributors.ListView):
    """A repository's details."""

    template_name = 'repository_details.html'

    def get_queryset(self):
        """Get a dataset."""
        self.repository = Repository.objects.get(pk=self.kwargs['pk'])
        self.queryset = (
            self.repository.contributors.visible().with_contributions()
        )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)
        context['repository'] = self.repository
        return context
