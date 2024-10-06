from django.views import generic

from contributors.forms.forms import PullRequestNameStatusFilterForm
from contributors.models.contribution import Contribution
from contributors.views.mixins import TableSortSearchAndPaginationMixin


class ListView(TableSortSearchAndPaginationMixin, generic.ListView):
    """A view for a list of all pull requests."""

    sortable_fields = (
        'info__title',
        'repository__full_name',
        'contributor__login',
        'created_at',
        'info__state',
    )
    searchable_fields = (
        'info__title',
        'repository__full_name',
        'contributor__login',
        'info__state',
    )
    ordering = sortable_fields[0]

    template_name = 'contributors_sections/pull_requests/pull_requests_list.html'

    def get_queryset(self):
        """Get pull requests.

        Returns:
            Queryset.
        """
        self.queryset = (
            Contribution.objects.filter(type='pr').
            select_related('repository', 'contributor', 'info')
        )

        form_status = PullRequestNameStatusFilterForm(self.request.GET)

        if form_status.is_valid():
            status = form_status.cleaned_data['state']
            start_date = form_status.cleaned_data['created_after']
            end_date = form_status.cleaned_data['created_till']
            repository = form_status.cleaned_data['repository']
            if status:
                self.queryset = self.queryset.filter(
                    info__state=status,
                ).distinct()
            if start_date:
                self.queryset = self.queryset.filter(
                    created_at__gte=start_date,
                ).distinct()
            if end_date:
                self.queryset = self.queryset.filter(
                    created_at__lte=end_date,
                ).distinct()
            if repository:
                self.queryset = self.queryset.filter(
                    repository=repository,
                ).distinct()

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Get search form by state."""
        context = super().get_context_data(**kwargs)
        context['form_status'] = PullRequestNameStatusFilterForm(
            self.request.GET,
        )
        return context
