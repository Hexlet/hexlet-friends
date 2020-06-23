from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from django.views import generic

from contributors.models import Organization
from contributors.utils.mixins import FilteringAndPaginationMixin


class ListView(FilteringAndPaginationMixin, generic.ListView):
    """A list of organizations."""

    queryset = Organization.objects.filter(
        repository__is_visible=True,
    ).annotate(repository_count=Count('repository'))
    template_name = 'organizations_list.html'
    sortable_fields = (
        'name',
        ('repository_count', _("Repositories")),
    )
    searchable_fields = ('name',)
    ordering = sortable_fields[0]
