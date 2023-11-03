from django.db.models import Prefetch
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
    """A list of issues."""

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

    contributionlabel_prefetch = Prefetch(
        'labels',
        queryset=ContributionLabel.objects.all(),
    )

    queryset = (
        Contribution.objects.filter(type='iss').
        select_related('repository', 'contributor', 'info').
        prefetch_related("repository__labels", contributionlabel_prefetch).
        distinct()
    )

    def get_context_data(self, *args, **kwargs):
        """Add context."""
        all_contribution_id = Contribution.objects.filter(
            type='iss'
        ).values_list('id', flat=True).distinct()
        all_contribution_labels = ContributionLabel.objects.filter(
            contribution__id__in=all_contribution_id,
        ).distinct()

        request_contribution_labels = self.request.GET.get(
            'contribution_labels',
        )

        if request_contribution_labels:
            contribution_labels = ContributionLabel.objects.exclude(
                name__in=request_contribution_labels.split('.'),
            ).distinct()
        else:
            contribution_labels = ContributionLabel.objects.filter(
                contribution__id__in=self.get_queryset(),
            ).distinct()

        context = super().get_context_data(**kwargs)
        context['all_contribution_labels'] = all_contribution_labels
        context['contribution_labels'] = contribution_labels
        return context
