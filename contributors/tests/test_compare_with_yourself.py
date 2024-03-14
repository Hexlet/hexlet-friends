from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from auth.models import SiteUser
from contributors.models.contributor import Contributor

TEST_CONTRIBUTOR_LOGIN = 'mintough57'
COMPARING_CONTRIBUTOR_LOGIN = 'kinganduld'


class CompareWithYourselfViewTestCase(TestCase):
    """Test for a comparing page."""

    fixtures = [
        "contributions",
        "contributionlabel",
        "contributors",
        "labels",
        "repositories",
        "organizations",
    ]

    def setUp(self):
        self.client = Client()
        self.user = SiteUser.objects.create_user(
            username=TEST_CONTRIBUTOR_LOGIN,
        )

    def test_unauthorized(self):
        with self.assertRaises(Contributor.DoesNotExist):
            self.client.get(
                reverse(
                    'contributors:compare_with_yourself',
                    args=[COMPARING_CONTRIBUTOR_LOGIN],
                ),
            )

    def test_for_all_time(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                'contributors:compare_with_yourself',
                args=[COMPARING_CONTRIBUTOR_LOGIN],
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context['me'],
            {'commits': 2, 'pull_requests': 2, 'issues': 2, 'comments': 0},
        )
        self.assertEqual(
            response.context['enemy'],
            {'commits': 1, 'pull_requests': 1, 'issues': 2, 'comments': 0},
        )
        self.assertEqual(
            response.context['me_top_repo'],
            'kinganduld/olsonmarket',
        )
        self.assertEqual(
            response.context['enemy_top_repo'],
            'kinganduld/olsonmarket',
        )

    def test_for_week(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                'contributors:compare_with_yourself',
                args=[COMPARING_CONTRIBUTOR_LOGIN],
            ),
            {'period': 'for_week'},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context['me'],
            {'commits': 0, 'pull_requests': 0, 'issues': 0, 'comments': 0},
        )
        self.assertEqual(
            response.context['enemy'],
            {'commits': 0, 'pull_requests': 0, 'issues': 0, 'comments': 0},
        )
        self.assertEqual(
            response.context['me_top_repo'],
            '---',
        )
        self.assertEqual(
            response.context['enemy_top_repo'],
            '---',
        )
