from django.db import models
from django.utils.translation import gettext_lazy as _

NAMES_LENGTH = 30


class CommonFields(models.Model):
    """Base github data model."""

    name = models.CharField(
        _('name'),
        max_length=NAMES_LENGTH,
        null=True,
    )
    html_url = models.URLField(_('html url'))

    class Meta(object):
        abstract = True

    def __str__(self):
        """Model string view."""
        return self.name
