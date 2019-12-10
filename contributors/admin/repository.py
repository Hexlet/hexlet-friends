
from django.contrib import admin

from contributors.admin import base
from contributors.admin.custom import site
from contributors.models import Contribution, Repository


class ContributionInline(admin.TabularInline):
    """Contributions of repository."""

    model = Contribution
    extra = 0


class RepositoryAdmin(base.ModelAdmin):
    """Repository representation."""

    fieldsets = (
        (None, {
            'fields': (
                'is_tracked',
                'is_visible',
                'name',
                'full_name',
                'html_url',
                'organization',
            ),
        }),
    )
    inlines = (ContributionInline,)
    list_display = ('id', 'name', 'organization', 'is_tracked', 'is_visible')
    list_filter = ('organization',)
    search_fields = ('name',)
    actions = ['change_tracking', 'change_visibility']


site.register(Repository, RepositoryAdmin)
