from django.views.generic.base import TemplateView


class LandingView(TemplateView):
    """Landing page."""

    template_name = 'landing/landing.html'
