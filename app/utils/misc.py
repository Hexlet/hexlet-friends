import os

from django.core.exceptions import ImproperlyConfigured


def getenv(env_variable):
    """Returns an environment variable or raises an exception."""
    try:
        return os.environ[env_variable]
    except KeyError:
        raise ImproperlyConfigured(
            f"The {env_variable} setting must not be empty.",
        )
