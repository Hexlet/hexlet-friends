from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from contributors.models.base import NAME_LENGTH, CommonFields


class Project(CommonFields):
    """Model representing a project."""

    full_name = models.CharField(_("full name"), max_length=NAME_LENGTH)
    is_visible = models.BooleanField(_("visible"), default=True)
    description = models.TextField( _("description"), blank=True)

    def __str__(self):
        return self.full_name

    class Meta(object):
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse('contributors:project_details', args=[self.pk])
