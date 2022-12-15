from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from auth.forms import UserChangeForm, UserCreationForm
from auth.models import GroupUser, SiteUser
from contributors.admin.custom import site


class SiteUserAdmin(UserAdmin):
    """Site user representation."""

    model = SiteUser
    add_form = UserCreationForm
    form = UserChangeForm
    filter_horizontal = ('groups', )


class GroupUserAdmin(ModelAdmin):
    """Site user representation."""

    filter_horizontal = ('users', )


site.register(SiteUser, SiteUserAdmin)
site.register(GroupUser, GroupUserAdmin)
