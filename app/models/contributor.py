from django.db import models

from app.models.base import NAMES_LENGTH, CommonFields


class Contributor(CommonFields):
    """Hexlet contributor model."""

    login = models.CharField('Логин', max_length=NAMES_LENGTH)
    avatar_url = models.URLField()

    class Meta(object):
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        """Contributor model string view."""
        return self.login
