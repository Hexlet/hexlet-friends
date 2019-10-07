from django.contrib import admin

from app.models import Contribution, Repository


class ContributionInline(admin.TabularInline):
    """Contributions of repository."""

    model = Contribution
    extra = 0


class RepositoryAdmin(admin.ModelAdmin):
    """Repository representation."""

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'full_name',
                'html_url',
                'organization',
            ),
        }),
    )
    inlines = (ContributionInline,)
    list_display = ('id', 'name', 'organization')
    list_filter = ('organization',)
    search_fields = ('name',)


admin.site.register(Repository, RepositoryAdmin)
