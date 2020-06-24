from contributors.models import Contributor
from contributors.utils import misc
from contributors.views import contributors


class ListView(contributors.ListView):
    """A list of contributors with monthly contributions."""

    template_name = 'contributors_for_month.html'
    context_object_name = 'contributors_list'
    queryset = Contributor.objects.visible_with_monthly_stats()

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)
        context['dt_month_ago'] = misc.datetime_month_ago()
        return context
