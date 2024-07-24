from dateutil import relativedelta
from django.db import models
from django.db.models.functions import ExtractMonth
from django.utils import timezone

from contributors.models import Contribution, Project
from contributors.utils import misc
from contributors.views.repositories_views import repositories


class ProjectRepositoryList(repositories.ListView):
    """A project's details."""

    template_name = 'project_details.html'

    def get_queryset(self):
        """Get a dataset."""
        self.project = Project.objects.get(pk=self.kwargs['pk'])
        return super().get_queryset().filter(project=self.project)

    def extract_contributions_for_project(self, project):
        """Return yearly results."""
        datetime_now = timezone.now()
        date_eleven_months_ago = (datetime_now - relativedelta.relativedelta(
            months=11, day=1,
        )).date()

        months_with_contrib_sums = Contribution.objects.filter(
            repository__is_visible=True,
            contributor__is_visible=True,
            created_at__gte=date_eleven_months_ago,
            repository__project=project,
        ).annotate(
            month=ExtractMonth('created_at'),
        ).values('month', 'type').annotate(count=models.Count('id'))

        sums_of_contribs_by_months = misc.group_contribs_by_months(
            months_with_contrib_sums,
        )

        return misc.get_contrib_sums_distributed_over_months(
            datetime_now.month,
            sums_of_contribs_by_months,
        )

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        context['project'] = self.project
        context['contributions_for_year'] = (
            self.extract_contributions_for_project(self.project)
        )

        return context
