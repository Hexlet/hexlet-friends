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
        ).distinct()

        repos_with_issues = {}
        for repo in repositories:
            repos_with_issues[repo] = repo.contribution_set.filter(
                type='iss',
                info__is_open=True,
            )

        context['repos_with_issues'] = {
            repo: issues for repo, issues in sorted(    # noqa: WPS441
                repos_with_issues.items(),
                key=lambda item: len(item[1]),  # noqa: WPS110
                reverse=True,
            )
        }
        return context
