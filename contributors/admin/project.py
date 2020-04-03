
from contributors.admin import base
from contributors.admin.custom import site
from contributors.models import Project


class ProjectAdmin(base.ModelAdmin):
    """Project representation."""

    fieldsets = (
        (None, {
            'fields': (
                'is_visible',
                'full_name',
                'description',
                'html_url',
            ),
        }),
    )

    list_display = ('id', 'full_name', 'is_visible',)
    search_fields = ('full_name',)
    actions = ['change_visibility',]


site.register(Project, ProjectAdmin)
