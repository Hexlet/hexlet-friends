from django.contrib import admin

from app.models import Contributor


@admin.register(Contributor)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin declaration."""

    list_display = ('login',)
    search_fields = ('login',)
