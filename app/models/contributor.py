from django.db import models
from django.utils.translation import gettext_lazy as lazy

from app.models.base import NAMES_LENGTH, CommonFields


class Contributor(CommonFields):
    """Hexlet contributor model."""

    login = models.CharField(lazy('Login'), max_length=NAMES_LENGTH)
    avatar_url = models.URLField(lazy('avatar url'))

    class Meta(object):
        verbose_name = lazy('Profile')
        verbose_name_plural = lazy('Profiles')

    def __str__(self):
        """Contributor model string view."""
        return self.login
