from django.db import models
from django.utils.translation import gettext_lazy as _

NAME_LENGTH = 50


class CommonFields(models.Model):
    """Base model with common fields."""

    name = models.CharField(
        _("name"),
        max_length=NAME_LENGTH,
        null=True,
    )
    html_url = models.URLField(_("URL"))
    is_tracked = models.BooleanField(_("tracked"), default=True)

    class Meta(object):
        abstract = True

    def __str__(self):
        """Represent an instance as a string."""
        return self.name
