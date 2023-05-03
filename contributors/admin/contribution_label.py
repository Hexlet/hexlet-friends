from django.contrib import admin

from contributors.admin.contribution import ContributionLabelInline
from contributors.admin.custom import site
from contributors.models import ContributionLabel


class ContributionLabelAdmin(admin.ModelAdmin):
    """Label representation."""

    inlines = (ContributionLabelInline,)


site.register(ContributionLabel, ContributionLabelAdmin)
