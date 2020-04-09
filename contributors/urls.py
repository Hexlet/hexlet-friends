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
        'organizations/<int:pk>',
        views.organization.DetailView.as_view(),
        name='organization_details',
    ),
    path(
        'repositories/',
        views.repositories.ListView.as_view(),
        name='repositories_list',
    ),
    path(
        'repositories/<int:pk>',
        views.repository.DetailView.as_view(),
        name='repository_details',
    ),
    path(
        'contributors/',
        views.contributors.ListView.as_view(),
        name='contributors_list',
    ),
    path(
        'contributors/<int:pk>',
        views.contributor.DetailView.as_view(),
        name='contributor_details',
    ),
    path(
        'projects/',
        views.projects.ListView.as_view(),
        name='projects_list',
    ),
    path(
        'projects/<int:pk>',
        views.project.DetailView.as_view(),
        name='project_details',
    ),
    path(
        "issues/",
        views.issues.ListView.as_view(),
        name="open_issues_list",
    ),
    path('event-handler', views.webhook.EventHandler.as_view()),
]
