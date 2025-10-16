"""
Tests for salary change tracking and compensation history.
Tests salary change form, history logging, and calculations.
"""
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date

from apps.compensation.models import SalaryInformation, CompensationHistory
from apps.departments.models import Department, Organization
from .test_base import BaseTestCase

User = get_user_model()


class SalaryManagementTest(BaseTestCase):
    """
    Test salary management functionality including:
    - Salary change form view
    - Creating new salary records
    - Compensation history tracking
    - Percentage change calculations
    """

    def setUp(self):
        """Set up test data."""
        super().setUp()  # Call parent setUp to create organization and department

        # Create admin user
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            first_name='Admin',
            last_name='User',
            role='admin',
            is_admin=True,
            department=self.department
        )

        # Create manager user
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@test.com',
            password='testpass123',
            first_name='Manager',
            last_name='User',
            role='manager',
            department=self.department
        )

        # Create employee user
        self.employee = User.objects.create_user(
            username='employee',
            email='employee@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            role='employee',
            department=self.department
        )

        # Create initial salary for employee
        self.salary = SalaryInformation.objects.create(
            user=self.employee,
            base_salary=Decimal('3000.00'),
            currency='AZN',
            payment_frequency='monthly',
            effective_date=date(2024, 1, 1),
            is_active=True
        )

        self.client = Client()

    def test_salary_change_form_requires_manager_or_admin(self):
        """Test that only managers/admins can access salary change form."""
        # Login as regular employee
        self.client.login(username='employee', password='testpass123')
        response = self.client.get(
            reverse('compensation:salary-change', kwargs={'user_id': self.employee.id})
        )

        # Should redirect non-managers
        self.assertEqual(response.status_code, 302)

    def test_salary_change_form_shows_current_salary(self):
        """Test that salary change form displays current salary."""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(
            reverse('compensation:salary-change', kwargs={'user_id': self.employee.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, '3000')

    def test_create_salary_change_deactivates_old_salary(self):
        """Test creating new salary deactivates old salary record."""
        self.client.login(username='admin', password='testpass123')

        new_salary_data = {
            'new_salary': '3500.00',
            'currency': 'AZN',
            'effective_date': date.today().isoformat(),
            'change_reason': 'performance',
            'notes': 'Annual performance increase'
        }

        response = self.client.post(
            reverse('compensation:salary-change', kwargs={'user_id': self.employee.id}),
            data=new_salary_data
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        # Verify old salary is deactivated
        self.salary.refresh_from_db()
        self.assertFalse(self.salary.is_active)
        self.assertIsNotNone(self.salary.end_date)

        # Verify new salary exists and is active
        new_salary = SalaryInformation.objects.get(user=self.employee, is_active=True)
        self.assertEqual(new_salary.base_salary, Decimal('3500.00'))

    def test_salary_change_creates_history_record(self):
        """Test that salary changes are logged in history."""
        self.client.login(username='admin', password='testpass123')

        new_salary_data = {
            'new_salary': '3600.00',
            'currency': 'AZN',
            'effective_date': date.today().isoformat(),
            'change_reason': 'promotion',
            'notes': 'Promoted to Senior Developer'
        }

        response = self.client.post(
            reverse('compensation:salary-change', kwargs={'user_id': self.employee.id}),
            data=new_salary_data
        )

        self.assertEqual(response.status_code, 200)

        # Verify history record created
        history = CompensationHistory.objects.filter(user=self.employee).latest('created_at')
        self.assertEqual(history.previous_salary, Decimal('3000.00'))
        self.assertEqual(history.new_salary, Decimal('3600.00'))
        self.assertEqual(history.change_reason, 'promotion')
        self.assertEqual(history.created_by, self.admin)

    def test_compensation_history_calculates_percentage(self):
        """Test automatic percentage calculation in history."""
        history = CompensationHistory.objects.create(
            user=self.employee,
            previous_salary=Decimal('3000.00'),
            new_salary=Decimal('3300.00'),
            currency='AZN',
            change_reason='annual_increase',
            effective_date=date.today(),
            approved_by=self.admin,
            created_by=self.admin
        )

        # Should calculate 10% increase
        self.assertEqual(history.change_percentage, Decimal('10.00'))

    def test_compensation_history_handles_decrease(self):
        """Test percentage calculation for salary decrease."""
        history = CompensationHistory.objects.create(
            user=self.employee,
            previous_salary=Decimal('3000.00'),
            new_salary=Decimal('2700.00'),
            currency='AZN',
            change_reason='demotion',
            effective_date=date.today(),
            approved_by=self.admin,
            created_by=self.admin
        )

        # Should calculate -10% decrease
        self.assertEqual(history.change_percentage, Decimal('-10.00'))

    def test_compensation_history_without_previous_salary(self):
        """Test history for initial salary (no previous salary)."""
        new_employee = User.objects.create_user(
            username='newbie',
            email='newbie@test.com',
            password='testpass123',
            first_name='New',
            last_name='Employee',
            role='employee',
            department=self.department
        )

        history = CompensationHistory.objects.create(
            user=new_employee,
            previous_salary=None,
            new_salary=Decimal('2500.00'),
            currency='AZN',
            change_reason='hire',
            effective_date=date.today(),
            created_by=self.admin
        )

        # Percentage should be None for initial hire
        self.assertIsNone(history.change_percentage)

    def test_manager_can_change_team_member_salary(self):
        """Test that managers can change salaries of their team members."""
        # Make employee report to manager
        self.employee.supervisor = self.manager
        self.employee.save()

        self.client.login(username='manager', password='testpass123')

        new_salary_data = {
            'new_salary': '3200.00',
            'currency': 'AZN',
            'effective_date': date.today().isoformat(),
            'change_reason': 'market_adjustment',
            'notes': 'Market adjustment'
        }

        response = self.client.post(
            reverse('compensation:salary-change', kwargs={'user_id': self.employee.id}),
            data=new_salary_data
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

    def test_salary_validation_prevents_negative_salary(self):
        """Test that negative salaries are rejected."""
        self.client.login(username='admin', password='testpass123')

        invalid_data = {
            'new_salary': '-100.00',
            'currency': 'AZN',
            'effective_date': date.today().isoformat(),
            'change_reason': 'other',
        }

        response = self.client.post(
            reverse('compensation:salary-change', kwargs={'user_id': self.employee.id}),
            data=invalid_data
        )

        # Should fail validation
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])

    def test_salary_history_ordering(self):
        """Test that salary history is ordered by effective date."""
        # Create multiple history records
        CompensationHistory.objects.create(
            user=self.employee,
            previous_salary=Decimal('3000.00'),
            new_salary=Decimal('3200.00'),
            currency='AZN',
            change_reason='annual_increase',
            effective_date=date(2024, 6, 1),
            created_by=self.admin
        )

        CompensationHistory.objects.create(
            user=self.employee,
            previous_salary=Decimal('3200.00'),
            new_salary=Decimal('3500.00'),
            currency='AZN',
            change_reason='promotion',
            effective_date=date(2025, 1, 1),
            created_by=self.admin
        )

        history = list(CompensationHistory.objects.filter(user=self.employee))

        # Should be ordered by effective_date descending
        self.assertEqual(history[0].new_salary, Decimal('3500.00'))
        self.assertEqual(history[1].new_salary, Decimal('3200.00'))

    def test_salary_information_str_representation(self):
        """Test string representation of salary information."""
        salary_str = str(self.salary)
        self.assertIn('John Doe', salary_str)
        self.assertIn('3000', salary_str)
        self.assertIn('AZN', salary_str)

    def test_multiple_currency_support(self):
        """Test salary changes with different currencies."""
        self.client.login(username='admin', password='testpass123')

        usd_salary_data = {
            'new_salary': '1800.00',
            'currency': 'USD',
            'effective_date': date.today().isoformat(),
            'change_reason': 'market_adjustment',
            'notes': 'Switched to USD compensation'
        }

        response = self.client.post(
            reverse('compensation:salary-change', kwargs={'user_id': self.employee.id}),
            data=usd_salary_data
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        # Verify currency changed
        new_salary = SalaryInformation.objects.get(user=self.employee, is_active=True)
        self.assertEqual(new_salary.currency, 'USD')

    def tearDown(self):
        """Clean up test data."""
        User.objects.all().delete()
        Department.objects.all().delete()
        SalaryInformation.objects.all().delete()
        CompensationHistory.objects.all().delete()
