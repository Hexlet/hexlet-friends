from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

EXPECTED_ISSUES_COUNT = 1


class TestIssuesListViewTestCase(TestCase):
    """Test the methods for a list of open issues."""

    fixtures = [
        "contributions",
        "contributors",
        "issues",
        "labels",
        "repositories",
    ]

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()

    def test_issues_listview_methods(self):
        response = self.client.get(reverse("contributors:open_issues_list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("repos_with_issues", response.context)
        self.assertEqual(
            len(response.context["repos_with_issues"]), EXPECTED_ISSUES_COUNT,
        )
