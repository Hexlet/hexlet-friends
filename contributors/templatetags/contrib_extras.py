from contextlib import suppress
from types import MappingProxyType

from django import template
from django.conf import settings

from contributors.utils.misc import DIRECTION_TRANSLATIONS, split_ordering

register = template.Library()


@register.filter
def get(object_, attr):
    """Return an object's attribute value."""
    return getattr(object_, attr, '')


@register.simple_tag(takes_context=True)
def get_ordering_direction(context, passed_field_name):
    """Get ordering direction for the field name."""
    view = context['view']
    direction, field_name = split_ordering(view.get_ordering())
    if passed_field_name == field_name:
        return DIRECTION_TRANSLATIONS[direction]
    return ''


@register.simple_tag(takes_context=True)
def get_table_column_query_string(context, passed_field_name):
    """Get table column query string."""
    view = context['view']
    get_params = view.request.GET.copy()
    ordering = view.get_ordering()
    if ordering:
        _, field_name = split_ordering(ordering)
        if passed_field_name == field_name:
            new_ordering = (
                ordering[1:] if ordering.startswith('-')
                else '-{0}'.format(ordering)
            )
        elif passed_field_name in settings.TEXT_COLUMNS:
            new_ordering = passed_field_name
        else:
            new_ordering = ''.join(('-', passed_field_name))
        with suppress(KeyError):
            get_params.pop('sort')
        get_params['sort'] = new_ordering
    return '?{0}'.format(get_params.urlencode()) if get_params else ''


@register.simple_tag(takes_context=True)
def get_pagination_query_string(context, page_num):
    """Get pagination query string."""
    view = context['view']
    get_params = view.request.GET.copy()
    with suppress(KeyError):
        get_params.pop('page')
    get_params['page'] = page_num
    return '?{0}'.format(get_params.urlencode()) if get_params else ''
