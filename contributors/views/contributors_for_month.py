from django.views import generic

from contributors.models.contributor import Contributor
from contributors.utils import misc


class ListView(generic.ListView):
    """A list of contributors with monthly contributions."""

    template_name = 'contributors_for_month.html'
    context_object_name = 'contributors_list'
    queryset = Contributor.objects.visible().for_month().with_contributions()

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)
        context['dt_month_ago'] = misc.datetime_month_ago()
        return context
