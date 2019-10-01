from django.contrib import admin

from app.models import Contributor


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'login',
        'name',
    )
    search_fields = ('id', 'login', 'name')
