from django.views import generic

from contributors.forms.forms import CombinedSearchForm
from contributors.models import Contributor
from contributors.views.mixins import TableSortSearchAndPaginationMixin


class ListView(TableSortSearchAndPaginationMixin, generic.ListView):
    """List of leaders among contributors by commits."""

    queryset = Contributor.objects.visible().with_contributions()
    template_name = 'leaderboard_commits.html'
    sortable_fields = (
        '-commits',
        'login',
        'name',
    )
    searchable_fields = ('login', 'name')
    ordering = sortable_fields[0]
    paginate_by = 100

    def get_context_data(self, **kwargs):
        """Get search form by organizations."""
        context = super().get_context_data(**kwargs)
        context['form_org'] = CombinedSearchForm(self.request.GET)
        return context

    def get_queryset(self):  # noqa: WPS615
        """Get filter queryset."""
        queryset = super().get_queryset().prefetch_related(
            'contributors__organization',
        )
        form = CombinedSearchForm(self.request.GET)
        if form.is_valid():
            organizations = form.cleaned_data['organizations']
            if organizations:
                queryset = queryset.filter(
                    contributors__organization__name__exact=organizations,
                )
            is_hexlet_stuff = form.cleaned_data['is_hexlet_stuff']
            if is_hexlet_stuff:
                queryset = queryset.filter(user__is_staff=True)
        return queryset
