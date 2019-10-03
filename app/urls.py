from django.urls import path

from app.views.index import IndexView
from app.views.registration import RegistrationView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registration', RegistrationView.as_view(), name='registration'),
]
