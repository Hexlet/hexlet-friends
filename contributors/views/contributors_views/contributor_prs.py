from django.views import generic

from contributors.forms.forms import PullRequestNameStatusFilterForm
from contributors.models import Contribution
from contributors.views.mixins import TableSortSearchAndPaginationMixin


class ListView(TableSortSearchAndPaginationMixin, generic.ListView):
    """A list of pull requests of a contributor."""

    template_name = 'contributor/contributor_prs.html'
    sortable_fields = (
        'info__title',
        'repository__full_name',
        'created_at',
        'html_url',
        'info__state',
    )
    searchable_fields = (
        'info__title',
        'repository__full_name',
    )
    ordering = sortable_fields[0]

    def get_queryset(self):
        """Get pull requests from contributions.

        Returns:
            Queryset.
        """
        self.queryset = Contribution.objects.select_related('info').filter(
            contributor__login=self.kwargs['slug'], type='pr',
        )

        form_status = PullRequestNameStatusFilterForm(self.request.GET)
        if form_status.is_valid():
            status = form_status.cleaned_data['state']
            if status:
                self.queryset = self.queryset.filter(
                    info__state=status,
                ).distinct()

            return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Get search form by state."""
        context = super().get_context_data(**kwargs)
        context['form_status'] = PullRequestNameStatusFilterForm(
            self.request.GET,
        )

        return context
