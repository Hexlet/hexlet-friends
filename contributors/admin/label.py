from django.contrib import admin

from contributors.admin.custom import site
from contributors.admin.repository import RepoLabelInline
from contributors.models import Label


class LabelAdmin(admin.ModelAdmin):
    """Label representation."""

    inlines = (RepoLabelInline,)


site.register(Label, LabelAdmin)
