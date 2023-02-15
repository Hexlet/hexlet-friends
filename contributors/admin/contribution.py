from django.contrib import admin

from contributors.admin.custom import site
from contributors.models import CommitStats, Contribution, IssueInfo


class CommitStatsInline(admin.StackedInline):
    """Commit statistics."""

    model = CommitStats
    extra = 0


class ContributionLabelInline(admin.StackedInline):
    """Repository label."""

    model = Contribution.labels.through
    extra = 1
    verbose_name = "relation"
    verbose_name_plural = "relations"


class IssueInfoInline(admin.StackedInline):
    """Issue or pull request additional info."""

    model = IssueInfo
    extra = 0


class ContributionAdmin(admin.ModelAdmin):
    """Contribution representation."""

    inlines = (CommitStatsInline, IssueInfoInline)
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
