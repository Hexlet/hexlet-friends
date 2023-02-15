from django.db import models


class ContributionLabel(models.Model):
    """Model representing a label."""

    NAME_LENGTH = 45  # noqa: WPS115

    name = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        """Represent an instance as a string."""
        return self.name
