from django.urls import path

from contributors import views

app_name = 'contributors'
urlpatterns = [
    path('', views.home.HomeView.as_view(), name='home'),
    path(
        'organizations/',
        views.organizations.ListView.as_view(),
        name='organizations_list',
    ),
    path(
        'organizations/<slug:slug>',
        views.organization.OrgRepositoryList.as_view(),
        name='organization_details',
    ),
    path(
        'repositories/',
        views.repositories.ListView.as_view(),
        name='repositories_list',
    ),
    path(
        'repositories/<path:slug>',
        views.repository.RepoContributorList.as_view(),
        name='repository_details',
    ),
    path(
        'contributors/',
        views.contributors.ListView.as_view(),
        name='contributors_list',
    ),
    path(
        'contributors/for-month',
        views.contributors_for_period.ListView.as_view(
            extra_context={'period': 'month'},
        ),
        name='contributors_for_month',
    ),
    path(
        'contributors/for-week',
        views.contributors_for_period.ListView.as_view(
            extra_context={'period': 'week'},
        ),
        name='contributors_for_week',
    ),
    path(
        'contributors/<slug:slug>',
        views.contributor.DetailView.as_view(),
        name='contributor_details',
    ),
    path(
        'contributors/<slug:slug>/issues/',
        views.contributor_issues.ListView.as_view(),
        name='contributor_issues',
    ),
    path(
        'contributors/<slug:slug>/pullrequests/',
        views.contributor_prs.ListView.as_view(),
        name='contributor_pullrequests',
    ),
    path(
        'projects/',
        views.projects.ListView.as_view(),
        name='projects_list',
    ),
    path(
        'projects/<int:pk>',
        views.project.ProjectRepositoryList.as_view(),
        name='project_details',
    ),
    path(
        "issues",
        views.issues.ListView.as_view(),
        name="open_issues",
    ),
    path(
        "pull_requests",
        views.pull_requests.ListView.as_view(),
        name="pull_requests_list",
    ),
    path('event-handler', views.webhook.EventHandler.as_view()),
    path('about', views.about.AboutView.as_view(), name="about"),
]
