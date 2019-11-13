from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from auth.forms import UserCreationForm


class RegistrationView(CreateView):
    """User registration view."""

    form_class = UserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('contributors:home')
