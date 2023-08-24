from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView, View

from auth.forms import UserCreationForm
from contributors.utils import github_lib as github


class RegistrationView(CreateView):
    """User registration view."""

    form_class = UserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')


class GitHubAuthRedirectView(RedirectView):
    """A view requesting the user's GitHub identity."""

    url = (
        'https://github.com/login/oauth/authorize'
        f'?client_id={settings.GITHUB_AUTH_CLIENT_ID}'
        '&scope=user:email'
    )
    permanent = True


class GitHubAuthView(View):
    """A view exchanging a code from GitHub for an access token."""

    def get(self, request, *args, **kwargs):
        """Try to authenticate and log in."""
        code = request.GET.get('code')
        access_token = github.get_access_token(code)
        user_data = github.get_data_of_token_holder(access_token)

        user = authenticate(request, user_data=user_data)
        if user is not None:
            login(request, user)
            return redirect('contributors:home')
        return HttpResponse("Unauthorized", status=HTTPStatus.UNAUTHORIZED)
