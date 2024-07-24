from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

SEARCH_FORM_CONTEXT_NAME = "form_org"
SEARCH_PARAM_ORG_EXISTS = {
    "search": "",
    "organizations": "Hexlet",
}
SEARCH_PARAM_ORG_NOT_EXISTS = {
    "search": "",
    "organizations": "123456",
}

OBJECTS_KEY = 'contributor_list'


class TestContributorLeaderboardViews(TestCase):
    """Test the functional leaderboard."""

    fixtures = [
        "organizations",
        "repositories",
        "contributions",
        "issues",
        "contributors",
        "contributionlabel",
        "labels",
    ]

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()

    def test_contributor_leaderboard_commits_view(self):
        response = self.client.get(
            reverse("contributors:leaderboard_commits"),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(SEARCH_FORM_CONTEXT_NAME, response.context)

    def test_contributor_leaderboard_commits_methods(self):
        response = self.client.get(
            reverse("contributors:leaderboard_commits"),
            SEARCH_PARAM_ORG_NOT_EXISTS,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context[OBJECTS_KEY]), 0)

        response = self.client.get(
            reverse("contributors:leaderboard_commits"),
            SEARCH_PARAM_ORG_EXISTS,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(len(response.context[OBJECTS_KEY]), 0)

    def test_contributor_leaderboard_prs_view(self):
        response = self.client.get(
            reverse("contributors:leaderboard_prs"),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(SEARCH_FORM_CONTEXT_NAME, response.context)

    def test_contributor_leaderboard_prs_methods(self):
        response = self.client.get(
            reverse("contributors:leaderboard_prs"),
            SEARCH_PARAM_ORG_NOT_EXISTS,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context[OBJECTS_KEY]), 0)

        response = self.client.get(
            reverse("contributors:leaderboard_prs"),
            SEARCH_PARAM_ORG_EXISTS,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(len(response.context[OBJECTS_KEY]), 0)

    def test_contributor_leaderboard_issues_view(self):
        response = self.client.get(
            reverse("contributors:leaderboard_issues"),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(SEARCH_FORM_CONTEXT_NAME, response.context)

    def test_contributor_leaderboard_issues_methods(self):
        response = self.client.get(
            reverse("contributors:leaderboard_issues"),
            SEARCH_PARAM_ORG_NOT_EXISTS,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context[OBJECTS_KEY]), 0)

        response = self.client.get(
            reverse("contributors:leaderboard_issues"),
            SEARCH_PARAM_ORG_EXISTS,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(len(response.context[OBJECTS_KEY]), 0)
