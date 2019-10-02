"""Registration form."""
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegistrationForm(forms.Form):
    """Registration form class."""
    email = forms.EmailField(
        label=_('E-mail'),
        max_length=20)
    username = forms.CharField(
        label=_('Username'),
        max_length=20)
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(),
        min_length=4)
    password_confirmation = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(),
        min_length=4)

    class Meta:
        """Form meta."""
        model = User
