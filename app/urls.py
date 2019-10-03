from django.urls import path

from app.views import IndexView, RegistrationView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registration', RegistrationView.as_view(), name='registration'),
]
