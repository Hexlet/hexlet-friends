from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    """Home page view."""

    template_name = 'home.html'
