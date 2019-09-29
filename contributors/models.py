from django.db import models

NAMES_LENGTH = 30


class CommonFields(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=NAMES_LENGTH, null=True)
    html_url = models.URLField()

    class Meta(object):
        abstract = True

    def __str__(self):
        return self.name


class Organization(CommonFields):
    pass    # noqa: WPS420,WPS604


class Contributor(CommonFields):
    login = models.CharField(max_length=NAMES_LENGTH)


class Repository(CommonFields):
    contributors = models.ManyToManyField(Contributor, through='Commit')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=NAMES_LENGTH)


class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    commits = models.IntegerField(default=0)
    additions = models.IntegerField(default=0)
    deletions = models.IntegerField(default=0)
