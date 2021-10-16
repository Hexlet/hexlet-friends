from django.db import models


class Label(models.Model):
    """Model representing a label."""

    NAME_LENGTH = 15  # noqa: WPS115

    name = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        """Represent an instance as a string."""
        return self.name
