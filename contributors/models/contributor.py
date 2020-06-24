from django.db import models
from django.db.models import Count, Q, Sum  # noqa: WPS347
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from contributors.models.base import NAME_LENGTH, CommonFields
from contributors.utils.misc import datetime_month_ago


class ContributorQuerySet(models.QuerySet):
    """A custom contributor QuerySet."""

    def visible(self):
        """Return only visible contributors."""
        return self.filter(
            is_visible=True,
            contribution__repository__is_visible=True,
        )

    def with_contributions(self):
        """Return a list of contributors annotated with contributions."""
        return self.annotate(
            commits=Count('contribution', filter=Q(contribution__type='cit')),
            additions=Coalesce(Sum('contribution__stats__additions'), 0),
            deletions=Coalesce(Sum('contribution__stats__deletions'), 0),
            pull_requests=Count(
                'contribution', filter=Q(contribution__type='pr'),
            ),
            issues=Count('contribution', filter=Q(contribution__type='iss')),
            comments=Count('contribution', filter=Q(contribution__type='cnt')),
        )

    def for_month(self):
        """Return monthly results."""
        return self.filter(
            contribution__created_at__gte=datetime_month_ago(),
        )


class Contributor(CommonFields):
    """A model representing a contributor."""

    login = models.CharField(_("login"), max_length=NAME_LENGTH)
    avatar_url = models.URLField(_("avatar URL"))
    is_visible = models.BooleanField(_("visible"), default=True)

    objects = ContributorQuerySet.as_manager()  # noqa: WPS110

    class Meta(object):
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        """Represent an instance as a string."""
        return self.login

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse('contributors:contributor_details', args=[self.pk])
