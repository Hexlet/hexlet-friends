from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

TEST_PROJECT_NAME = "YoungHeart"
TEST_PROJECT_PK = 1


class TestProjectRepositoryListTestCase(TestCase):
    """Test the methods for the project's details view."""

    fixtures = ["projects"]

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()

    def test_project_listview_methods(self):
        response = self.client.get(
            reverse("contributors:project_details", args=[TEST_PROJECT_PK]),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertIn("contributions_for_year", response.context)
        self.assertEqual(str(response.context["project"]), TEST_PROJECT_NAME)
