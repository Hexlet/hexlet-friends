from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('auth.urls')),
    path('', include('contributors.urls')),
]
