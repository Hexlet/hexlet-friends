from http import HTTPStatus

from django.conf import settings
from django.test import Client, TestCase


class IndexPageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_page_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(settings.APP_NAME, str(response.content))
