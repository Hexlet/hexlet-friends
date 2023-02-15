from django.utils.translation import gettext_lazy as _
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
    """A list of repositories."""

    queryset = Contribution.objects.filter(type='iss', info__state='open')
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
        all_contribution_id = Contribution.objects.filter(type='iss', info__state='open').values_list('id', flat=True)
        all_contribution_labels = ContributionLabel.objects.filter(
            contribution__id__in=all_contribution_id,
        ).distinct()
        chosen_labels = self.request.GET.get('contribution_labels')
        if chosen_labels:
            list_of_labels = chosen_labels.split('.')
            contribution_labels = ContributionLabel.objects.filter(
                name__in=list_of_labels,
            ).distinct()
        else:
            contribution_labels = all_contribution_labels
        context = super().get_context_data(**kwargs)
        context['all_contribution_labels'] = all_contribution_labels
        context['contribution_labels'] = contribution_labels
        return context
