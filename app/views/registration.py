from django.views.generic.base import TemplateView

from app.forms.registration import RegistrationForm
from app.views.index import BaseView


class RegistrationView(TemplateView):

    template_name = 'auth/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegistrationForm()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
