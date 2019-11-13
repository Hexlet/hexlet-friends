from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth.forms import UserChangeForm, UserCreationForm
from auth.models import SiteUser


class SiteUserAdmin(UserAdmin):
    """Site user representation."""

    model = SiteUser
    add_form = UserCreationForm
    form = UserChangeForm


admin.site.register(SiteUser, SiteUserAdmin)
