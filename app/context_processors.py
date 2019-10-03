from django.conf import settings
from django.http import request


def base_template_context(request: request) -> dict:
    """Build common application context"""
    return {
        'app_name': settings.APP_NAME
    }
