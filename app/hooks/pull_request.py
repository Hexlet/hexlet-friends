from django.http import HttpResponse
from django.utils.decorators import method_decorator

from app.hooks.decorators import validate_request
from app.hooks.base import BaseHook
from app.models import Contribution, Contributor, Repository

import json


@method_decorator(validate_request, name='post')
class PullRequestHook(BaseHook):
    def post(self, request, *args, **kwargs):
        github_data = json.loads(request.POST['payload'])
        pr = github_data['pull_request']

        if github_data['action'] == 'closed' and pr['merged']:
            user = pr['user']
            login, user_id,  = user['login'], user['id']
            avatar_url, html_url = user['avatar_url'], user['html_url']
            contributor, _ = Contributor.objects.get_or_create(
                id=user_id,
                defaults={'login': login,
                          'avatar_url': avatar_url,
                          'html_url': html_url}
            )
            repository = Repository.objects.get(pk=github_data['repository']['id'])
            contribution, _ = Contribution.objects.get_or_create(
                contributor=contributor,
                repository=repository
            )
            contribution.pull_requests += 1
            contribution.save()
        return HttpResponse('ok')
