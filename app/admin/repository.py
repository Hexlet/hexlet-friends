from django.contrib import admin

from app.models import Repository


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'organization'
    )
    search_fields = ('id', 'name', 'organization')
