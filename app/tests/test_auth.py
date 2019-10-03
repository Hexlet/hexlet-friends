"""User authnentications test."""
from collections import OrderedDict
from http import HTTPStatus

from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.test import Client
from django.test import TestCase
from django.urls import reverse_lazy
from faker import Faker

from app.forms import RegistrationForm


class RegistrationPageViewTest(TestCase):
    """Test common registration page view."""

    def setUp(self):
        self.client: Client = Client()

    def test(self):
        """Send get request, and check data page assertions."""
        response: TemplateResponse = self.client.get(
            reverse_lazy('registration'),
        )
        form_fields: OrderedDict = RegistrationForm.base_fields
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            str(form_fields['email'].label),
            response.rendered_content
        )
        self.assertIn(
            str(form_fields['email'].help_text),
            response.rendered_content
        )
        self.assertIn(
            str(form_fields['username'].label),
            response.rendered_content
        )
        self.assertIn(
            str(form_fields['username'].help_text),
            response.rendered_content
        )
        self.assertIn(
            str(form_fields['password1'].label),
            response.rendered_content
        )
        self.assertIn(
            str(form_fields['password1'].help_text),
            response.rendered_content
        )
        self.assertIn(
            str(form_fields['password2'].label),
            response.rendered_content
        )
        self.assertIn(
            str(form_fields['password2'].help_text),
            response.rendered_content
        )


class SuccessRegistrationTest(TestCase):

    def setUp(self):
        self.client: Client = Client()
        self.faker = Faker()

    def test(self):
        email: str = self.faker.email()
        fake_password: str = self.faker.password(length=10)
        user_name: str = self.faker.user_name()
        response: TemplateResponse = self.client.post(
            reverse_lazy('registration'),
            data={
                'email': email,
                'username': user_name,
                'password1': fake_password,
                'password2': fake_password
            },
        )
        self.assertRedirects(response, reverse_lazy('index'))
        self.assertTrue(User.objects.filter(email=email, username=user_name,))

