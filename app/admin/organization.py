from django.contrib import admin

from app.models import Organization, Repository


class RepositoryInline(admin.TabularInline):
    """Repositories of organization."""

    model = Repository
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    """Organization representation."""

    inlines = (RepositoryInline,)
    list_display = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Organization, OrganizationAdmin)
