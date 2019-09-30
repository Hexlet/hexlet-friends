from django.db import models
from django.utils.translation import gettext_lazy as lazy

NAMES_LENGTH = 30


class CommonFields(models.Model):
    """Base model with common fields."""

    name = models.CharField(
        lazy('name'),
        max_length=NAMES_LENGTH,
        null=True,
    )
    html_url = models.URLField(lazy('html url'))

    class Meta(object):
        abstract = True

    def __str__(self):
        """String representation."""
        return self.name
