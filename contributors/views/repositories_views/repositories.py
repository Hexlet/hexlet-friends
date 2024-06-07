from django.db.models import Count, Q  # noqa: WPS347
from django.utils.translation import gettext_lazy as _
from django.views import generic

from contributors.models import Label, Repository
from contributors.views.mixins import (
    LabelsMixin,
    TableSortSearchAndPaginationMixin,
)


class ListView(
    LabelsMixin,
    TableSortSearchAndPaginationMixin,
    generic.ListView,
):
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
    template_name = 'contributors_sections/repositories/repositories_list.html'
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

    def get_context_data(self, **kwargs):
        """Add context."""
        all_labels = Label.objects.all()
        labels = Label.objects.filter(
            repository__id__in=self.get_queryset(),
        ).distinct()

        context = super().get_context_data(**kwargs)
        context['all_labels'] = all_labels
        context['labels'] = labels

        return context
