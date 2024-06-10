from django.conf import settings
from django.contrib import admin
from django.urls import path

from contributors.views.config import collect_data, show_repos


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
                self.admin_view(show_repos),
                name='config',
            ),
            path(
                'contributors/config/collect_data',
                self.admin_view(collect_data),
                name='collect_data',
            ),
        ]
        return urls + custom_urls


site = CustomAdminSite()
