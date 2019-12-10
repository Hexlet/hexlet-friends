from django.db.models import Count, Q
from django.views import generic

from contributors.models import Organization, Repository


class ListView(generic.ListView):
    """A view for a list of organizations."""

    visible_repos = Repository.objects.filter(is_visible=True)
    queryset = Organization.objects.annotate(repository_count=Count(
        'repository', filter=Q(repository__in=visible_repos),
    ))

    template_name = 'organizations_list.html'
    context_object_name = 'organizations_list'
