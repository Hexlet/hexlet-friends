from django.db import models

from app.models.base import NAMES_LENGTH, CommonFields
from app.models.contributor import Contributor
from app.models.organization import Organization
from django.utils.translation import gettext_lazy as _


class Repository(CommonFields):
    """Repository model."""

    contributors = models.ManyToManyField(
        Contributor,
        through='Contribution',
        verbose_name=_('Contributors')
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name=_('Organization')
    )
    full_name = models.CharField(_('full name'), max_length=NAMES_LENGTH)

    class Meta(object):
        verbose_name = _('Repository')
        verbose_name_plural = _('Repositories')
