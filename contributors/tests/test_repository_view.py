from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

TEST_REPOSITORY_FULL_NAME = "mintough57/scriptaculous"
TEST_REPOSITORY_NAME = "scriptaculous"
TEST_REPOSITORY_NOT_EXISTS_FULL_NAME = 'Greyvoid'


class TestProjectRepositoryListTestCase(TestCase):
    """Test the methods for the repository's details view."""

    fixtures = ["contributors", "labels", "repositories", "organizations"]

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()

    def test_repository_listview_methods(self):
        response = self.client.get(
            reverse(
                "contributors:repository_details",
                args=[TEST_REPOSITORY_NOT_EXISTS_FULL_NAME],
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.get(
            reverse(
                "contributors:repository_details",
                args=[TEST_REPOSITORY_FULL_NAME],
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            str(response.context["repository"]), TEST_REPOSITORY_NAME,
        )
        self.assertIn("labels", response.context)
