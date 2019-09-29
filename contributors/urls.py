from django.urls import path

from contributors.views import ContributorsListView

urlpatterns = [
    path('', ContributorsListView.as_view(), name='home'),
]
