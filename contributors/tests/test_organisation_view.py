from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

ORG_NOT_EXISTS = "mintough57"
ORG_EXISTS = "Hexlet"


class TestOrgRepositoryListTestCase(TestCase):
    """Test the methods for the organization's details view."""

    fixtures = ["organizations"]

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()

    def test_org_listview_methods(self):
        response = self.client.get(
            reverse(
                "contributors:organization_details", args=[ORG_NOT_EXISTS],
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.get(
            reverse("contributors:organization_details", args=[ORG_EXISTS]),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("organization", response.context)
        self.assertEqual(str(response.context["organization"]), ORG_EXISTS)
