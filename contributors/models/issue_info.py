from django.db import models
from django.utils.translation import gettext_lazy as _


class IssueInfo(models.Model):
    """Additional info for an issue or pull request."""

    TITLE_LENGTH = 255
    STATE_LENGTH = 10

    issue = models.OneToOneField(
        'Contribution',
        on_delete=models.CASCADE,
        verbose_name=_("issue"),
        related_name='info',
    )
    title = models.CharField(_("title"), max_length=TITLE_LENGTH)
    state = models.CharField(_("state"), max_length=STATE_LENGTH)

    class Meta(object):
        verbose_name = _("issue info")
        verbose_name_plural = _("issue info")
