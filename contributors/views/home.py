from django.db.models import Prefetch
from django.views.generic.base import TemplateView

from contributors.models import Contribution, Contributor

LATEST_COUNT = 10


class HomeView(TemplateView):
    """Home page view."""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """Add context."""
        context = super().get_context_data(**kwargs)

        contributors_for_month = (
            Contributor.objects.visible_with_monthly_stats().prefetch_related(
                Prefetch(
                    "contribution_set",
                    queryset=Contribution.objects.select_related("repository"),
                    to_attr="prefetched_contributions",
                )
            )
        )
        contributors_for_week = (
            Contributor.objects.visible_with_weekly_stats().prefetch_related(
                Prefetch(
                    "contribution_set",
                    queryset=Contribution.objects.select_related("repository"),
                    to_attr="prefetched_contributions",
                )
            )
        )

        latest_contributions = Contribution.objects.select_related(
            "contributor", "repository"
        ).order_by("-created_at")[: LATEST_COUNT * 2]

        context.update(
            {
                "top10_committers_of_month": self.get_top10(
                    contributors_for_month, "commits"
                ),
                "top10_requesters_of_month": self.get_top10(
                    contributors_for_month, "pull_requests"
                ),
                "top10_reporters_of_month": self.get_top10(
                    contributors_for_month, "issues"
                ),
                "top10_commentators_of_month": self.get_top10(
                    contributors_for_month, "comments"
                ),
                "top10_committers_of_week": self.get_top10(
                    contributors_for_week, "commits"
                ),
                "top10_requesters_of_week": self.get_top10(
                    contributors_for_week, "pull_requests"
                ),
                "top10_reporters_of_week": self.get_top10(
                    contributors_for_week, "issues"
                ),
                "top10_commentators_of_week": self.get_top10(
                    contributors_for_week, "comments"
                ),
                "contributions_for_year": Contribution.objects.for_year(),
                "latest_time_issues": [
                    c for c in latest_contributions if c.type == "iss"
                ][:LATEST_COUNT],
                "latest_time_pr": [c for c in latest_contributions if c.type == "pr"][
                    :LATEST_COUNT
                ],
            }
        )

        return context

    @staticmethod
    def get_top10(dataset, contrib_type):
        """Return top 10 contributors of the type from the dataset."""
        return sorted(dataset, key=lambda x: getattr(x, contrib_type), reverse=True)[
            :LATEST_COUNT
        ]
