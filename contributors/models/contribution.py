from django.db import models
from django.utils.translation import gettext_lazy as lazy

from contributors.models.contributor import Contributor
from contributors.models.repository import Repository


class Contribution(models.Model):
    """Contribution model."""

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        verbose_name=lazy('Repository'),
    )
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        verbose_name=lazy('Contributor'),
    )
    commits = models.IntegerField(lazy('commits'), default=0)
    additions = models.IntegerField(lazy('additions'), default=0)
    deletions = models.IntegerField(lazy('deletions'), default=0)
    pull_requests = models.IntegerField(lazy('pull requests'), default=0)
    issues = models.IntegerField(lazy('issues'), default=0)
    comments = models.IntegerField(lazy('comments'), default=0)

    class Meta(object):
        verbose_name = lazy('Contribution')
        verbose_name_plural = lazy('Contributions')
