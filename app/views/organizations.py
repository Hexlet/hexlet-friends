from django.views import generic

from app.models.organization import Organization


class ListView(generic.ListView):
    """A view for a list of organizations."""

    model = Organization
    template_name = 'organizations_list.html'
    context_object_name = 'organizations_list'
