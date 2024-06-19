from collections import OrderedDict
from http import HTTPStatus
from unittest.mock import patch

from django.template.response import TemplateResponse
from django.test import Client, TestCase
from django.urls import reverse_lazy
from faker import Faker
from faker.generator import Generator

from auth.forms import UserCreationForm
from auth.models import GroupUser, SiteUser


class RegistrationPageViewTest(TestCase):
    """Test common registration page view."""

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()

    def test(self):
        """Send get request, and check data page assertions."""
        response: TemplateResponse = self.client.get(
            reverse_lazy('auth:registration'),
        )
        form_fields: OrderedDict = UserCreationForm.base_fields
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self._assert_email(form_fields, response)
        self._assert_username(form_fields, response)
        self._assert_password(form_fields, response)
        self._assert_password_confirmation(form_fields, response)

    def _assert_email(self, form_fields, response):
        self.assertIn(
            str(form_fields['email'].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields['email'].help_text),
            response.rendered_content,
        )

    def _assert_username(self, form_fields, response):
        self.assertIn(
            str(form_fields['username'].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields['username'].help_text),
            response.rendered_content,
        )

    def _assert_password(self, form_fields, response):
        self.assertIn(
            str(form_fields['password1'].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields['password1'].help_text),
            response.rendered_content,
        )

    def _assert_password_confirmation(self, form_fields, response):
        self.assertIn(
            str(form_fields['password2'].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields['password2'].help_text),
            response.rendered_content,
        )


class SuccessRegistrationTest(TestCase):
    """Test user registration."""

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()
        self.faker: Generator = Faker()

    def test(self):
        """Send valid registration request."""
        email: str = self.faker.email()
        fake_password: str = self.faker.password(length=10)
        user_name: str = self.faker.user_name()
        response: TemplateResponse = self.client.post(
            reverse_lazy('auth:registration'),
            data={
                'email': email,
                'username': user_name,
                'password1': fake_password,
                'password2': fake_password,
            },
        )
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertTrue(
            SiteUser.objects.filter(email=email, username=user_name),
        )


class AuthModelsMethodsTest(TestCase):
    """Test model methods."""

    def setUp(self):
        """Create a test database."""
        self.faker: Generator = Faker()
        self.client: Client = Client()

    def test_siteuser_methods(self):
        """Create a test user and test its methods."""
        user_name: str = self.faker.user_name()
        user = SiteUser.objects.create(username=user_name)
        self.assertEqual(str(user), user.username)

    def test_groupuser_methods(self):
        """Create a test group and test its methods."""
        group_name: str = self.faker.domain_word()
        group = GroupUser.objects.create(name=group_name)
        self.assertEqual(str(group), group.name)


class AuthViewsTest(TestCase):
    """Test auth views."""

    def setUp(self):
        """Create a test client."""
        self.client: Client = Client()

    @patch('contributors.utils.github_lib.get_access_token', lambda *args: None)
    @patch('contributors.utils.github_lib.get_data_of_token_holder', lambda *args: None)
    @patch('auth.backends.GitHubBackend.authenticate', lambda *args: None)
    def test_github_auth_view(self):
        """Send a request without authentication and check the response."""
        response = self.client.get(reverse_lazy('auth:github-login'))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
