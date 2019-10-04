"""Index page views."""

from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    """Index page view."""

    template_name = 'index.html'
