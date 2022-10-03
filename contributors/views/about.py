from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    """About project page view."""

    template_name = 'about.html'
