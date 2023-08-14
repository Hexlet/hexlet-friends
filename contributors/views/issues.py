from django_filters.views import FilterView

from contributors.models import Contribution, ContributionLabel
from contributors.views.filters import IssuesFilter
from contributors.views.mixins import (
    ContributionLabelsMixin,
    TableSortSearchAndPaginationMixin,
)


class ListView(
    ContributionLabelsMixin,
    TableSortSearchAndPaginationMixin,
    FilterView,
):
    """A list of opened issues."""

    queryset = Contribution.objects.filter(
        type='iss', info__state='open',
    ).distinct()
    template_name = 'open_issues.html'
    filterset_class = IssuesFilter
    sortable_fields = (  # noqa: WPS317
        'info__title',
        'repository__full_name',
        'repository__labels',
        'contributor__login',
        'created_at',
        'info__state',
    )
    searchable_fields = (
        'info__title',
        'repository__full_name',
        'repository__labels',
    )
    ordering = sortable_fields[0]

    def get_context_data(self, *args, **kwargs):
        """Add context."""
        all_contribution_id = Contribution.objects.filter(
            type='iss', info__state='open',
        ).values_list('id', flat=True).distinct()
        all_contribution_labels = ContributionLabel.objects.filter(
            contribution__id__in=all_contribution_id,
        ).distinct()

        contribution_labels = ContributionLabel.objects.filter(
            contribution__id__in=self.get_queryset(),
        ).distinct()

        context = super().get_context_data(**kwargs)
        context['all_contribution_labels'] = all_contribution_labels
        context['contribution_labels'] = contribution_labels
        return context
