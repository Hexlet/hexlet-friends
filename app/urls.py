from django.urls import path

from app.views import contributor, contributors, home, registration

app_name = 'contributors'
urlpatterns = [
    path(
        'registration',
        registration.RegistrationView.as_view(),
        name='registration',
    ),
    path('', home.HomeView.as_view(), name='home'),
    path(
        'contributors',
        contributors.ListView.as_view(),
        name='contributors_list',
    ),
    path(
        'contributors/<int:pk>',
        contributor.DetailView.as_view(),
        name='contributor_details',
    ),
]
