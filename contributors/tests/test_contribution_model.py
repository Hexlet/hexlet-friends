from django.test import TestCase
from django.utils import timezone

from contributors.models.contribution import Contribution
from contributors.models.contributor import Contributor
from contributors.models.repository import Repository


class ContributionManagerTestCase(TestCase):
    """Test manager methods."""

    def setUp(self):
        # Create some test data here
        self.repository = Repository.objects.create(
            name='Test Repo',
            is_visible=True,
        )
        self.contributor = Contributor.objects.create(
            name='Test Contributor',
            is_visible=True,
        )
        self.contribution = Contribution.objects.create(
            repository=self.repository,
            contributor=self.contributor,
            id='test_id',
            type='cit',
            html_url='https://example.com',
            created_at=timezone.now(),
        )

    def test_for_week(self):
        # Test the for_week method of ContributionManager
        contributions = Contribution.objects.for_week()
        self.assertEqual(contributions.count(), 1)

    def test_for_month(self):
        # Test the for_month method of ContributionManager
        contributions = Contribution.objects.for_month()
        self.assertEqual(contributions.count(), 1)

    def test_visible_for_month(self):
        # Test the visible_for_month method of ContributionManager
        contributions = Contribution.objects.visible_for_month()
        self.assertEqual(contributions.count(), 1)

    def test_visible_for_week(self):
        # Test the visible_for_week method of ContributionManager
        contributions = Contribution.objects.visible_for_week()
        self.assertEqual(contributions.count(), 1)
