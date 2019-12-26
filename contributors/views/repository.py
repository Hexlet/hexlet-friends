from django.db.models import Count, Q, Sum  # noqa: WPS226
from django.db.models.functions import Coalesce
from django.views import generic

from contributors.models import Repository


class DetailView(generic.DetailView):
    """Repository's details."""

    model = Repository
    template_name = 'repository_details.html'

    def get_context_data(self, **kwargs):
        """Add additional context for the repository."""
        context = super().get_context_data(**kwargs)

        contributors = self.object.contributors.filter(
            is_visible=True,
        ).annotate(
            pull_requests=Count(
                'contribution', filter=Q(contribution__type='pr'),
            ),
            issues=Count(
                'contribution', filter=Q(contribution__type='iss'),
            ),
            comments=Count(
                'contribution', filter=Q(contribution__type='cnt'),
            ),
            commits=Count(
                'contribution', filter=Q(contribution__type='cit'),
            ),
            additions=Coalesce(Sum('contribution__stats__additions'), 0),
            deletions=Coalesce(Sum('contribution__stats__deletions'), 0),
        )

        context['contributors'] = contributors
        return context
