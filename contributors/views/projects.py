from django.views import generic

from contributors.models import Project


class ListView(generic.ListView):
    """A view for a list of projects."""

    queryset = Project.objects.all()

    template_name = 'projects_list.html'
    context_object_name = 'projects_list'
