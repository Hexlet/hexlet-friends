from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as lazy

from contributors.models.base import NAMES_LENGTH, CommonFields


class Contributor(CommonFields):
    """Model representing a contributor."""

    login = models.CharField(lazy('Login'), max_length=NAMES_LENGTH)
    avatar_url = models.URLField(lazy('avatar url'))

    class Meta(object):
        verbose_name = lazy('Profile')
        verbose_name_plural = lazy('Profiles')

    def __str__(self):
        """String representation."""
        return self.login

    def get_absolute_url(self):
        """Returns the url of an instance."""
        return reverse('contributors:contributor_details', args=[self.pk])
