from django.db.models import Count, Prefetch, Q
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.cache import cache_page

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

    @method_decorator(cache_page(60 * 15))  # кэширование на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = (
            Repository.objects.select_related("organization", "project")
            .filter(
                is_visible=True,
            )
            .distinct()
            .annotate(
                pull_requests=Count(
                    "contribution",
                    filter=Q(contribution__type="pr") & self.for_visible_contributor,
                ),
                issues=Count(
                    "contribution",
                    filter=Q(contribution__type="iss") & self.for_visible_contributor,
                ),
                contributors_count=Count(
                    "contribution__contributor",
                    filter=self.for_visible_contributor,
                    distinct=True,
                ),
            )
            .prefetch_related(Prefetch("labels", queryset=Label.objects.only("name")))
        )

        filtered_labels = self.request.GET.get('labels')
        if filtered_labels:
            queryset = queryset.filter(
                labels__name__lower__in=filtered_labels.split('.'))
        return queryset

    template_name = "contributors_sections/repositories/repositories_list.html"
    sortable_fields = (
        "name",
        "organization",
        "project",
        "pull_requests",
        "issues",
        ("contributors_count", _("Contributors")),
    )
    searchable_fields = ("name", "organization__name", "project__name")
    ordering = sortable_fields[0]

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        all_labels = Label.objects.only("name")
        labels = (
            Label.objects.filter(
                repository__in=self.get_queryset(),
            )
            .distinct()
            .only("name")
        )

        filtered_labels = self.request.GET.get('labels')
        if filtered_labels:
            labels = labels.filter(name__lower__in=filtered_labels.split('.'))

        context['all_labels'] = all_labels
        context['labels'] = labels

        return context
