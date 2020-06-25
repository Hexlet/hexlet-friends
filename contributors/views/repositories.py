from django.db.models import Count, Q  # noqa: WPS347
from django.utils.translation import gettext_lazy as _
from django.views import generic

from contributors.models import Repository
from contributors.views.mixins import TableControlsAndPaginationMixin


class ListView(TableControlsAndPaginationMixin, generic.ListView):
    """A list of repositories."""

    queryset = (
        Repository.objects.select_related('organization').filter(
            Q(contribution__contributor__is_visible=True)
            | Q(contributors__isnull=True),
            is_visible=True,
        ).annotate(
            pull_requests=Count(
                'contribution', filter=Q(contribution__type='pr'),
            ),
            issues=Count(
                'contribution', filter=Q(contribution__type='iss'),
            ),
            contributors_count=Count(
                'contribution__contributor', distinct=True,
            ),
        )
    )
    template_name = 'repositories_list.html'
    sortable_fields = (  # noqa: WPS317
        'name',
        ('organization__name', _("Organization")),
        ('project__name', _("Project")),
        'pull_requests',
        'issues',
        ('contributors_count', _("Contributors")),
    )
    searchable_fields = ('name', 'organization__name', 'project__name')
    ordering = sortable_fields[0]
