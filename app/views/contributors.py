from django.views import generic

from app.models.contributor import Contributor


class ListView(generic.ListView):
    """A view for a list of contributors."""

    model = Contributor
    template_name = 'contributors_list.html'
    context_object_name = 'contributors_list'
