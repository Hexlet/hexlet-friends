from django.utils.translation import gettext_lazy as lazy

from app.models.base import CommonFields


class Organization(CommonFields):
    """Organization model."""

    class Meta(object):
        verbose_name = lazy('Organization')
        verbose_name_plural = lazy('Organizations')
