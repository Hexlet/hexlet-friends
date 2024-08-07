from django.db import models
from django.utils.translation import gettext_lazy as _


class ContributionLabel(models.Model):
    """Model representing a label."""

    NAME_LENGTH = 45

    name = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        """Represent an instance as a string."""
        return self.name

    class Meta(object):
        verbose_name = _("contribution label")
        verbose_name_plural = _("contribution label")
