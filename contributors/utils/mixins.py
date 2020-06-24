from contextlib import suppress
from functools import reduce
from operator import __or__

from django.core.paginator import Paginator
from django.db.models import Q  # noqa: WPS347
from django.views.generic.list import MultipleObjectMixin

from contributors.forms import ListSortAndSearchForm


def get_page_range(page_obj):
    """
    Return a range of page numbers to display.

    The first and last 5 pages are visible when the current page is among them.
    3 page numbers are displayed in other cases.
    """
    index = page_obj.number - 1
    max_index = page_obj.paginator.num_pages
    if index < 4:
        start_index = 0
        end_index = 5
    elif index <= max_index - 5:
        start_index = index - 1
        end_index = index + 2
    else:
        start_index = max_index - 5
        end_index = max_index
    return page_obj.paginator.page_range[start_index:end_index]


class PaginationMixin(MultipleObjectMixin):
    """A mixin for pagination."""

    paginate_by = 25

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.get_adjusted_queryset(), self.paginate_by)
        page_obj = paginator.get_page(self.request.GET.get('page'))

        context['page_obj'] = page_obj
        context['page_range'] = get_page_range(page_obj)
        return context


class TableControlsMixin(object):
    """A mixin for table controls."""

    def get_adjusted_queryset(self):
        """Return a sorted and filtered QuerySet."""
        self.ordering = self.request.GET.get('sort', self.get_ordering())
        filter_value = self.request.GET.get('search', '').strip()
        lookups = {}
        for field in self.searchable_fields:
            key = '{0}{1}'.format(field, '__icontains')
            lookups[key] = filter_value
        expressions = [Q(**{key: value}) for key, value in lookups.items()]  # noqa: WPS110,E501
        direction = '-' if self.request.GET.get('descending', False) else ''
        return self.get_queryset().filter(
            reduce(__or__, expressions),
        ).order_by('{0}{1}'.format(direction, self.get_ordering()))

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        form = ListSortAndSearchForm(self.sortable_fields, self.request.GET)
        get_params = self.request.GET.copy()
        with suppress(KeyError):
            get_params.pop('page')

        context['form'] = form
        context['get_params'] = get_params.urlencode()
        return context


class TableControlsAndPaginationMixin(TableControlsMixin, PaginationMixin):
    """Combine mixins for table controls and pagination."""
