from django.views import generic

from contributors.models import Contributor
from contributors.views.mixins import TableControlsAndPaginationMixin


class ListView(TableControlsAndPaginationMixin, generic.ListView):
    """A list of contributors with contributions."""

    queryset = Contributor.objects.visible().with_contributions()
    template_name = 'contributors_list.html'
    sortable_fields = (
        'login',
        'name',
        'commits',
        'additions',
        'deletions',
        'pull_requests',
        'issues',
        'comments',
    )
    searchable_fields = ('login', 'name')
    ordering = sortable_fields[0]
