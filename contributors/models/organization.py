from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from contributors.models.base import CommonFields


class Organization(CommonFields):
    """Model representing an organization."""

    class Meta(object):
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse('contributors:organization_details', args=[self.pk])
