from contributors.admin import base
from contributors.admin.custom import site
from contributors.models import Contributor


class ContributorAdmin(base.ModelAdmin):
    """Contributor representation."""

    fieldsets = (
        (None, {
            'fields': (
                'is_tracked',
                'is_visible',
                'login',
            ),
        }),
        ('Additional info', {
            'fields': (
                'name',
                'html_url',
                'avatar_url',
            ),
        }),
    )
    list_display = ('id', 'login', 'name', 'is_tracked', 'is_visible')
    search_fields = ('login', 'name')
    actions = ['change_tracking', 'change_visibility']


site.register(Contributor, ContributorAdmin)
