from django.views import generic

from contributors.forms.forms import OrganizationFilterForm
from contributors.models import Contributor
from contributors.views.mixins import TableSortSearchAndPaginationMixin


class ListView(TableSortSearchAndPaginationMixin, generic.ListView):
    """A list of contributors with contributions."""

    queryset = Contributor.objects.visible().with_contributions()
    template_name = 'contributors_list.html'
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

    @property
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_org'] = OrganizationFilterForm(self.request.GET)
        return context

    @property
    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            'contributors__organization'
        )
        form_org = OrganizationFilterForm(self.request.GET)
        if form_org.is_valid():
            organizations = form_org.cleaned_data['organizations']

            if organizations:
                queryset = queryset.filter(
                    contributors__organization=organizations).distinct(
                )
            return queryset
