from django import forms as django_forms
from django.contrib.auth import forms

from auth.models import SiteUser


class UserCreationForm(forms.UserCreationForm):
    """Site user creation form."""

    class Meta(forms.UserCreationForm.Meta):
        model = SiteUser
        fields = ('username', 'email')


class UserChangeForm(forms.UserChangeForm):
    """Site user change form."""

    class Meta(forms.UserChangeForm.Meta):
        model = SiteUser
        fields = ('username', 'email')


class UserTokenForm(django_forms.ModelForm):
    """User GitHub token change form."""

    class Meta:
        model = SiteUser
        fields = ['github_token']
