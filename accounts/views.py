from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from accounts.forms import SiteUserCreationForm


class RegistrationView(CreateView):
    """User registration view."""

    form_class = SiteUserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('contributors:home')
