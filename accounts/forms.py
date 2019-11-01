from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from accounts.models import SiteUser


class SiteUserCreationForm(UserCreationForm):
    """Site user creation form."""

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ('username', 'email')


class SiteUserChangeForm(UserChangeForm):
    """Site user change form."""

    class Meta(UserChangeForm.Meta):
        model = SiteUser
        fields = ('username', 'email')
