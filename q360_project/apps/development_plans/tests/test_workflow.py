"""
Tests for Development Goal Approval Workflow.
Tests state transitions, permissions, and edge cases.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta

from apps.accounts.models import User
from apps.departments.models import Organization, Department
from apps.development_plans.models import DevelopmentGoal


class DevelopmentGoalWorkflowTests(TestCase):
    """Test DevelopmentGoal state machine logic."""

    def setUp(self):
        """Set up test users and department."""
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

        self.employee = User.objects.create_user(
            username='employee',
            email='employee@test.com',
            password='test123',
            role='employee',
            department=self.department
        )

        self.manager = User.objects.create_user(
            username='manager',
            email='manager@test.com',
            password='test123',
            role='manager',
            department=self.department
        )

    def create_goal(self, status='draft'):
        """Helper to create a development goal."""
        return DevelopmentGoal.objects.create(
            user=self.employee,
            title='Test Goal',
            description='Test description',
            category='Technical Skills',
            status=status,
            target_date=date.today() + timedelta(days=30),
            created_by=self.employee
        )

    def test_initial_status_is_draft(self):
        """Test that newly created goals start in draft status."""
        goal = self.create_goal()
        self.assertEqual(goal.status, 'draft')

    def test_submit_for_approval_from_draft(self):
        """Test submitting goal for approval from draft status."""
        goal = self.create_goal()
        goal.submit_for_approval()
        self.assertEqual(goal.status, 'pending_approval')

    def test_cannot_submit_non_draft_goal(self):
        """Test that only draft goals can be submitted for approval."""
        goal = self.create_goal(status='active')

        with self.assertRaises(ValidationError) as context:
            goal.submit_for_approval()

        self.assertIn('qaralama', str(context.exception))

    def test_approve_from_pending(self):
        """Test approving a goal from pending_approval status."""
        goal = self.create_goal()
        goal.submit_for_approval()
        goal.approve(self.manager, note='Looks good!')

        self.assertEqual(goal.status, 'active')
        self.assertEqual(goal.approved_by, self.manager)
        self.assertIsNotNone(goal.approved_at)
        self.assertEqual(goal.approval_note, 'Looks good!')

    def test_cannot_approve_non_pending_goal(self):
        """Test that only pending goals can be approved."""
        goal = self.create_goal(status='draft')

        with self.assertRaises(ValidationError) as context:
            goal.approve(self.manager)

        self.assertIn('təsdiq gözləyən', str(context.exception))

    def test_reject_from_pending(self):
        """Test rejecting a goal from pending_approval status."""
        goal = self.create_goal()
        goal.submit_for_approval()
        goal.reject(self.manager, note='Needs more details')

        self.assertEqual(goal.status, 'rejected')
        self.assertEqual(goal.approved_by, self.manager)
        self.assertIsNotNone(goal.approved_at)
        self.assertEqual(goal.approval_note, 'Needs more details')

    def test_cannot_reject_non_pending_goal(self):
        """Test that only pending goals can be rejected."""
        goal = self.create_goal(status='active')

        with self.assertRaises(ValidationError) as context:
            goal.reject(self.manager)

        self.assertIn('təsdiq gözləyən', str(context.exception))

    def test_mark_completed_from_active(self):
        """Test marking goal as completed from active status."""
        goal = self.create_goal()
        goal.submit_for_approval()
        goal.approve(self.manager)
        goal.mark_completed(completion_note='Successfully completed')

        self.assertEqual(goal.status, 'completed')
        self.assertIsNotNone(goal.completion_date)
        self.assertEqual(goal.approval_note, 'Successfully completed')

    def test_cannot_complete_non_active_goal(self):
        """Test that only active goals can be completed."""
        goal = self.create_goal(status='draft')

        with self.assertRaises(ValidationError) as context:
            goal.mark_completed()

        self.assertIn('aktiv', str(context.exception))

    def test_cancel_from_any_status_except_completed(self):
        """Test cancelling goals from various statuses."""
        # Can cancel from draft
        goal1 = self.create_goal(status='draft')
        goal1.cancel(cancel_note='Changed mind')
        self.assertEqual(goal1.status, 'cancelled')

        # Can cancel from pending
        goal2 = self.create_goal()
        goal2.submit_for_approval()
        goal2.cancel(cancel_note='No longer relevant')
        self.assertEqual(goal2.status, 'cancelled')

        # Can cancel from active
        goal3 = self.create_goal()
        goal3.submit_for_approval()
        goal3.approve(self.manager)
        goal3.cancel(cancel_note='Priorities changed')
        self.assertEqual(goal3.status, 'cancelled')

    def test_cannot_cancel_completed_goal(self):
        """Test that completed goals cannot be cancelled."""
        goal = self.create_goal()
        goal.submit_for_approval()
        goal.approve(self.manager)
        goal.mark_completed()

        with self.assertRaises(ValidationError) as context:
            goal.cancel()

        self.assertIn('Tamamlanmış', str(context.exception))

    def test_workflow_complete_cycle(self):
        """Test complete workflow: draft → pending → active → completed."""
        goal = self.create_goal()

        # Step 1: Draft
        self.assertEqual(goal.status, 'draft')

        # Step 2: Submit for approval
        goal.submit_for_approval()
        self.assertEqual(goal.status, 'pending_approval')

        # Step 3: Approve
        goal.approve(self.manager, note='Approved')
        self.assertEqual(goal.status, 'active')

        # Step 4: Complete
        goal.mark_completed(completion_note='Done')
        self.assertEqual(goal.status, 'completed')

    def test_workflow_rejection_cycle(self):
        """Test workflow with rejection: draft → pending → rejected."""
        goal = self.create_goal()

        # Submit for approval
        goal.submit_for_approval()
        self.assertEqual(goal.status, 'pending_approval')

        # Reject
        goal.reject(self.manager, note='Not aligned with company goals')
        self.assertEqual(goal.status, 'rejected')

    def test_workflow_cancellation(self):
        """Test workflow with cancellation at different stages."""
        # Cancel from pending
        goal1 = self.create_goal()
        goal1.submit_for_approval()
        goal1.cancel(cancel_note='User requested cancellation')
        self.assertEqual(goal1.status, 'cancelled')

        # Cancel from active
        goal2 = self.create_goal()
        goal2.submit_for_approval()
        goal2.approve(self.manager)
        goal2.cancel(cancel_note='Role changed')
        self.assertEqual(goal2.status, 'cancelled')

    def test_approval_metadata_persistence(self):
        """Test that approval metadata is properly stored."""
        goal = self.create_goal()
        goal.submit_for_approval()

        approval_note = 'Great goal, well defined'
        goal.approve(self.manager, note=approval_note)

        # Reload from database
        goal.refresh_from_db()

        self.assertEqual(goal.approved_by, self.manager)
        self.assertIsNotNone(goal.approved_at)
        self.assertEqual(goal.approval_note, approval_note)

    def test_completion_date_set_on_completion(self):
        """Test that completion_date is set when goal is marked as completed."""
        goal = self.create_goal()
        goal.submit_for_approval()
        goal.approve(self.manager)

        self.assertIsNone(goal.completion_date)

        goal.mark_completed()

        self.assertIsNotNone(goal.completion_date)
        self.assertEqual(goal.completion_date, date.today())

    def test_state_transitions_are_atomic(self):
        """Test that state transitions don't leave partial state."""
        goal = self.create_goal()
        goal.submit_for_approval()

        try:
            # Try to approve with invalid approver (None)
            goal.approve(None)
        except Exception:
            pass

        # Status should not have changed if approval failed
        goal.refresh_from_db()
        self.assertEqual(goal.status, 'pending_approval')
