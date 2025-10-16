"""
Base test class with common setup for all tests.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

from apps.departments.models import Organization, Department

User = get_user_model()


class BaseTestCase(TestCase):
    """
    Base test case class with common setup.
    Creates organization and department by default.
    """

    def setUp(self):
        """Set up common test data."""
        super().setUp()

        # Create organization
        self.organization = Organization.objects.create(
            name='Test Organization',
            short_name='TEST_ORG',
            code='TESTORG',
            is_active=True
        )

        # Create department
        self.department = Department.objects.create(
            name='Test Department',
            code='TEST',
            organization=self.organization,
            is_active=True
        )

    def tearDown(self):
        """Clean up test data."""
        Organization.objects.all().delete()
        Department.objects.all().delete()
        User.objects.all().delete()
        super().tearDown()
