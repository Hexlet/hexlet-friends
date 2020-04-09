
from contributors.admin import base
from contributors.admin.custom import site
from contributors.models import Project


class ProjectAdmin(base.ModelAdmin):
    """Project representation."""

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'html_url',
            ),
        }),
    )

    list_display = ('id', 'name')
    search_fields = ('name',)


site.register(Project, ProjectAdmin)
