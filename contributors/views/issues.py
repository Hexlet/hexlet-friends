from django.views import generic

from contributors.models import Contribution, ContributionLabel
from contributors.views.mixins import (
    ContributionLabelsMixin,
    TableSortSearchAndPaginationMixin,
)


class ListView(
    ContributionLabelsMixin,
    TableSortSearchAndPaginationMixin,
    generic.ListView,
):
    """A list of opened issues."""

    queryset = Contribution.objects.filter(
        type='iss', info__state='open',
    ).distinct()
    template_name = 'open_issues.html'
    sortable_fields = (  # noqa: WPS317
        'info__title',
        'repository__full_name',
        'repository__labels',
        'contributor__login',
        'created_at',
        'labels',
    )
    searchable_fields = (
        'info__title',
        'repository__full_name',
        'repository__labels',
        'contributor__login',
        'created_at',
        'labels',
    )

    ordering = sortable_fields[1]

    def get_context_data(self, **kwargs):
        """Add context."""
        all_contribution_id = Contribution.objects.filter(
            type='iss', info__state='open',
        ).values_list('id', flat=True).distinct()
        all_contribution_labels = ContributionLabel.objects.filter(
            contribution__id__in=all_contribution_id,
        ).distinct()
        if self.request.GET.get('contribution_labels'):
            contribution_labels_names = self.request.GET.get(
                'contribution_labels',
            ).split('.')
            contribution_labels = all_contribution_labels.filter(
                name__in=contribution_labels_names,
            ).distinct()
        else:
            contribution_labels = all_contribution_labels
        # here I ve got some dublicates. What is wrong?
        context = super().get_context_data(**kwargs)
        context['all_contribution_labels'] = all_contribution_labels
        context['contribution_labels'] = contribution_labels
        return context
