from django.db import models

from app.models.base import CommonFields, NAMES_LENGTH
from app.models.contributor import Contributor
from app.models.organization import Organization


class Repository(CommonFields):
    contributors = models.ManyToManyField(Contributor, through='Contribution')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=NAMES_LENGTH)
