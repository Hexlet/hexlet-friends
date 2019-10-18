from django.views import generic

from contributors.models.repository import Repository


class ListView(generic.ListView):
    """A view for a list of repositories."""

    model = Repository
    template_name = 'repositories_list.html'
    context_object_name = 'repositories_list'
