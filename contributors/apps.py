from django.apps import AppConfig
from django.conf import settings
from django.contrib.admin.apps import AdminConfig
from django.db.models.signals import post_save

from contributors.signals import handle_user_post_save


class ContributorsConfig(AppConfig):
    """Application config."""

    name = 'contributors'

    def ready(self):
        """Additional setup."""
        post_save.connect(
            handle_user_post_save,
            sender=settings.AUTH_USER_MODEL,
        )


class CustomAdminConfig(AdminConfig):
    """Custom admin config."""

    default_site = 'contributors.admin.custom.CustomAdminSite'
