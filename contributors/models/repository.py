from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from contributors.models.base import CommonFields
from contributors.models.contributor import Contributor
from contributors.models.label import Label
from contributors.models.organization import Organization
from contributors.models.project import Project


class Repository(CommonFields):
    """Model representing a repository."""

    FULL_NAME_LENGTH = 100

    contributors = models.ManyToManyField(
        Contributor,
        through='Contribution',
        related_name='contributors',
        verbose_name=_("contributors"),
    )
    owner = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name=_("owner"),
        null=True,
        blank=True,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name=_("organization"),
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        verbose_name=_("project"),
        null=True,
        blank=True,
    )
    full_name = models.CharField(_("full name"), max_length=FULL_NAME_LENGTH)
    is_visible = models.BooleanField(_("visible"), default=True)
    labels = models.ManyToManyField(
        Label,
        verbose_name=_("labels"),
    )

    class Meta(object):
        verbose_name = _("repository")
        verbose_name_plural = _("repositories")

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse(
            'contributors:repository_details',
            args=[self.full_name],
        )
