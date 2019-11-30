from django.conf import settings
from django.contrib import admin

from contributors.admin import (
    contribution,
    contributor,
    organization,
    repository,
)

admin.site.site_title = settings.PROJECT_NAME
admin.site.site_header = settings.PROJECT_NAME
