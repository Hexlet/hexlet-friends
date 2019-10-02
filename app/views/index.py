"""Index page views."""
from django.conf import settings
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    """Index page view."""

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """Provide view page context."""
        context = super().get_context_data(**kwargs)
        context['APP_NAME'] = settings.APP_NAME
        return context
