from django.conf import settings
from django.contrib import admin
from django.urls import path

from contributors import views


class CustomAdminSite(admin.AdminSite):
    """Custom admin site."""

    site_title = settings.PROJECT_NAME
    site_header = settings.PROJECT_NAME

    def get_urls(self):
        """Extend default admin urls."""
        urls = super().get_urls()
        custom_urls = [
            path(
                'contributors/config/',
                self.admin_view(views.config.show_repos),
                name='config',
            ),
            path(
                'contributors/config/collect_data',
                self.admin_view(views.config.collect_data),
                name='collect_data',
            ),
        ]
        return urls + custom_urls


site = CustomAdminSite()
