from django.views import generic

from contributors.models import Contributor, Organization


class DetailView(generic.DetailView):
    """Contributor's details."""

    model = Contributor
    template_name = 'contributor_details.html'

    def get_context_data(self, **kwargs):
        """Adds additional context for the contributor."""
        context = super().get_context_data(**kwargs)

        organizations_for_user = Organization.objects.filter(
            repository__contribution__contributor=self.object,
        ).distinct()
        orgs_dict = {}
        for organization in organizations_for_user:
            orgs_dict[organization] = {}
            org_repositories_for_user = organization.repository_set.filter(
                contribution__contributor=self.object,
            )
            for repo in org_repositories_for_user:
                orgs_dict[organization][repo] = {}
                repo_contributions_for_user = repo.contribution_set.filter(
                    contributor=self.object,
                )
                orgs_dict[organization][repo] = (
                    repo_contributions_for_user
                )

        context['organizations'] = orgs_dict
        return context
