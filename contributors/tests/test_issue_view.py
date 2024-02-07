from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

EXPECTED_ISSUES_COUNT = 2


class TestIssuesListViewTestCase(TestCase):
    """Test the methods for a list of open issues."""

    fixtures = [
        "contributions",
        "contributionlabel",
        "contributors",
        "issues",
        "labels",
        "repositories",
        "organizations",
    ]

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()

    def test_issues_listview_methods(self):
        response = self.client.get(reverse("contributors:open_issues"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("all_contribution_labels", response.context)
        self.assertEqual(
            len(response.context["all_contribution_labels"]),
            EXPECTED_ISSUES_COUNT,
        )
