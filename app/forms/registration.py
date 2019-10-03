"""Registration form."""
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    """Registration form class."""
    email = forms.EmailField(
        label='E-mail',
        max_length=20,
        help_text=_('Enter your e-mail address')
    )

    class Meta:
        """Form meta."""
        model = User
        fields = ('email', 'username')
