import operator
from functools import reduce

from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Sum, Window  # noqa: WPS347
from django.db.models.functions import Coalesce, RowNumber
from django.views.generic.list import MultipleObjectMixin
from django_cte import With

from contributors.forms import TableSortSearchForm
from contributors.utils.misc import DIRECTION_TRANSLATIONS, split_ordering

MAX_PAGES_WITHOUT_SHRINKING = 8
PAGES_VISIBLE_AT_BOUNDARY = 5
INNER_VISIBLE_PAGES = 3


def get_page_slice(
    current_page,
    num_pages,
    max_pages_without_shrinking=MAX_PAGES_WITHOUT_SHRINKING,
    pages_visible_at_boundary=PAGES_VISIBLE_AT_BOUNDARY,
    inner_visible_pages=INNER_VISIBLE_PAGES,
):
    """
    Return a range of page numbers to display.

    If the number of pages is less than MAX, return all.
    Else the first or last pages WITHIN LIMIT are returned when the current
    page is among the limit - 1. Some INNER pages are returned in other cases.
    """
    if num_pages <= max_pages_without_shrinking:
        return slice(0, num_pages)
    if current_page < pages_visible_at_boundary:
        start_index = 0
        end_index = pages_visible_at_boundary
    elif current_page <= num_pages - pages_visible_at_boundary + 1:
        current_page_index = current_page - 1
        start_index = current_page_index - inner_visible_pages // 2
        end_index = start_index + inner_visible_pages
    else:
        start_index = num_pages - pages_visible_at_boundary
        end_index = num_pages
    return slice(start_index, end_index)


class PaginationMixin(MultipleObjectMixin):
    """A mixin for pagination."""

    paginate_by = 25
    max_pages_without_shrinking = MAX_PAGES_WITHOUT_SHRINKING
    pages_visible_at_boundary = PAGES_VISIBLE_AT_BOUNDARY
    inner_visible_pages = INNER_VISIBLE_PAGES

    def get_context_data(self, **kwargs):
        """Add context."""
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = paginator.get_page(self.request.GET.get('page'))

        page_slice = get_page_slice(
            page.number,
            paginator.num_pages,
            self.max_pages_without_shrinking,
            self.pages_visible_at_boundary,
            self.inner_visible_pages,
        )

        context = super().get_context_data(**kwargs)
        context.update({
            'page': page,
            'page_range': paginator.page_range[page_slice],
            'first_boundary_last_page': self.pages_visible_at_boundary,
            'last_boundary_first_page': (
                paginator.num_pages - self.pages_visible_at_boundary + 1
            ),
            'max_pages_without_shrinking': self.max_pages_without_shrinking,
        })

        return context


class TableSortSearchMixin(MultipleObjectMixin):
    """A mixin for table sort and search."""

    def set_ordering(self, ordering=None):  # noqa: WPS615
        """Set ordering."""
        sortable_fields = []
        for field in self.sortable_fields:
            if isinstance(field, str):
                sortable_fields.append(field)
            elif isinstance(field, (list, tuple)):
                sortable_fields.append(field[0])
            else:
                raise TypeError("Unknown item type")
        if ordering is None:
            self.ordering = sortable_fields[0]
            return
        direction, field_name = split_ordering(ordering)
        if field_name not in sortable_fields:
            self.ordering = sortable_fields[0]
            return
        self.ordering = ''.join((direction, field_name))

    def get_queryset(self):  # noqa: WPS210
        """Return an ordered and filtered QuerySet."""
        self.set_ordering(self.request.GET.get('sort'))
        direction, field_name = split_ordering(self.get_ordering())
        ordering = getattr(
            F(field_name),
            DIRECTION_TRANSLATIONS[direction],
        )
        # Can be simplified when filtering on windows gets implemented
        # https://code.djangoproject.com/ticket/28333
        queryset = self.queryset.order_by(ordering())
        ids_nums = With(
            queryset.annotate(
                num=Window(RowNumber(), order_by=ordering()),
            ).values('id', 'num'),
        )
        numbered_queryset = ids_nums.join(
            queryset, id=ids_nums.col.id,
        ).with_cte(ids_nums).annotate(num=ids_nums.col.num)

        filter_value = self.request.GET.get('search', '').strip()
        lookups = {}
        for field in self.searchable_fields:
            key = '{0}__icontains'.format(field)
            lookups[key] = filter_value
        expressions = [
            Q(**{key: value})
            for key, value in lookups.items()  # noqa: WPS110
        ]
        if filter_value:
            return numbered_queryset.filter(reduce(operator.or_, expressions))
        return numbered_queryset

    def get_context_data(self, **kwargs):
        """Add context."""
        form = TableSortSearchForm(self.request.GET)

        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context


class TableSortSearchAndPaginationMixin(TableSortSearchMixin, PaginationMixin):
    """A mixin for table sort, search and pagination."""


class LabelsMixin(object):
    """A mixin for labels."""

    def get_queryset(self):  # noqa: WPS615
        """Get a dataset."""
        labels_param = self.request.GET.get('labels')
        if labels_param:
            for label in labels_param.split('.'):
                self.queryset = self.queryset.filter(
                    labels__name__iexact=label,
                )
        return super().get_queryset()


class ContributorTotalStatMixin(object):
    """Add total stat to contributor context."""

    def get_context_data(self, **kwargs):
        """Get and modify context data."""
        context = super().get_context_data(**kwargs)
        context['total'] = self.object.contribution_set.aggregate(
            commits=Count('id', filter=Q(type='cit')),
            additions=Coalesce(Sum('stats__additions'), 0),
            deletions=Coalesce(Sum('stats__deletions'), 0),
            pull_requests=Count('type', filter=Q(type='pr')),
            issues=Count('type', filter=Q(type='iss')),
            comments=Count('type', filter=Q(type='cnt')),
        )
        return context


class ContributorsJsonMixin(object):
    """Add json-formatted list of contributors stats."""

    def get_context_data(self, **kwargs):
        """Get and modify context data."""
        context = super().get_context_data(**kwargs)
        context['contributors_json'] = list(
            self.model.objects.visible().with_contributions().values(
                'id',
                'commits',
                'additions',
                'deletions',
                'pull_requests',
                'issues',
                'comments',
            ),
        )
        return context
