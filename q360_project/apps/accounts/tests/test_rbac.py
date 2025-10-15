"""
Comprehensive RBAC (Role-Based Access Control) Tests.
Tests role hierarchy, permissions, and access control logic.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.rbac import RoleManager, PermissionChecker
from apps.departments.models import Organization, Department

User = get_user_model()


class RoleManagerTests(TestCase):
    """Test RoleManager functionality."""

    def setUp(self):
        """Set up test users with different roles."""
        self.organization = Organization.objects.create(
            name='Test Organization',
            short_name='TEST-ORG',
            code='TEST'
        )
        self.department = Department.objects.create(
            organization=self.organization,
            name='Test Department',
            code='TEST'
        )

        self.superadmin = User.objects.create_user(
            username='superadmin',
            email='super@test.com',
            password='test123',
            role='superadmin',
            first_name='Super',
            last_name='Admin',
            department=self.department
        )

        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='test123',
            role='admin',
            first_name='Admin',
            last_name='User',
            department=self.department
        )

        self.manager = User.objects.create_user(
            username='manager',
            email='manager@test.com',
            password='test123',
            role='manager',
            first_name='Manager',
            last_name='User',
            department=self.department
        )

        self.employee = User.objects.create_user(
            username='employee',
            email='employee@test.com',
            password='test123',
            role='employee',
            first_name='Employee',
            last_name='User',
            department=self.department,
            supervisor=self.manager
        )

    def test_role_hierarchy(self):
        """Test role hierarchy levels."""
        self.assertEqual(RoleManager.get_role_level('superadmin'), 0)
        self.assertEqual(RoleManager.get_role_level('admin'), 1)
        self.assertEqual(RoleManager.get_role_level('manager'), 2)
        self.assertEqual(RoleManager.get_role_level('employee'), 3)

    def test_is_superadmin(self):
        """Test superadmin identification."""
        self.assertTrue(RoleManager.is_superadmin(self.superadmin))
        self.assertFalse(RoleManager.is_superadmin(self.admin))
        self.assertFalse(RoleManager.is_superadmin(self.manager))
        self.assertFalse(RoleManager.is_superadmin(self.employee))

    def test_is_admin(self):
        """Test admin or higher identification."""
        self.assertTrue(RoleManager.is_admin(self.superadmin))
        self.assertTrue(RoleManager.is_admin(self.admin))
        self.assertFalse(RoleManager.is_admin(self.manager))
        self.assertFalse(RoleManager.is_admin(self.employee))

    def test_is_manager(self):
        """Test manager or higher identification."""
        self.assertTrue(RoleManager.is_manager(self.superadmin))
        self.assertTrue(RoleManager.is_manager(self.admin))
        self.assertTrue(RoleManager.is_manager(self.manager))
        self.assertFalse(RoleManager.is_manager(self.employee))

    def test_has_capability_superadmin(self):
        """Test superadmin capabilities."""
        self.assertTrue(RoleManager.has_capability(self.superadmin, 'can_manage_users'))
        self.assertTrue(RoleManager.has_capability(self.superadmin, 'can_manage_roles'))
        self.assertTrue(RoleManager.has_capability(self.superadmin, 'can_delete_evaluations'))

    def test_has_capability_admin(self):
        """Test admin capabilities."""
        self.assertTrue(RoleManager.has_capability(self.admin, 'can_manage_users'))
        self.assertFalse(RoleManager.has_capability(self.admin, 'can_manage_roles'))
        self.assertTrue(RoleManager.has_capability(self.admin, 'can_delete_evaluations'))

    def test_has_capability_manager(self):
        """Test manager capabilities."""
        self.assertFalse(RoleManager.has_capability(self.manager, 'can_manage_users'))
        self.assertFalse(RoleManager.has_capability(self.manager, 'can_delete_evaluations'))
        self.assertTrue(RoleManager.has_capability(self.manager, 'can_export_data'))

    def test_has_capability_employee(self):
        """Test employee capabilities (should have minimal)."""
        self.assertFalse(RoleManager.has_capability(self.employee, 'can_manage_users'))
        self.assertFalse(RoleManager.has_capability(self.employee, 'can_export_data'))

    def test_can_evaluate_admin(self):
        """Test that admin can evaluate anyone."""
        self.assertTrue(RoleManager.can_evaluate(self.admin, self.employee))
        self.assertTrue(RoleManager.can_evaluate(self.admin, self.manager))
        self.assertTrue(RoleManager.can_evaluate(self.admin, self.superadmin))

    def test_can_evaluate_manager_subordinates(self):
        """Test that manager can evaluate subordinates."""
        self.assertTrue(RoleManager.can_evaluate(self.manager, self.employee))

    def test_can_evaluate_peer(self):
        """Test that employees can evaluate peers in same department."""
        employee2 = User.objects.create_user(
            username='employee2',
            email='employee2@test.com',
            password='test123',
            role='employee',
            department=self.department
        )
        self.assertTrue(RoleManager.can_evaluate(self.employee, employee2))

    def test_can_evaluate_supervisor(self):
        """Test upward evaluation (employee can evaluate supervisor)."""
        self.assertTrue(RoleManager.can_evaluate(self.employee, self.manager))

    def test_cannot_evaluate_different_department(self):
        """Test that employees cannot evaluate users from different departments."""
        other_dept = Department.objects.create(
            organization=self.organization,
            name='Other Dept',
            code='OTHER'
        )
        other_employee = User.objects.create_user(
            username='other_employee',
            email='other@test.com',
            password='test123',
            role='employee',
            department=other_dept
        )
        self.assertFalse(RoleManager.can_evaluate(self.employee, other_employee))

    def test_can_access_own_report(self):
        """Test that users can always access their own reports."""
        self.assertTrue(RoleManager.can_access_report(self.employee, self.employee))

    def test_admin_can_access_all_reports(self):
        """Test that admin can access all reports."""
        self.assertTrue(RoleManager.can_access_report(self.admin, self.employee))
        self.assertTrue(RoleManager.can_access_report(self.admin, self.manager))

    def test_manager_can_access_subordinate_reports(self):
        """Test that manager can access subordinate reports."""
        self.assertTrue(RoleManager.can_access_report(self.manager, self.employee))

    def test_employee_cannot_access_others_reports(self):
        """Test that employee cannot access other employees' reports."""
        employee2 = User.objects.create_user(
            username='employee2',
            email='employee2@test.com',
            password='test123',
            role='employee',
            department=self.department
        )
        self.assertFalse(RoleManager.can_access_report(self.employee, employee2))

    def test_can_manage_user_superadmin(self):
        """Test that superadmin can manage all users."""
        self.assertTrue(RoleManager.can_manage_user(self.superadmin, self.admin))
        self.assertTrue(RoleManager.can_manage_user(self.superadmin, self.manager))
        self.assertTrue(RoleManager.can_manage_user(self.superadmin, self.employee))

    def test_admin_cannot_manage_superadmin(self):
        """Test that admin cannot manage superadmin."""
        self.assertFalse(RoleManager.can_manage_user(self.admin, self.superadmin))

    def test_manager_cannot_manage_users(self):
        """Test that manager cannot manage users."""
        self.assertFalse(RoleManager.can_manage_user(self.manager, self.employee))

    def test_get_accessible_users_admin(self):
        """Test that admin can access all active users."""
        accessible = RoleManager.get_accessible_users(self.admin)
        self.assertIn(self.superadmin, accessible)
        self.assertIn(self.manager, accessible)
        self.assertIn(self.employee, accessible)

    def test_get_accessible_users_manager(self):
        """Test that manager can access subordinates and department members."""
        accessible = RoleManager.get_accessible_users(self.manager)
        self.assertIn(self.employee, accessible)

    def test_get_accessible_users_employee(self):
        """Test that employee can only access department members."""
        accessible = RoleManager.get_accessible_users(self.employee)
        self.assertIn(self.manager, accessible)

        # Create employee from different department
        other_dept = Department.objects.create(
            organization=self.organization,
            name='Other',
            code='OTH'
        )
        other_employee = User.objects.create_user(
            username='other',
            email='other@test.com',
            password='test123',
            role='employee',
            department=other_dept
        )
        self.assertNotIn(other_employee, accessible)


class PermissionCheckerTests(TestCase):
    """Test PermissionChecker helper class."""

    def setUp(self):
        """Set up test user."""
        self.organization = Organization.objects.create(
            name='Test Organization',
            short_name='TEST-ORG',
            code='TEST'
        )
        self.department = Department.objects.create(
            organization=self.organization,
            name='Test Dept',
            code='TEST'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='test123',
            role='admin',
            department=self.department
        )
        self.checker = PermissionChecker(self.admin)

    def test_can_method(self):
        """Test can() method for checking capabilities."""
        self.assertTrue(self.checker.can('can_manage_users'))
        self.assertFalse(self.checker.can('can_manage_roles'))

    def test_role_check_methods(self):
        """Test role checking methods."""
        self.assertTrue(self.checker.is_admin())
        self.assertFalse(self.checker.is_superadmin())
        self.assertTrue(self.checker.is_manager())
