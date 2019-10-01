from app.models.contributor import Contributor
from app.models.repository import Repository
from django.db import models


class Contribution(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    commits = models.IntegerField(default=0)
    additions = models.IntegerField(default=0)
    deletions = models.IntegerField(default=0)
    pull_requests = models.IntegerField(default=0)
    issues = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
