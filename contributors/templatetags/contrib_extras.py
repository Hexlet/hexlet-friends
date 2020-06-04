from django import template

register = template.Library()


def get(object_, attr):
    """Return an object's attribute value."""
    return getattr(object_, attr, '')


register.filter('get', get)
