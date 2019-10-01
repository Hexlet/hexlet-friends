from app.models.base import NAMES_LENGTH, CommonFields
from app.models.contributor import Contributor
from app.models.organization import Organization
from django.db import models


class Repository(CommonFields):
    contributors = models.ManyToManyField(Contributor, through='Contribution')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=NAMES_LENGTH)
