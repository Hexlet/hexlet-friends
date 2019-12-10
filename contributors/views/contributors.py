from django.db.models import Sum
from django.views import generic

from contributors.models.contributor import Contributor


class ListView(generic.ListView):
    """A view for a list of contributors."""

    queryset = Contributor.objects.filter(is_visible=True).annotate(
        commits=Sum('contribution__commits'),
        additions=Sum('contribution__additions'),
        deletions=Sum('contribution__deletions'),
        pull_requests=Sum('contribution__pull_requests'),
        issues=Sum('contribution__issues'),
        comments=Sum('contribution__comments'),
    )
    template_name = 'contributors_list.html'
    context_object_name = 'contributors_list'
