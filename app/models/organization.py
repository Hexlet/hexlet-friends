from app.models.base import CommonFields
from django.utils.translation import gettext_lazy as _


class Organization(CommonFields):
    """Organization model."""

    class Meta(object):
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')
