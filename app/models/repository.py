from django.db import models

from app.models.base import NAMES_LENGTH, CommonFields
from app.models.contributor import Contributor
from app.models.organization import Organization


class Repository(CommonFields):
    """Repository model."""

    contributors = models.ManyToManyField(Contributor, through='Contribution')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=NAMES_LENGTH)

    class Meta(object):
        verbose_name = 'Repository'
        verbose_name_plural = 'Repositories'
