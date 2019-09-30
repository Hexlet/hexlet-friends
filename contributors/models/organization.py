from django.urls import reverse
from django.utils.translation import gettext_lazy as lazy

from contributors.models.base import CommonFields


class Organization(CommonFields):
    """Model representing an organization."""

    class Meta(object):
        verbose_name = lazy('Organization')
        verbose_name_plural = lazy('Organizations')

    def get_absolute_url(self):
        """Returns the url of an instance."""
        return reverse('contributors:organization_details', args=[self.pk])
