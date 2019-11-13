from django.db.models import Count
from django.views import generic

from contributors.models.organization import Organization


class ListView(generic.ListView):
    """A view for a list of organizations."""

    queryset = Organization.objects.annotate(Count('repository'))
    template_name = 'organizations_list.html'
    context_object_name = 'organizations_list'
