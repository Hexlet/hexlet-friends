from django.contrib import admin

from contributors.admin.custom import site
from contributors.models import CommitStats, Contribution


class CommitStatsInline(admin.StackedInline):
    """Commit statistics."""

    model = CommitStats
    extra = 0


class ContributionAdmin(admin.ModelAdmin):
    """Contribution representation."""

    inlines = (CommitStatsInline,)
    list_display = (
        'id',
        'repository',
        'contributor',
        'type',
        'html_url',
        'created_at',
    )
    list_filter = (
        'repository__organization', 'repository', 'contributor', 'type',
    )


site.register(Contribution, ContributionAdmin)
