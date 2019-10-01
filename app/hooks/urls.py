from django.urls import path

from app.hooks.pull_request import PullRequestHook

urlpatterns = [
    path('pr/', PullRequestHook.as_view(), name='hooks-commit'),
]
