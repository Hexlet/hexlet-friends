from django.db import models
from django.utils.translation import gettext_lazy as _

from contributors.models.contributor import Contributor
from contributors.models.repository import Repository


class Contribution(models.Model):
    """Model representing a set of contributions."""

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        verbose_name=_('Repository'),
    )
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        verbose_name=_('Contributor'),
    )
    commits = models.IntegerField(_('commits'), default=0)
    additions = models.IntegerField(_('additions'), default=0)
    deletions = models.IntegerField(_('deletions'), default=0)
    pull_requests = models.IntegerField(_('pull requests'), default=0)
    issues = models.IntegerField(_('issues'), default=0)
    comments = models.IntegerField(_('comments'), default=0)

    class Meta(object):
        verbose_name = _('Contribution')
        verbose_name_plural = _('Contributions')
