from types import MappingProxyType

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def get(object_, attr):
    """Return an object's attribute value."""
    return getattr(object_, attr, '')


@register.simple_tag(takes_context=True)
def get_ordering_direction(context, field_name):
    """Get ordering direction for the field name."""
    view = context['view']
    if field_name == view.get_ordering():
        return view.get_ordering_direction()
    return ''


OPPOSITE_DIRECTIONS = MappingProxyType({
    'asc': '-',
    'desc': '',
})


@register.simple_tag(takes_context=True)
def get_query_string(context, field_name):
    """Get query string."""
    view = context['view']
    page = context['page']
    current_direction = view.get_ordering_direction()
    if field_name == view.get_ordering():
        new_direction = OPPOSITE_DIRECTIONS[current_direction]
    elif field_name in settings.TEXT_COLUMNS:
        new_direction = ''
    else:
        new_direction = '-'
    search_value = view.request.GET.get('search')
    qs = '?page={number}&sort={direction}{field}'.format(
        number=page.number,
        direction=new_direction,
        field=field_name,
    )
    if search_value:
        return '{0}&search={1}'.format(qs, search_value)
    return qs
