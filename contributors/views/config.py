import subprocess  # noqa: S404

import requests
from django.http import HttpResponseForbidden
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from contributors.admin import custom
from contributors.forms import OrgNamesForm, RepoNamesForm
from contributors.models import Organization, Repository
from contributors.utils import github_lib as github
from contributors.utils import misc


def set_up_context(request):
    """Set up admin site context."""
    context = custom.site.each_context(request)
    context['title'] = _("Processing configuration")
    return context


def show_repos(request):
    """Get repositories for organizations."""
    context = set_up_context(request)
    if request.method == 'POST':
        form_orgs = OrgNamesForm(request.POST)
        if form_orgs.is_valid():
            session = requests.Session()
            repos_choices = []
            for org_name in form_orgs.cleaned_data['organizations'].split():
                org_data = github.get_org_data(org_name, session)
                org, _ = misc.get_or_create_record(Organization, org_data)
                repos_data = [
                    repo for repo in github.get_org_repos(org_name, session)
                ]
                for repo_data in repos_data:
                    misc.get_or_create_record(
                        org,
                        repo_data,
                        {'is_tracked': False, 'is_visible': False},
                    )
                    repos_choices.append(
                        (repo_data['id'], repo_data['name']),
                    )
            session.close()
            form_repos = RepoNamesForm(choices=repos_choices)
            context['form_repos'] = form_repos
    else:
        form_orgs = OrgNamesForm()

    context['form_orgs'] = form_orgs

    return TemplateResponse(request, 'admin/configuration.html', context)


def collect_data(request):
    """Collect data for chosen repositories."""
    context = set_up_context(request)
    if request.method == 'POST':
        repo_ids = request.POST.getlist('repositories')
        repos = Repository.objects.filter(id__in=repo_ids)
        for repo in repos:
            repo.is_tracked = True
            repo.is_visible = True
            repo.save()
        fetch_command = ['./manage.py', 'fetchdata', '--repo']
        fetch_command.extend([repo.full_name for repo in repos])  # noqa: WPS441,E501
        subprocess.Popen(fetch_command)  # noqa: S603
        return TemplateResponse(request, 'admin/data_collection.html', context)
    return HttpResponseForbidden("Forbidden.")
