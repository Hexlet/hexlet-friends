from django.views import generic

from contributors.models import Contributor, IssueInfo
from contributors.views.mixins import TableSortSearchAndPaginationMixin


class ListView(TableSortSearchAndPaginationMixin, generic.ListView):
    """A list of issues of a contributor."""

    template_name = 'contributor_issues.html'
    sortable_fields = (
        'title',
        'is_open',
    )
    searchable_fields = ('title',)
    ordering = sortable_fields[0]

    def get_queryset(self):
        """Get issues from contributions.

        Returns:
            Queryset.
        """
        contributor = Contributor.objects.get(login=self.kwargs.get('slug'))
        return IssueInfo.objects.filter(
            issue__type='iss',
            issue__contributor=contributor,
        )
