from contributors.models import Contributor
from contributors.utils import misc
from contributors.views import contributors


class ListView(contributors.ListView):
    """A list of contributors with monthly contributions."""

    template_name = 'contributors_for_period.html'
    context_object_name = 'contributors_list'

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)
        context['dt_month_ago'] = misc.datetime_month_ago()
        return context

    def get_queryset(self):  # noqa: WPS615
        """Modify queryset depending on extra_content.period value."""
        if self.extra_context.get('period') == 'week':
            self.queryset = Contributor.objects.visible_with_weekly_stats()
        elif self.extra_context.get('period') == 'month':
            self.queryset = Contributor.objects.visible_with_monthly_stats()
        return super().get_queryset()
