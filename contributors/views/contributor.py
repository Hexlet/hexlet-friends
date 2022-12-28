from django.db.models import Count, Q, Sum  # noqa: WPS347
from django.db.models.functions import Coalesce
from django.views import generic

from contributors.models import Contributor, Repository


class DetailView(generic.DetailView):
    """Contributor's details."""

    model = Contributor
    template_name = 'contributor_details.html'
    slug_field = 'login'
    queryset = Contributor.objects.with_contributions()

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
        total = self.object.contribution_set.aggregate(
            commits=Count('id', filter=Q(type='cit')),
            additions=Coalesce(Sum('stats__additions'), 0),
            deletions=Coalesce(Sum('stats__deletions'), 0),
            pull_requests=Count('id', filter=Q(type='pr')),
            issues=Count('id', filter=Q(type='iss')),
            comments=Count('id', filter=Q(type='cnt')),
        )
        context['contributors_json'] = list(
            Contributor.objects.visible().with_contributions().values(
                'id',
                'commits',
                'additions',
                'deletions',
                'pull_requests',
                'issues',
                'comments',
            ),
        )
        context['contributors'] = Contributor.objects.visible().values(
            'id',
            'name',
        )
        context['total'] = total
        return context
