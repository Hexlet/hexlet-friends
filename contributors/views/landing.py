from django.views.generic.base import TemplateView

from contributors.models import Contribution, Contributor


class LandingView(TemplateView):

    template_name = 'landing/landing.html'
