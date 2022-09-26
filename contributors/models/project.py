from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from contributors.models.base import CommonFields


class Project(CommonFields):
    """Model representing a project."""

    description = models.TextField(_("description"), blank=True)

    class Meta(object):
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse('contributors:project_details', args=[self.pk])

    def pull_requests(self):
        """Return pull_requests to repositories within a project."""
        return sum([repository.contribution_set.filter(
            repository__is_visible=True,
            contributor__is_visible=True,
            repository__project=self,
            type='pr',
        ).aggregate(
            count=models.Count('id'),
        ).get('count') for repository in self.repository_set.all()
        ])

    def issues(self):
        """Return issues of repositories within a project."""
        return sum([repository.contribution_set.filter(
            repository__is_visible=True,
            contributor__is_visible=True,
            repository__project=self,
            type='iss',
        ).aggregate(
            count=models.Count('id'),
        ).get('count') for repository in self.repository_set.all()
        ])

    def contributors_count(self):
        """Return a number of contributors within a project."""
        return self.repository_set.aggregate(
            count=models.Count('contributors', distinct=True),
        ).get('count')
