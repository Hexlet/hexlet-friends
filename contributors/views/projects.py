from django.views import generic
from django.utils.translation import gettext_lazy as _

from contributors.models import Project
from contributors.views.mixins import TableSortSearchAndPaginationMixin


class ListView(TableSortSearchAndPaginationMixin, generic.ListView):
    """A view for a list of projects."""

    queryset = Project.objects.all()

    template_name = 'projects_list.html'
    context_object_name = 'projects_list'
    sortable_fields = (  # noqa: WPS317
        'name',
        'URL',
        'description',
        'pull_requests',
        'issues',
        ('contributors_count', _("Contributors")),
    )
    ordering = sortable_fields[0]
    searchable_fields = ('name',)
