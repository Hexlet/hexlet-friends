from django.contrib import admin

from contributors.admin.custom import site
from contributors.models import Organization, Repository


class RepositoryInline(admin.TabularInline):
    """Repositories of organization."""

    model = Repository
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    """Organization representation."""

    inlines = (RepositoryInline,)
    list_display = ('id', 'name', 'is_tracked')
    search_fields = ('name',)


site.register(Organization, OrganizationAdmin)
