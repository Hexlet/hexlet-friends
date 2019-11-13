from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    """Application config."""

    name = 'auth'
    label = 'custom_auth'   # To avoid label clash with django.contrib.auth
    verbose_name = _("Custom Authentication and Authorization")
