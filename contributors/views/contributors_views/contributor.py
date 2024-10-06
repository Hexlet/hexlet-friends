from django.db.models import Count, F, Q, Sum
from django.db.models.functions import Coalesce
from django.views import generic

from contributors.models import Contribution, Contributor, Repository
from contributors.views.mixins import (
    ContributorsJsonMixin,
    ContributorTotalStatMixin,
)

# This was done to fix: WPS 226 Found string literal over-use: id > 4
ID = 'id'


class DetailView(
    ContributorTotalStatMixin, ContributorsJsonMixin, generic.DetailView,
):
    """Contributor's details."""

    model = Contributor
    template_name = 'contributor/contributor_details.html'
    slug_field = 'login'

    def get_context_data(self, **kwargs):
        """Add additional context for the contributor."""
        context = super().get_context_data(**kwargs)

        repositories = Repository.objects.select_related(
            'organization',
        ).filter(
            is_visible=True,
            contribution__contributor=self.object,
        ).annotate(
            commits=Count('id', filter=Q(contribution__type='cit')),
            additions=Coalesce(Sum('contribution__stats__additions'), 0),
            deletions=Coalesce(Sum('contribution__stats__deletions'), 0),
            pull_requests=Count(
                'contribution', filter=Q(contribution__type='pr'),
            ),
            issues=Count('contribution', filter=Q(contribution__type='iss')),
            comments=Count('contribution', filter=Q(contribution__type='cnt')),
        ).order_by('organization', 'name')

        context['repositories'] = repositories
        context['contributions_for_year'] = (
            self.object.contribution_set.for_year()
        )
        context['top_repository'] = repositories.annotate(
            summary=F('commits') + F('pull_requests') + F('issues') + F('comments'),  # noqa: E501
        ).order_by('-summary').first()

        context['summary'] = Contribution.objects.filter(
            contributor=self.object,
        ).aggregate(
            commits=Count(ID, filter=Q(type='cit')),
            pull_requests=Count(ID, filter=Q(type='pr')),
            issues=Count(ID, filter=Q(type='iss')),
            comments=Count(ID, filter=Q(type='cnt')),
        )

        contributors = Contributor.objects.visible()
        contributors_ordered = contributors.order_by('name')
        context['contributors'] = contributors_ordered.values('id', 'name')

        context['current_contributor'] = self.object
        if self.request.GET.get('compare') == 'yes':
            current_user = self.request.user.contributor
            context['my_contributions_for_year'] = (
                current_user.contribution_set.for_year()
            )

        return context
