from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from contributors.models.base import NAME_LENGTH, CommonFields
from contributors.models.contributor import Contributor
from contributors.models.organization import Organization


class Repository(CommonFields):
    """Model representing a repository."""

    contributors = models.ManyToManyField(
        Contributor,
        through='Contribution',
        verbose_name=_("contributors"),
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name=_("organization"),
    )
    full_name = models.CharField(_("full name"), max_length=NAME_LENGTH)
    is_visible = models.BooleanField(_("visible"), default=True)

    class Meta(object):
        verbose_name = _("repository")
        verbose_name_plural = _("repositories")

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse('contributors:repository_details', args=[self.pk])
