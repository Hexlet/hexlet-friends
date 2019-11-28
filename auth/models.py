from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class SiteUser(AbstractUser):
    """Model representing a user account."""

    class Meta(object):
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        """Represent an instance as a string."""
        return self.username

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse('account_details', args=[self.pk])
