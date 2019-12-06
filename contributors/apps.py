from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class ContributorsConfig(AppConfig):
    """Application config."""

    name = 'contributors'


class CustomAdminConfig(AdminConfig):
    """Custom admin config."""

    default_site = 'contributors.admin.custom.CustomAdminSite'
