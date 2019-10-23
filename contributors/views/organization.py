from django.views import generic

from contributors.models import Organization


class DetailView(generic.DetailView):
    """Organization's details."""

    model = Organization
    template_name = 'organization_details.html'
