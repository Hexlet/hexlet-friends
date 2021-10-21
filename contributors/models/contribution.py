from dateutil import relativedelta
from django.db import models
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from contributors.models.contributor import Contributor
from contributors.models.repository import Repository
from contributors.utils import misc


class ContributionManager(models.Manager):
    """A custom contribution manager."""

    def for_year(self):
        """Return yearly results."""
        date_eleven_months_ago = (timezone.now() - relativedelta.relativedelta(
            months=11, day=1,   # noqa: WPS432
        )).date()

        months_with_contrib_sums = self.get_queryset().filter(
            repository__is_visible=True,
            contributor__is_visible=True,
            created_at__gte=date_eleven_months_ago,
        ).annotate(
            month=ExtractMonth('created_at'),
        ).values('month', 'type').annotate(count=Count('id'))

        sums_of_contribs_by_months = misc.group_contribs_by_months(
            months_with_contrib_sums,
        )

        return misc.get_contrib_sums_distributed_over_months(
            timezone.now().month,
            sums_of_contribs_by_months,
        )


class Contribution(models.Model):
    """Model representing a set of contributions."""

    ID_LENGTH = 40   # noqa: WPS115
    TYPE_LENGTH = 3  # noqa: WPS115

    TYPES = (   # noqa: WPS115
        ('cit', _("commit")),
        ('iss', _("issue")),
        ('pr', _("pull request")),
        ('cnt', _("comment")),
    )

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        verbose_name=_("repository"),
    )
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        verbose_name=_("contributor"),
    )
    id = models.CharField(primary_key=True, max_length=ID_LENGTH)  # noqa: A003,WPS125,E501
    type = models.CharField(_("type"), choices=TYPES, max_length=TYPE_LENGTH)  # noqa: A003,WPS125,E501
    html_url = models.URLField(_("URL"))
    created_at = models.DateTimeField(_("creation date"))

    objects = ContributionManager()  # noqa: WPS110

    class Meta(object):
        verbose_name = _("contribution")
        verbose_name_plural = _("contributions")

    def __str__(self):
        """Represent an instance as a string."""
        return str(self.id)
