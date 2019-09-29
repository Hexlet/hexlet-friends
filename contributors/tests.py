from django.test import TestCase
from django.test import Client
from django.conf import settings


class IndexPageTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_index_page_view(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(settings.APP_NAME, str(response.content))
