from django.db import models
from django.utils.translation import gettext_lazy as lazy

from contributors.models.base import NAMES_LENGTH, CommonFields
from contributors.models.contributor import Contributor
from contributors.models.organization import Organization


class Repository(CommonFields):
    """Repository model."""

    contributors = models.ManyToManyField(
        Contributor,
        through='Contribution',
        verbose_name=lazy('Contributors'),
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name=lazy('Organization'),
    )
    full_name = models.CharField(lazy('full name'), max_length=NAMES_LENGTH)

    class Meta(object):
        verbose_name = lazy('Repository')
        verbose_name_plural = lazy('Repositories')
