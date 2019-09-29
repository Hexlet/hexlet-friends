from django.contrib import admin

from contributors.models import Commit, Contributor, Organization, Repository

admin.site.register(Organization)
admin.site.register(Repository)
admin.site.register(Contributor)
admin.site.register(Commit)
