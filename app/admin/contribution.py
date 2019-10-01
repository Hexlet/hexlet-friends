from django.contrib import admin

from app.models import Contribution


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'contributor',
        'repository',
        'commits',
        'issues',
        'pull_requests',
        'comments',
        'additions',
        'deletions')
    search_fields = ('contributor__login', 'repository__name')
