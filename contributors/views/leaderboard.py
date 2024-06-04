from django.views import generic

from contributors.models import Contributor
from contributors.views.mixins import (
    LeaderboardQueryMixin,
    TableSortSearchAndPaginationMixin,
)


class LeaderboardGenericListView(
    LeaderboardQueryMixin,
    TableSortSearchAndPaginationMixin,
    generic.ListView,
):
    """Generic view for inheritance."""

    queryset = Contributor.objects.visible().with_contributions()

    searchable_fields = ('login', 'name')
    paginate_by = 100


class CommitsListView(LeaderboardGenericListView):
    """List of leaders among contributors by commits."""

    template_name = (
        'contributors_sections/leaderboard/leaderboard_commits.html'
    )
    sortable_fields = (
        '-commits',
        'login',
        'name',
    )
    ordering = sortable_fields[0]


class IssuesListView(LeaderboardGenericListView):
    """List of leaders among contributors by issues."""

    template_name = 'contributors_sections/leaderboard/leaderboard_issues.html'
    sortable_fields = (
        '-issues',
        'login',
        'name',
    )
    ordering = sortable_fields[0]


class PrsListView(LeaderboardGenericListView):
    """List of leaders among contributors by pull requests."""

    template_name = 'contributors_sections/leaderboard/leaderboard_prs.html'
    sortable_fields = (
        '-pull_requests',
        'login',
        'name',
    )
    ordering = sortable_fields[0]
