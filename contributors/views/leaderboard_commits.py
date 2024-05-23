from django.views import generic

from contributors.models import Contributor
from contributors.views.mixins import (
    LeaderboardQueryMixin,
    TableSortSearchAndPaginationMixin,
)


class ListView(
    LeaderboardQueryMixin,
    TableSortSearchAndPaginationMixin,
    generic.ListView,
):
    """List of leaders among contributors by commits."""

    queryset = Contributor.objects.visible().with_contributions()
    template_name = 'leaderboard_commits.html'
    sortable_fields = (
        '-commits',
        'login',
        'name',
    )
    searchable_fields = ('login', 'name')
    ordering = sortable_fields[0]
    paginate_by = 100
