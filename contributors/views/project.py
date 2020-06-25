from contributors.models import Project
from contributors.views import repositories


class ProjectRepositoryList(repositories.ListView):
    """A project's details."""

    template_name = 'project_details.html'

    def get_queryset(self):
        """Get a dataset."""
        self.project = Project.objects.get(pk=self.kwargs['pk'])
        return super().get_queryset().filter(project=self.project)

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        context['project'] = self.project
        return context
