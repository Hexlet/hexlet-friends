from django.urls import path

from app.views.index import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
