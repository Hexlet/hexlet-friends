from django.contrib import admin

from app.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('login', 'commits', 'pull_requests', )
    search_fields = ('login', )
