from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class LandingViewTestCase(TestCase):
    """Test for a new landing page."""

    def setUp(self):
        self.client = Client()

    def test_response(self):
        response = self.client.get(reverse('contributors:landing'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
