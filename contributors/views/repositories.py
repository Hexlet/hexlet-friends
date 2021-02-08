from django.db.models import Count, Q  # noqa: WPS347
from django.utils.translation import gettext_lazy as _
from django.views import generic

from contributors.models import Repository
from contributors.views.mixins import TableControlsAndPaginationMixin


class ListView(TableControlsAndPaginationMixin, generic.ListView):
    """A list of repositories."""

    for_visible_contributor = Q(contribution__contributor__is_visible=True)
    queryset = (
        Repository.objects.select_related('organization').filter(
            is_visible=True,
        ).distinct().annotate(
            pull_requests=Count(
                'contribution',
                filter=Q(contribution__type='pr') & for_visible_contributor,
            ),
            issues=Count(
                'contribution',
                filter=Q(contribution__type='iss') & for_visible_contributor,
            ),
            contributors_count=Count(
                'contribution__contributor',
                filter=for_visible_contributor,
                distinct=True,
            ),
        )
    )
    template_name = 'repositories_list.html'
    sortable_fields = (  # noqa: WPS317
        'name',
        'organization',
        'project',
        'pull_requests',
        'issues',
        ('contributors_count', _("Contributors")),
    )
    searchable_fields = ('name', 'organization__name', 'project__name')
    ordering = sortable_fields[0]
