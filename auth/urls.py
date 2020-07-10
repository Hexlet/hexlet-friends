from django.urls import path

from auth.views import (
    GitHubAuthRedirectView,
    GitHubAuthView,
    RegistrationView,
)

app_name = 'auth'
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('github/', GitHubAuthRedirectView.as_view(), name='github'),
    path('github/login/', GitHubAuthView.as_view(), name='github-login'),
]
