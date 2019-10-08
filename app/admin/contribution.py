from django.contrib import admin

from app.models import Contribution


class ContributionAdmin(admin.ModelAdmin):
    """Contribution representation."""

    list_display = (
        'id',
        'repository',
        'contributor',
        'commits',
        'additions',
        'deletions',
        'pull_requests',
        'issues',
        'comments',
    )
    list_filter = ('repository__organization', 'repository', 'contributor')


admin.site.register(Contribution, ContributionAdmin)
