from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce
from django.views import generic

from contributors.models.contributor import Contributor


class ListView(generic.ListView):
    """A view for a list of contributors."""

    queryset = Contributor.objects.filter(is_visible=True).annotate(
        commits=Count('contribution', filter=Q(contribution__type='cit')),
        additions=Coalesce(Sum('contribution__stats__additions'), 0),
        deletions=Coalesce(Sum('contribution__stats__deletions'), 0),
        pull_requests=Count('contribution', filter=Q(contribution__type='pr')),
        issues=Count('contribution', filter=Q(contribution__type='iss')),
        comments=Count('contribution', filter=Q(contribution__type='cnt')),
    )
    template_name = 'contributors_list.html'
    context_object_name = 'contributors_list'
