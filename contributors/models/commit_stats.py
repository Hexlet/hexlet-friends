from django.db import models
from django.utils.translation import gettext_lazy as _


class CommitStats(models.Model):
    """Commit additions and deletions."""

    commit = models.OneToOneField(
        'Contribution',
        on_delete=models.CASCADE,
        verbose_name=_("commit"),
        related_name='stats',
    )
    additions = models.IntegerField(_("additions"), default=0)
    deletions = models.IntegerField(_("deletions"), default=0)

    class Meta(object):
        verbose_name = _("commit stats")
        verbose_name_plural = _("commit stats")
