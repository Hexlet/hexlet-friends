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
        if qs_param == 'labels':
            get_params.pop('page')
        if qs_param == 'contribution_labels':
            get_params.pop('page')
    with suppress(KeyError):
        get_params.pop(qs_param)
    get_params[qs_param] = (
        qs_param_value(previous_value)
        if callable(qs_param_value) else qs_param_value
    )
    return f'?{get_params.urlencode()}' if get_params else ''


@register.simple_tag(takes_context=True)
def get_sort_query_string(context, passed_sort_field):
    """Get table column query string."""
    def prepare_sort_param_value(ordering):
        ordering = ordering or context['view'].get_ordering()
        current_sort_field = split_ordering(ordering)[1]
        if passed_sort_field == current_sort_field:
            new_ordering = (
                ordering[1:] if ordering.startswith('-')
                else f'-{ordering}'
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


@register.simple_tag(takes_context=True)
def get_label_query_string(context, passed_label):
    """Get labels query string."""
    def prepare_labels_param_value(labels_param):
        delimiter = '.'
        labels = labels_param.split(delimiter) if labels_param else []
        if passed_label in labels:
            labels.remove(passed_label)
        else:
            labels.append(passed_label)
        return delimiter.join(labels)

    return get_query_string(context, 'labels', prepare_labels_param_value)


@register.simple_tag(takes_context=True)
def get_contribution_label_query_string(context, passed_label):
    """Get labels query string."""
    def prepare_contribution_labels_param_value(labels_param):
        delimiter = '.'
        labels = labels_param.split(delimiter) if labels_param else []
        if passed_label in labels:
            labels.remove(passed_label)
        else:
            labels.append(passed_label)
        return delimiter.join(labels)

    return get_query_string(
        context,
        'contribution_labels',
        prepare_contribution_labels_param_value,
    )


@register.simple_tag(takes_context=True)
def get_canonical_url(context):
    """Get canonical url from request."""
    request = context.get('request')
    if request:
        return request.build_absolute_uri(request.path)
    return ''


@register.simple_tag
def calc_percent_achievement(numerator, denominator):
    """Get contributor statistics and required quantity."""
    if numerator is not None:
        if numerator / denominator > 1:
            return 100.0
        return numerator / denominator * 100
    return 0
