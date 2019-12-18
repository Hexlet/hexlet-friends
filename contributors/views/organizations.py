from django.db.models import Count
from django.views import generic

from contributors.models import Organization


class ListView(generic.ListView):
    """A view for a list of organizations."""

    queryset = Organization.objects.filter(
        repository__is_visible=True,
    ).annotate(repository_count=Count('repository'))

    template_name = 'organizations_list.html'
    context_object_name = 'organizations_list'
