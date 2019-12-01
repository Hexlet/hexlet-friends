from django.db.models import Count, Q, Sum
from django.views import generic

from contributors.models import Contribution, Repository


class ListView(generic.ListView):
    """A view for a list of repositories."""

    visible_contributions = Contribution.objects.filter(
        contributor__is_visible=True,
    )
    filter_ = Q(contribution__in=visible_contributions)
    queryset = (
        Repository.objects.select_related('organization').filter(
            is_visible=True,
        ).annotate(
            pull_requests=Sum('contribution__pull_requests', filter=filter_),
            issues=Sum('contribution__issues', filter=filter_),
            contributors_count=Count('contribution', filter=filter_),
        )
    )
    template_name = 'repositories_list.html'
    context_object_name = 'repositories_list'
