from django.db.models import Count, Q  # noqa: WPS347
from django.views import generic

from contributors.models import Project, Repository


class DetailView(generic.DetailView):
    """Project's details."""

    model = Project
    template_name = 'project_details.html'

    def get_context_data(self, **kwargs):
        """Add additional context for the project."""
        context = super().get_context_data(**kwargs)

        repositories = Repository.objects.filter(
            project__pk=self.object.pk,
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
        ).order_by('full_name')

        context['repositories_list'] = repositories

        return context
