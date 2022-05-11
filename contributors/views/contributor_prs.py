from django.views import generic

from contributors.models import Contribution
from contributors.views.mixins import TableSortSearchAndPaginationMixin


class ListView(TableSortSearchAndPaginationMixin, generic.ListView):
    """A list of pull requests of a contributor."""

    template_name = 'contributor_prs.html'
    sortable_fields = (
        'info__title',
    )
    searchable_fields = ('info__title',)
    ordering = sortable_fields[0]

    def get_queryset(self):
        """Get pull requests from contributions.

        Returns:
            Queryset.
        """
        self.queryset = Contribution.objects.select_related('info').filter(
            contributor__login=self.kwargs['slug'], type='pr',
        )
        return super().get_queryset()
