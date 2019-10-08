from django.conf import settings
from django.http import request


def base_template_context(request: request) -> dict:  # noqa: WPS442
    """Build common application context."""
    return {
        'PROJECT_NAME': settings.PROJECT_NAME,
    }
