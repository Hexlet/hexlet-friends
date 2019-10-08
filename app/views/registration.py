"""Registration view module."""
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from app.forms import RegistrationForm


class RegistrationView(CreateView):
    """User registration view."""

    template_name = 'auth/registration.html'
    success_url = reverse_lazy('contributors:home')
    model = User
    form_class = RegistrationForm
