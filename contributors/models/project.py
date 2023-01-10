from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from contributors.models.base import CommonFields


class Project(CommonFields):
    """Model representing a project."""

    description = models.TextField(_("description"), blank=True)
    html_url = models.URLField()

    class Meta(object):
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse('contributors:project_details', args=[self.pk])
