from django.db.models import Count, Q  # noqa: WPS347
from django.views import generic

from contributors.models import Project


class ListView(generic.ListView):
    """A view for a list of projects."""

    queryset = (
        Project.objects.filter(
            is_visible=True,
        )
    )
    template_name = 'projects_list.html'
    context_object_name = 'projects_list'
