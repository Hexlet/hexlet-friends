from django.db.models import Count
from django.views.generic.base import TemplateView

from contributors.models import Repository


class ListView(TemplateView):
    """A view for a list of open issues."""

    template_name = 'open_issues_list.html'

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        repositories = Repository.objects.filter(
            is_visible=True,
            contribution__type='iss',
            contribution__info__is_open=True,
        ).distinct().annotate(
            Count('contribution'),
        ).order_by('-contribution__count')

        repos_with_issues = {}
        for repo in repositories:
            repos_with_issues[repo] = repo.contribution_set.filter(
                type='iss',
                info__is_open=True,
            )

        context['repos_with_issues'] = repos_with_issues
        return context
