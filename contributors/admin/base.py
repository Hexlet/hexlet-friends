from django.contrib import admin


class ModelAdmin(admin.ModelAdmin):
    """A base ModelAdmin class."""

    def change_visibility(self, request, queryset):
        """Change visibility of the object."""
        for obj in queryset:    # noqa WPS110
            obj.is_visible = not obj.is_visible
            obj.save()
    change_visibility.short_description = (
        "Change visibility to the opposite value"
    )
