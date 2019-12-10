from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class ModelAdmin(admin.ModelAdmin):
    """A base ModelAdmin class."""

    def change_tracking(self, request, queryset):
        """Inverse tracking of the object."""
        for obj in queryset:    # noqa WPS110
            obj.is_tracked = not obj.is_tracked
            if not obj.is_tracked:
                obj.is_visible = False
            obj.save()

    def change_visibility(self, request, queryset):
        """Inverse visibility of the object."""
        for obj in queryset:    # noqa WPS110
            obj.is_visible = not obj.is_visible
            if obj.is_visible:
                obj.is_tracked = True
            obj.save()

    change_tracking.short_description = (
        _("Change tracking to the opposite value")
    )
    change_visibility.short_description = (
        _("Change visibility to the opposite value")
    )
