from django.db.models import Count, Sum
from django.views import generic

from contributors.models import Repository


class ListView(generic.ListView):
    """A view for a list of repositories."""

    queryset = (
        Repository.objects.select_related('organization').filter(
            is_visible=True,
            contribution__contributor__is_visible=True,
        ).annotate(
            pull_requests=Sum('contribution__pull_requests'),
            issues=Sum('contribution__issues'),
            contributors_count=Count('contribution'),
        )
    )
    template_name = 'repositories_list.html'
    context_object_name = 'repositories_list'
