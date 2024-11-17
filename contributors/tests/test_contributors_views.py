from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

TEST_CONTRIBUTOR_LOGIN = "mintough57"

EXPECTED_REPOSITORIES_COUNT = 2
EXPECTED_CONTRIBUTORS_COUNT = 2
EXPECTED_CONTRIBUTORS_ISSUE_COUNT = 2
EXPECTED_CONTRIBUTORS_PR_COUNT = 2

TEST_CONTRIBUTORS = ["mintough57", "kinganduld", "indecing", "pilly1964", "suir1948"]


class TestContributorDetailView(TestCase):
    """Test the methods for the contributor's details view."""

    fixtures = [
        "contributions",
        "contributionlabel",
        "contributors",
        "labels",
        "repositories",
        "organizations",
    ]

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()

    def test_contributor_detailview_methods(self):
        response = self.client.get(
            reverse(
                "contributors:contributor_details",
                args=[TEST_CONTRIBUTOR_LOGIN],
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("contributions_for_year", response.context)
        self.assertEqual(
            len(response.context["repositories"]),
            EXPECTED_REPOSITORIES_COUNT,
        )
        self.assertEqual(
            len(response.context["contributors"]),
            EXPECTED_CONTRIBUTORS_COUNT,
        )


class TestContributorIssuesView(TestCase):
    """Test the methods for the list of issues."""

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

    def test_contributor_issues_listview_methods(self):
        response = self.client.get(
            reverse(
                "contributors:contributor_issues",
                args=[TEST_CONTRIBUTOR_LOGIN],
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("contribution_list", response.context)
        self.assertEqual(
            len(response.context["contribution_list"]),
            EXPECTED_CONTRIBUTORS_ISSUE_COUNT,
        )


class TestContributorPrView(TestCase):
    """Test the methods for the list of pull requests."""

    fixtures = [
        "contributions",
        "contributionlabel",
        "contributors",
        "labels",
        "repositories",
        "organizations",
    ]

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()

    def test_contributor_pr_listview_methods(self):
        response = self.client.get(
            reverse(
                "contributors:contributor_pullrequests",
                args=[TEST_CONTRIBUTOR_LOGIN],
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("contribution_list", response.context)
        self.assertEqual(
            len(response.context["contribution_list"]),
            EXPECTED_CONTRIBUTORS_PR_COUNT,
        )


class TestContributorForPeriodView(TestCase):
    """Test the methods for the list of contributors for the period."""

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()

    def test_contributors_listview_methods(self):
        response = self.client.get(
            reverse("contributors:contributors_for_month"),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("dt_month_ago", response.context)
        self.assertEqual(response.context.get("period"), "month")

        response = self.client.get(
            reverse("contributors:contributors_for_week"),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("dt_month_ago", response.context)
        self.assertEqual(response.context.get("period"), "week")


class AchievementViewTestCase(TestCase):
    """Test the methods for the list of achievements."""

    fixtures = TestContributorDetailView.fixtures

    def setUp(self):
        """Create a test client."""
        self.client = Client()

    def test_get_context_data(self):
        response = self.client.get(reverse('contributors:achievements'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['contributors_amount'], 5)
        self.assertEqual(response.context['contributors_commits_gte_1'], 2)
        self.assertEqual(response.context['contributors_issues_gte_1'], 2)
        self.assertEqual(response.context['contributors_comments_gte_1'], 0)
        self.assertEqual(response.context['contributors_editions_gte_1'], 0)

    def test_get_context_data_contributor(self):
        for contributor in TEST_CONTRIBUTORS:
            response = self.client.get(reverse(
                'contributors:contributor_achievements',
                args=[contributor]),
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
