from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from django.views import generic

from contributors.models import Project
from contributors.views.mixins import TableSortSearchAndPaginationMixin


class ListView(TableSortSearchAndPaginationMixin, generic.ListView):
    """A view for a list of projects."""

    queryset = Project.objects.prefetch_related(
        'repository_set__contribution_set',
    ).annotate(
        pull_requests=Count(
            'repository__contribution__id',
            filter=Q(
                repository__contribution__type='pr',
                repository__contribution__repository__is_visible=True,
                repository__contribution__contributor__is_visible=True,
            ),
        ),
        issues=Count(
            'repository__contribution__id',
            filter=Q(
                repository__contribution__type='iss',
                repository__contribution__repository__is_visible=True,
                repository__contribution__contributor__is_visible=True,
            ),
        ),
        commits=Count(
            'repository__contribution__id',
            filter=Q(
                repository__contribution__type='cit',
                repository__contribution__repository__is_visible=True,
                repository__contribution__contributor__is_visible=True,
            ),
        ),
        comments=Count(
            'repository__contribution__id',
            filter=Q(
                repository__contribution__type='cnt',
                repository__contribution__repository__is_visible=True,
                repository__contribution__contributor__is_visible=True,
            ),
        ),
        contributors_count=Count(
            'repository__contribution__contributor',
            distinct=True,
        ),
    )

    template_name = 'projects_list.html'
    context_object_name = 'projects_list'
    sortable_fields = (
        'name',
        'html_url',
        'description',
        'pull_requests',
        'issues',
        'commits',
        'comments',
        ('contributors_count', _("Contributors")),
    )
    ordering = sortable_fields[0]
    searchable_fields = ('name',)
