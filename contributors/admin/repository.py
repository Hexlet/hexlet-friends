from django.contrib import admin

from contributors.admin import base
from contributors.admin.custom import site
from contributors.models import Repository


class RepoLabelInline(admin.StackedInline):
    """Repository label."""

    model = Repository.labels.through
    extra = 1
    verbose_name = "relation"
    verbose_name_plural = "relations"


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
                'owner',
                'organization',
                'project',
            ),
        }),
    )
    list_display = (
        'id',
        'name',
        'owner',
        'organization',
        'project',
        'is_tracked',
        'is_visible',
    )
    list_filter = ('organization',)
    search_fields = ('name',)
    actions = ['change_tracking', 'change_visibility']
    inlines = (RepoLabelInline,)


site.register(Repository, RepositoryAdmin)
