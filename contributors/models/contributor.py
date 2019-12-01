from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from contributors.models.base import NAME_LENGTH, CommonFields


class Contributor(CommonFields):
    """Model representing a contributor."""

    login = models.CharField(_("login"), max_length=NAME_LENGTH)
    avatar_url = models.URLField(_("avatar URL"))
    is_visible = models.BooleanField(_("visible"), default=True)

    class Meta(object):
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        """Represent an instance as a string."""
        return self.login

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse('contributors:contributor_details', args=[self.pk])
