from django.views import generic

from contributors.models.contributor import Contributor


class ListView(generic.ListView):
    """A list of contributors with contributions."""

    queryset = Contributor.objects.visible().with_contributions()
    template_name = 'contributors_list.html'
    context_object_name = 'contributors_list'
