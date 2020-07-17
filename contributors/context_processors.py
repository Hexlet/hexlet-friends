from django.conf import settings


def general_context(request):
    """Set a general application context."""
    return {
        'PROJECT_NAME': settings.PROJECT_NAME,
        'GTM_ID': settings.GTM_ID,
        'YANDEX_VERIFICATION': settings.YANDEX_VERIFICATION,
    }
