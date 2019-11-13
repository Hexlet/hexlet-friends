from django.db import models
from django.utils.translation import gettext_lazy as _

NAME_LENGTH = 30


class CommonFields(models.Model):
    """Base model with common fields."""

    name = models.CharField(
        _('name'),
        max_length=NAME_LENGTH,
        null=True,
    )
    html_url = models.URLField(_('html url'))

    class Meta(object):
        abstract = True

    def __str__(self):
        """Represents an instance as a string."""
        return self.name
