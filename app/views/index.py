from django.conf import settings

from django.views.generic.base import TemplateView


class IndexView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['APP_NAME'] = settings.APP_NAME
        return context
