from contextlib import suppress
from functools import reduce
from operator import __or__

from django.core.paginator import Paginator
from django.db.models import F, Q, Window  # noqa: WPS347
from django.db.models.functions import RowNumber
from django.views.generic.list import MultipleObjectMixin
from django_cte import With

from contributors.forms import ListSortAndSearchForm

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

    def get_adjusted_queryset(self):
        """Return a sorted and filtered QuerySet."""
        self.ordering = self.request.GET.get('sort', self.get_ordering())
        filter_value = self.request.GET.get('search', '').strip()
        lookups = {}
        for field in self.searchable_fields:
            key = '{0}__icontains'.format(field)
            lookups[key] = filter_value
        expressions = [
            Q(**{key: value})
            for key, value in lookups.items()  # noqa: WPS110
        ]
        direction = 'desc' if self.request.GET.get('descending') else 'asc'
        ordering = getattr(F(self.get_ordering()), direction)

        # Can be simplified when filtering on windows gets implemented
        # https://code.djangoproject.com/ticket/28333
        queryset = self.get_queryset().order_by(ordering())
        ids_nums = With(queryset.annotate(
            num=Window(RowNumber(), order_by=ordering()),
        ).values('id', 'num'),
        )
        return ids_nums.join(
            queryset, id=ids_nums.col.id,
        ).with_cte(ids_nums).annotate(num=ids_nums.col.num).filter(
            reduce(__or__, expressions),
        )

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.get_adjusted_queryset(), self.paginate_by)
        page = paginator.get_page(self.request.GET.get('page'))

        page_slice = get_page_slice(
            page.number,
            paginator.num_pages,
            self.max_pages_without_shrinking,
            self.pages_visible_at_boundary,
            self.inner_visible_pages,
        )

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


class TableControlsMixin(object):
    """A mixin for table controls."""

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        form = ListSortAndSearchForm(self.sortable_fields, self.request.GET)
        get_params = self.request.GET.copy()
        with suppress(KeyError):
            get_params.pop('page')

        context['form'] = form
        context['get_params'] = (
            '&{0}'.format(get_params.urlencode()) if get_params else ''
        )
        return context


class TableControlsAndPaginationMixin(TableControlsMixin, PaginationMixin):
    """Combine mixins for table controls and pagination."""
