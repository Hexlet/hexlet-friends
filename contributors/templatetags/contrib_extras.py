from contextlib import suppress

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


def get_query_string(context, qs_param, qs_param_value):
    """Get query string."""
    view = context['view']
    get_params = view.request.GET.copy()
    previous_value = get_params.get(qs_param)
    with suppress(KeyError):
        get_params.pop(qs_param)
    get_params[qs_param] = (
        qs_param_value(previous_value)
        if callable(qs_param_value) else qs_param_value
    )
    return '?{0}'.format(get_params.urlencode()) if get_params else ''


@register.simple_tag(takes_context=True)
def get_sort_query_string(context, passed_sort_field):
    """Get table column query string."""
    def prepare_sort_param_value(ordering):  # noqa: WPS430
        ordering = ordering or context['view'].get_ordering()
        current_sort_field = split_ordering(ordering)[1]
        if passed_sort_field == current_sort_field:
            new_ordering = (
                ordering[1:] if ordering.startswith('-')
                else '-{0}'.format(ordering)
            )
        elif passed_sort_field in settings.TEXT_COLUMNS:
            new_ordering = passed_sort_field
        else:
            new_ordering = ''.join(('-', passed_sort_field))
        return new_ordering

    return get_query_string(context, 'sort', prepare_sort_param_value)


@register.simple_tag(takes_context=True)
def get_pagination_query_string(context, page_num):
    """Get pagination query string."""
    return get_query_string(context, 'page', page_num)
