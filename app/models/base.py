from django.db import models

NAMES_LENGTH = 30


class CommonFields(models.Model):
    name = models.CharField(max_length=NAMES_LENGTH, null=True)
    html_url = models.URLField()

    class Meta(object):
        abstract = True

    def __str__(self):
        return self.name
