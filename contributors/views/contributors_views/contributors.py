from django.views import generic

from contributors.forms.forms import CombinedSearchForm
from contributors.models import Contributor
from contributors.views.mixins import TableSortSearchAndPaginationMixin


class ListView(TableSortSearchAndPaginationMixin, generic.ListView):
    """A list of contributors with contributions."""

    queryset = Contributor.objects.visible().with_contributions()
    template_name = 'contributors_sections/contributors/contributors_list.html'
    sortable_fields = (
        'login',
        'name',
        'commits',
        'additions',
        'deletions',
        'pull_requests',
        'issues',
        'comments',
    )
    searchable_fields = ('login', 'name')
    ordering = sortable_fields[0]

    def get_context_data(self, **kwargs):
        """Get search form by organizations."""
        context = super().get_context_data(**kwargs)
        context['form_org'] = CombinedSearchForm(self.request.GET)
        return context

    def get_queryset(self):
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
        return queryset
