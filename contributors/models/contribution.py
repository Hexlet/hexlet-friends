from dateutil import relativedelta
from django.db import models
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_cte import CTEManager

from contributors.models.contribution_label import ContributionLabel
from contributors.models.contributor import Contributor
from contributors.models.repository import Repository
from contributors.utils import misc


class ContributionManager(CTEManager):
    """A custom contribution manager."""

    def for_year(self):
        """Return yearly results."""
        datetime_now = timezone.now()
        date_eleven_months_ago = (datetime_now - relativedelta.relativedelta(
            months=11, day=1,
        )).date()

        months_with_contrib_sums = self.get_queryset().filter(
            repository__is_visible=True,
            contributor__is_visible=True,
            created_at__gte=date_eleven_months_ago,
        ).annotate(
            month=ExtractMonth('created_at'),
        ).values('month', 'type').annotate(count=models.Count('id'))

        sums_of_contribs_by_months = misc.group_contribs_by_months(
            months_with_contrib_sums,
        )

        return misc.get_contrib_sums_distributed_over_months(
            datetime_now.month,
            sums_of_contribs_by_months,
        )

    def for_week(self):
        """Return weekly results."""
        return self.filter(
            created_at__gte=misc.datetime_week_ago(),
        ).distinct()

    def for_month(self):
        """Return monthly results."""
        return self.filter(
            created_at__gte=misc.datetime_month_ago(),
        ).distinct()

    def visible_for_month(self):
        """Get monthly visible contribution."""
        return self.for_month().filter(
            repository__is_visible=True,
            contributor__is_visible=True,
        )

    def visible_for_week(self):
        """Get weekly visible contribution."""
        return self.for_week().filter(
            repository__is_visible=True,
            contributor__is_visible=True,
        )


class Contribution(models.Model):
    """Model representing a set of contributions."""

    ID_LENGTH = 40
    TYPE_LENGTH = 3

    TYPES = (
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
    id = models.CharField(primary_key=True, max_length=ID_LENGTH)  # noqa: A003,E501
    type = models.CharField(_("type"), choices=TYPES, max_length=TYPE_LENGTH)  # noqa: A003,E501
    html_url = models.URLField(_("URL"))
    created_at = models.DateTimeField(_("creation date"))

    objects = ContributionManager()

    labels = models.ManyToManyField(
        ContributionLabel,
        verbose_name=_("contribution labels"),
    )

    class Meta(object):
        verbose_name = _("contribution")
        verbose_name_plural = _("contributions")

    def __str__(self):
        """Represent an instance as a string."""
        return str(self.id)
