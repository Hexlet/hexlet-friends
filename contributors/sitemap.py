from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from contributors.models import (
    Contributor,
    Organization,
    Project,
    Repository,
)


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return [
            "contributors:home",
            "contributors:about",
            "contributors:landing",
            "contributors:achievements",
        ]

    def location(self, item):
        return reverse(item)


class OrganizationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Organization.objects.all()

    def location(self, item):
        return reverse("contributors:organization_details", args=[item.name])


class RepositorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Repository.objects.all()

    def location(self, item):
        return reverse("contributors:repository_details", args=[item.name])


class ContributorSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Contributor.objects.all()

    def location(self, item):
        return reverse("contributors:contributor_details", args=[item.login])


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Project.objects.all()

    def location(self, item):
        return reverse("contributors:project_details", args=[item.pk])


sitemaps = {
    "static": StaticViewSitemap,
    "organizations": OrganizationSitemap,
    "repositories": RepositorySitemap,
    "contributors": ContributorSitemap,
    "projects": ProjectSitemap,
}
