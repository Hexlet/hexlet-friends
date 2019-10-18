from django.contrib import admin

from contributors.models import Contributor


class ContributorAdmin(admin.ModelAdmin):
    """Contributor representation."""

    fieldsets = (
        (None, {
            'fields': (
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
    list_display = ('id', 'login', 'name')
    search_fields = ('login', 'name')


admin.site.register(Contributor, ContributorAdmin)
