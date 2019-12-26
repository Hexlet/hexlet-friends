from django.db import models
from django.utils.translation import gettext_lazy as _

from contributors.models.contributor import Contributor
from contributors.models.repository import Repository


class Contribution(models.Model):
    """Model representing a set of contributions."""

    ID_LENGTH = 40   # noqa: WPS115
    TYPE_LENGTH = 3  # noqa: WPS115

    TYPES = (   # noqa: WPS115
        ('cit', _("commit")),
        ('iss', _("issue")),
        ('pr', _("pull request")),
        ('cnt', _("comment")),
    )

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        verbose_name=_("repository"),
    )
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        verbose_name=_("contributor"),
    )
    id = models.CharField(primary_key=True, max_length=ID_LENGTH)  # noqa: A003
    type = models.CharField(_("type"), choices=TYPES, max_length=TYPE_LENGTH)  # noqa: A003,E501
    html_url = models.URLField(_("URL"))
    created_at = models.DateTimeField(_("creation date"))

    class Meta(object):
        verbose_name = _("contribution")
        verbose_name_plural = _("contributions")

    def __str__(self):
        """Represent an instance as a string."""
        return str(self.id)
