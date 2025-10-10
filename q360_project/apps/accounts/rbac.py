"""
Role-Based Access Control (RBAC) Manager for Q360.
Centralized role and permission management system.
"""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class RoleManager:
    """
    Centralized role management with hierarchical permissions.
    Replaces scattered is_admin(), is_manager() methods in User model.
    """

    # Role hierarchy (lower number = higher privilege)
    ROLE_HIERARCHY = {
        'superadmin': 0,
        'admin': 1,
        'manager': 2,
        'employee': 3,
    }

    # Role capabilities mapping
    ROLE_CAPABILITIES = {
        'superadmin': {
            'can_manage_users': True,
            'can_manage_departments': True,
            'can_manage_campaigns': True,
            'can_view_all_reports': True,
            'can_manage_roles': True,
            'can_manage_system_settings': True,
            'can_delete_evaluations': True,
            'can_export_data': True,
        },
        'admin': {
            'can_manage_users': True,
            'can_manage_departments': True,
            'can_manage_campaigns': True,
            'can_view_all_reports': True,
            'can_manage_roles': False,
            'can_manage_system_settings': False,
            'can_delete_evaluations': True,
            'can_export_data': True,
        },
        'manager': {
            'can_manage_users': False,
            'can_manage_departments': False,
            'can_manage_campaigns': False,
            'can_view_all_reports': False,  # Only team reports
            'can_manage_roles': False,
            'can_manage_system_settings': False,
            'can_delete_evaluations': False,
            'can_export_data': True,  # Only team data
        },
        'employee': {
            'can_manage_users': False,
            'can_manage_departments': False,
            'can_manage_campaigns': False,
            'can_view_all_reports': False,
            'can_manage_roles': False,
            'can_manage_system_settings': False,
            'can_delete_evaluations': False,
            'can_export_data': False,
        },
    }

    @classmethod
    def get_role_level(cls, role):
        """Get numerical level for role (lower is higher privilege)."""
        return cls.ROLE_HIERARCHY.get(role, 999)

    @classmethod
    def has_role_or_higher(cls, user_role, required_role):
        """
        Check if user's role is equal to or higher than required role.

        Args:
            user_role: The user's current role
            required_role: The minimum required role

        Returns:
            bool: True if user has sufficient privileges
        """
        user_level = cls.get_role_level(user_role)
        required_level = cls.get_role_level(required_role)
        return user_level <= required_level

    @classmethod
    def is_superadmin(cls, user):
        """Check if user is superadmin."""
        return user.role == 'superadmin'

    @classmethod
    def is_admin(cls, user):
        """Check if user is admin or higher."""
        return cls.has_role_or_higher(user.role, 'admin')

    @classmethod
    def is_manager(cls, user):
        """Check if user is manager or higher."""
        return cls.has_role_or_higher(user.role, 'manager')

    @classmethod
    def has_capability(cls, user, capability):
        """
        Check if user has a specific capability.

        Args:
            user: User instance
            capability: Capability name (e.g., 'can_manage_users')

        Returns:
            bool: True if user has the capability
        """
        role_caps = cls.ROLE_CAPABILITIES.get(user.role, {})
        return role_caps.get(capability, False)

    @classmethod
    def can_evaluate(cls, evaluator, evaluatee):
        """
        Check if evaluator can evaluate the evaluatee.

        Rules:
        - Superadmin can evaluate anyone
        - Admin can evaluate anyone
        - Manager can evaluate subordinates and department members
        - Employee can evaluate peers and supervisor (in peer/upward evaluation)
        """
        # Superadmin and Admin can evaluate anyone
        if cls.is_admin(evaluator):
            return True

        # Manager can evaluate subordinates
        if cls.is_manager(evaluator):
            if evaluatee.supervisor == evaluator:
                return True
            # Can also evaluate department members
            if evaluatee.department and evaluator.department == evaluatee.department:
                return True

        # Employee can evaluate peers in same department
        if evaluatee.department and evaluator.department == evaluatee.department:
            return True

        # Can evaluate direct supervisor (upward evaluation)
        if evaluatee == evaluator.supervisor:
            return True

        return False

    @classmethod
    def can_access_report(cls, user, report_owner):
        """
        Check if user can access another user's report.

        Args:
            user: User trying to access the report
            report_owner: User who owns the report

        Returns:
            bool: True if access is allowed
        """
        # Can always access own reports
        if user == report_owner:
            return True

        # Admin can access all reports
        if cls.is_admin(user):
            return True

        # Manager can access subordinates' reports
        if cls.is_manager(user):
            if report_owner.supervisor == user:
                return True
            # Can access department members' reports
            if report_owner.department and user.department == report_owner.department:
                return True

        return False

    @classmethod
    def can_manage_user(cls, manager, target_user):
        """
        Check if manager can manage (edit, delete) target user.

        Args:
            manager: User attempting to manage
            target_user: User being managed

        Returns:
            bool: True if management is allowed
        """
        # Superadmin can manage anyone
        if cls.is_superadmin(manager):
            return True

        # Admin can manage non-superadmins
        if manager.role == 'admin':
            return target_user.role != 'superadmin'

        # Manager can only view, not manage users
        return False

    @classmethod
    def get_accessible_users(cls, user):
        """
        Get all users that the given user can access/view.

        Args:
            user: User instance

        Returns:
            QuerySet: Accessible users
        """
        from apps.accounts.models import User

        if cls.is_admin(user):
            # Admin sees all active users
            return User.objects.filter(is_active=True)
        elif cls.is_manager(user):
            # Manager sees subordinates and department members
            subordinates = user.get_subordinates()
            if user.department:
                department_members = User.objects.filter(
                    department=user.department,
                    is_active=True
                )
                # Combine and remove duplicates
                return (subordinates | department_members).distinct()
            return subordinates
        else:
            # Employee sees only department members
            if user.department:
                return User.objects.filter(
                    department=user.department,
                    is_active=True
                )
            return User.objects.filter(pk=user.pk)

    @classmethod
    def assign_default_permissions(cls, user):
        """
        Assign default Django permissions based on role.

        Args:
            user: User instance
        """
        # Clear existing permissions
        user.user_permissions.clear()

        # Get permissions based on role
        if cls.is_superadmin(user):
            # Superadmin gets all permissions
            user.is_staff = True
            user.is_superuser = True
        elif cls.is_admin(user):
            # Admin gets most permissions except user management
            user.is_staff = True
            user.is_superuser = False

            # Add specific permissions
            permissions_to_add = Permission.objects.filter(
                content_type__app_label__in=[
                    'evaluations',
                    'reports',
                    'development_plans',
                    'notifications',
                    'departments'
                ]
            )
            user.user_permissions.set(permissions_to_add)
        elif cls.is_manager(user):
            # Manager gets limited permissions
            user.is_staff = False
            user.is_superuser = False

            # Add view and limited edit permissions
            permissions_to_add = Permission.objects.filter(
                content_type__app_label__in=['evaluations', 'reports', 'development_plans'],
                codename__startswith='view_'
            )
            user.user_permissions.set(permissions_to_add)
        else:
            # Employee gets minimal permissions
            user.is_staff = False
            user.is_superuser = False
            user.user_permissions.clear()

        user.save()


class PermissionChecker:
    """
    Helper class for checking permissions in views and templates.
    """

    def __init__(self, user):
        self.user = user
        self.role_manager = RoleManager

    def can(self, capability):
        """Check if user has capability."""
        return self.role_manager.has_capability(self.user, capability)

    def is_admin(self):
        """Check if user is admin."""
        return self.role_manager.is_admin(self.user)

    def is_manager(self):
        """Check if user is manager."""
        return self.role_manager.is_manager(self.user)

    def is_superadmin(self):
        """Check if user is superadmin."""
        return self.role_manager.is_superadmin(self.user)

    def can_evaluate(self, other_user):
        """Check if can evaluate other user."""
        return self.role_manager.can_evaluate(self.user, other_user)

    def can_access_report(self, report_owner):
        """Check if can access report."""
        return self.role_manager.can_access_report(self.user, report_owner)

    def can_manage_user(self, target_user):
        """Check if can manage user."""
        return self.role_manager.can_manage_user(self.user, target_user)
