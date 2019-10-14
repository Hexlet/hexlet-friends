from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.base import NAMES_LENGTH, CommonFields


class Contributor(CommonFields):
    """Hexlet contributor model."""

    login = models.CharField(_('Login'), max_length=NAMES_LENGTH)
    avatar_url = models.URLField(_('avatar url'))

    class Meta(object):
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        """Contributor model string view."""
        return self.login
