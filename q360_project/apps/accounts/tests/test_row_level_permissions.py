from django.db.models.signals import post_save
from django.test import TestCase

from apps.accounts.models import User
from apps.accounts.permissions import (
    filter_queryset_for_user,
    get_accessible_users,
    user_has_row_access,
)
from apps.onboarding.models import OnboardingProcess
from apps.onboarding.signals import ensure_onboarding_process


class RowLevelPermissionTests(TestCase):
    def setUp(self):
        # Avoid automatic onboarding noise for test fixtures.
        post_save.disconnect(ensure_onboarding_process, sender=User)
        self.addCleanup(lambda: post_save.connect(ensure_onboarding_process, sender=User))

        self.manager = User.objects.create_user(
            username="manager",
            password="pass1234",
            role="manager",
            department_id=None,
        )
        self.employee = User.objects.create_user(
            username="employee",
            password="pass1234",
            role="employee",
            supervisor=self.manager,
            department=self.manager.department,
        )
        self.other_employee = User.objects.create_user(
            username="employee2",
            password="pass1234",
            role="employee",
        )

        self.manager_process = OnboardingProcess.objects.create(
            employee=self.manager,
            created_by=self.manager,
        )
        self.employee_process = OnboardingProcess.objects.create(
            employee=self.employee,
            created_by=self.manager,
        )
        self.other_process = OnboardingProcess.objects.create(
            employee=self.other_employee,
            created_by=self.other_employee,
        )

    def test_filter_queryset_for_manager(self):
        qs = OnboardingProcess.objects.order_by("id")
        scoped = filter_queryset_for_user(self.manager, qs, relation_field="employee")
        self.assertIn(self.manager_process, scoped)
        self.assertIn(self.employee_process, scoped)
        self.assertNotIn(self.other_process, scoped)

    def test_filter_queryset_for_employee(self):
        qs = OnboardingProcess.objects.all()
        scoped = filter_queryset_for_user(self.employee, qs, relation_field="employee")
        self.assertIn(self.employee_process, scoped)
        self.assertNotIn(self.manager_process, scoped)
        self.assertNotIn(self.other_process, scoped)

    def test_get_accessible_users(self):
        users = get_accessible_users(self.manager)
        self.assertIn(self.manager, users)
        self.assertIn(self.employee, users)
        self.assertNotIn(self.other_employee, users)

    def test_user_has_row_access(self):
        self.assertTrue(user_has_row_access(self.manager, self.employee))
        self.assertFalse(user_has_row_access(self.employee, self.other_employee))
