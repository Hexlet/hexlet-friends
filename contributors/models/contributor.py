from django.conf import settings
from django.db import models
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_cte import CTEQuerySet

from contributors.models.base import NAME_LENGTH, CommonFields
from contributors.utils.misc import datetime_month_ago, datetime_week_ago


class ContributorQuerySet(CTEQuerySet):
    """A custom contributor QuerySet."""

    def visible(self):
        """Return only visible contributors."""
        return self.filter(
            is_visible=True,
            contribution__repository__is_visible=True,
        ).distinct()

    def with_contributions(self):
        """Return a list of contributors annotated with contributions."""
        return self.annotate(
            commits=models.Count('contribution', filter=models.Q(contribution__type='cit')),
            additions=Coalesce(models.Sum('contribution__stats__additions'), 0),
            deletions=Coalesce(models.Sum('contribution__stats__deletions'), 0),
            pull_requests=models.Count('contribution', filter=models.Q(contribution__type='pr')),
            issues=models.Count('contribution', filter=models.Q(contribution__type='iss')),
            comments=models.Count('contribution', filter=models.Q(contribution__type='cnt')),
        ).annotate(
            editions=models.F('additions') + models.F('deletions'),
            contribution_amount=models.F('commits') + models.F('editions')
            + models.F('pull_requests') + models.F('issues') + models.F('comments')
        )

    def for_month(self):
        """Return monthly results."""
        return self.filter(
            contribution__created_at__gte=datetime_month_ago(),
        ).distinct()

    def for_week(self):
        """Return weekly results."""
        return self.filter(
            contribution__created_at__gte=datetime_week_ago(),
        ).distinct()

    def visible_with_monthly_stats(self):
        """Get monthly contribution stats for visible contributors ."""
        visible_contributors = self.visible().filter(id=models.OuterRef('id'))
        return self.for_month().filter(
            id__in=models.Subquery(visible_contributors.values('id')),
        ).with_contributions()

    def visible_with_weekly_stats(self):
        """Get weekly contribution stats for visible contributors."""
        visible_contributors = self.visible().filter(id=models.OuterRef('id'))
        return self.for_week().filter(
            id__in=models.Subquery(visible_contributors.values('id')),
        ).with_contributions()


class Contributor(CommonFields):
    """A model representing a contributor."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    login = models.CharField(_("login"), max_length=NAME_LENGTH)
    avatar_url = models.URLField(_("avatar URL"))
    is_visible = models.BooleanField(_("visible"), default=True)

    objects = ContributorQuerySet.as_manager()

    class Meta(object):
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        """Represent an instance as a string."""
        return self.login

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse('contributors:contributor_details', args=[self.login])
