from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

from contributors.admin.custom import site

urlpatterns = [
    path('admin/', site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript_catalog'),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('auth.urls')),
    path('', include('contributors.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

]
