from django.contrib import admin
from django.db import models
from django.db.models.functions import Lower

from contributors.admin.custom import site
from contributors.admin.repository import RepoLabelInline
from contributors.models import Label


class LabelAdmin(admin.ModelAdmin):
    """Label representation."""

    inlines = (RepoLabelInline,)


models.CharField.register_lookup(Lower)

site.register(Label, LabelAdmin)
