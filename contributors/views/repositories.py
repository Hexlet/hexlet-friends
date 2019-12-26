from django.db.models import Count, Q
from django.views import generic

from contributors.models import Repository


class ListView(generic.ListView):
    """A view for a list of repositories."""

    queryset = (
        Repository.objects.select_related('organization').filter(
            is_visible=True,
            contribution__contributor__is_visible=True,
        ).annotate(
            pull_requests=Count(
                'contribution', filter=Q(contribution__type='pr'),
            ),
            issues=Count(
                'contribution', filter=Q(contribution__type='iss'),
            ),
            contributors_count=Count(
                'contribution__contributor', distinct=True,
            ),
        )
    )
    template_name = 'repositories_list.html'
    context_object_name = 'repositories_list'
