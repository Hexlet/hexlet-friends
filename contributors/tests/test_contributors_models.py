from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from faker import Faker
from faker.generator import Generator

from contributors.models.base import CommonFields
from contributors.models.contribution_label import ContributionLabel
from contributors.models.label import Label
from contributors.models.organization import Organization
from contributors.models.project import Project
from contributors.models.repository import Repository

EXISTING_ORGANISATION_NAME = "Hexlet"


class ContributorsModelsMethodsTest(TestCase):
    """Test model methods."""

    fixtures = ["organizations"]

    def setUp(self):
        """Create a test database."""
        self.faker: Generator = Faker()
        self.client: Client = Client()

    def test_label_methods(self):
        """Create a test label and test its methods."""
        label_name: str = self.faker.domain_word()
        label = Label.objects.create(name=label_name)
        self.assertEqual(str(label), label.name)

    def test_organisation_methods(self):
        """Create a test Organization and test its methods."""
        organisation_name: str = self.faker.domain_word()
        org = Organization.objects.create(name=organisation_name)
        self.assertEqual(
            org.get_absolute_url(),
            f"/organizations/{organisation_name}",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Organization.objects.create(name=organisation_name)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                rename_org = Organization.objects.get(name=organisation_name)
                rename_org.name = EXISTING_ORGANISATION_NAME
                rename_org.save()

    def test_project_methods(self):
        """Create a test project and test its methods."""
        project_name: str = self.faker.domain_word()
        project = Project.objects.create(name=project_name)
        self.assertEqual(project.get_absolute_url(), f"/projects/{project.pk}")

    def test_repository_methods(self):
        """Create a test repository and test its methods."""
        repository_name: str = self.faker.domain_word()
        repo = Repository.objects.create(full_name=repository_name)
        self.assertEqual(
            repo.get_absolute_url(),
            f"/repositories/{repo.full_name}",
        )

    def test_common_fields_methods(self):
        """Create a test common field and test its methods."""
        common_field_name: str = self.faker.domain_word()
        common_field = CommonFieldTestClass(name=common_field_name)
        self.assertEqual(str(common_field), common_field.name)

    def test_contributions_label_methods(self):
        """Create a test contribution label and test its methods."""
        contribution_label_name: str = self.faker.domain_word()
        contribution_label = ContributionLabel.objects.create(
            name=contribution_label_name,
        )
        self.assertEqual(str(contribution_label), contribution_label.name)


class CommonFieldTestClass(CommonFields):
    """Empty class to test an abstract class."""

    pass
