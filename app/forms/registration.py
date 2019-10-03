"""Registration form."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    """Registration form class."""

    email = forms.EmailField(
        label='E-mail',
        help_text=_('Enter your e-mail address'),  # noqa: WPS121
    )

    class Meta:  # noqa WPS306
        """Form meta."""

        model = User
        fields = ('email', 'username')
