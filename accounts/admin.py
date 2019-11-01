from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import SiteUserChangeForm, SiteUserCreationForm
from accounts.models import SiteUser


class SiteUserAdmin(UserAdmin):
    """Site user representation."""

    model = SiteUser
    add_form = SiteUserCreationForm
    form = SiteUserChangeForm


admin.site.register(SiteUser, SiteUserAdmin)
