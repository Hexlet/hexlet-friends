from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin

from auth.forms import UserChangeForm, UserCreationForm
from auth.models import SiteUser
from auth.models import GroupUser
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
