from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from django.views import generic

from contributors.models import Project
from contributors.views.mixins import TableSortSearchAndPaginationMixin


class ListView(TableSortSearchAndPaginationMixin, generic.ListView):
    """A view for a list of projects."""

    queryset = Project.objects.prefetch_related(
        'repository_set__contribution_set'
    ).annotate(
        pull_requests=Count(
            'repository__contribution__id',
            filter=Q(repository__contribution__type='pr')),
        issues=Count(
            'repository__contribution__id',
            filter=Q(repository__contribution__type='iss')),
        contributors_count=Count(
            'repository__contribution__contributor',
            distinct=True),
        )

    template_name = 'projects_list.html'
    context_object_name = 'projects_list'
    sortable_fields = (  # noqa: WPS317
        'name',
        'html_url',
        'description',
        'pull_requests',
        'issues',
        ('contributors_count', _("Contributors")),
    )
    ordering = sortable_fields[0]
    searchable_fields = ('name',)
