"""
Tests for proactive feedback suggestions functionality.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from apps.continuous_feedback.models import QuickFeedback
from apps.departments.models import Department, Organization

User = get_user_model()


class ProactiveFeedbackSuggestionsTestCase(TestCase):
    """Test proactive feedback suggestions view and functionality."""

    def setUp(self):
        """Set up test data."""
        # Create organization
        self.organization = Organization.objects.create(
            name='Test Organization',
            short_name='TestOrg'
        )

        # Create departments
        self.dept1 = Department.objects.create(
            name='IT Department',
            code='IT',
            organization=self.organization,
            is_active=True
        )

        self.dept2 = Department.objects.create(
            name='HR Department',
            code='HR',
            organization=self.organization,
            is_active=True
        )

        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123!',
            role='manager',
            first_name='Test',
            last_name='User',
            department=self.dept1,
            position='Manager'
        )

        # Team member 1 - same department
        self.team_member1 = User.objects.create_user(
            username='team1',
            email='team1@test.com',
            password='TestPass123!',
            role='employee',
            first_name='Team',
            last_name='Member1',
            department=self.dept1,
            position='Developer',
            supervisor=self.user
        )

        # Team member 2 - same department
        self.team_member2 = User.objects.create_user(
            username='team2',
            email='team2@test.com',
            password='TestPass123!',
            role='employee',
            first_name='Team',
            last_name='Member2',
            department=self.dept1,
            position='Developer'
        )

        # Different department user (should not appear in suggestions)
        self.other_dept_user = User.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='TestPass123!',
            role='employee',
            first_name='Other',
            last_name='User',
            department=self.dept2,
            position='HR Manager'
        )

        # Supervisor
        self.supervisor = User.objects.create_user(
            username='supervisor',
            email='supervisor@test.com',
            password='TestPass123!',
            role='manager',
            first_name='Super',
            last_name='Visor',
            department=self.dept1,
            position='Director'
        )
        self.user.supervisor = self.supervisor
        self.user.save()

        self.client = Client()

    def test_proactive_suggestions_view_authenticated(self):
        """Test that authenticated users can access suggestions page."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'continuous_feedback/proactive_suggestions.html')

    def test_proactive_suggestions_view_unauthenticated(self):
        """Test that unauthenticated users are redirected."""
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_suggestions_include_team_members(self):
        """Test that suggestions include team members from same department."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']
        team_member_ids = [s['user'].id for s in suggestions]

        self.assertIn(self.team_member1.id, team_member_ids)
        self.assertIn(self.team_member2.id, team_member_ids)

    def test_suggestions_exclude_different_department(self):
        """Test that suggestions exclude users from different departments."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']
        user_ids = [s['user'].id for s in suggestions]

        self.assertNotIn(self.other_dept_user.id, user_ids)

    def test_suggestions_include_supervisor(self):
        """Test that suggestions include the user's supervisor."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']
        user_ids = [s['user'].id for s in suggestions]

        self.assertIn(self.supervisor.id, user_ids)

    def test_high_priority_for_no_feedback(self):
        """Test that users with no feedback history get high priority."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']

        # Find team_member1 in suggestions
        member1_suggestion = next((s for s in suggestions if s['user'].id == self.team_member1.id), None)

        self.assertIsNotNone(member1_suggestion)
        self.assertEqual(member1_suggestion['priority'], 'high')

    def test_high_priority_for_old_feedback(self):
        """Test that users not given feedback in 30+ days get high priority."""
        # Create old feedback
        old_date = timezone.now() - timedelta(days=35)
        feedback = QuickFeedback.objects.create(
            sender=self.user,
            recipient=self.team_member1,
            feedback_type='recognition',
            visibility='private',
            title='Old Feedback',
            message='This is old'
        )
        # Update created_at using queryset to bypass auto_now_add
        QuickFeedback.objects.filter(id=feedback.id).update(created_at=old_date)

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']
        member1_suggestion = next((s for s in suggestions if s['user'].id == self.team_member1.id), None)

        self.assertEqual(member1_suggestion['priority'], 'high')

    def test_medium_priority_for_recent_feedback(self):
        """Test that users given feedback 14-30 days ago get medium priority."""
        # Use team_member2 who is not a subordinate
        # Create feedback 20 days ago
        recent_date = timezone.now() - timedelta(days=20)
        feedback = QuickFeedback.objects.create(
            sender=self.user,
            recipient=self.team_member2,  # Changed to team_member2 to avoid subordinate logic
            feedback_type='recognition',
            visibility='private',
            title='Recent Feedback',
            message='This is recent'
        )
        QuickFeedback.objects.filter(id=feedback.id).update(created_at=recent_date)

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']
        member2_suggestion = next((s for s in suggestions if s['user'].id == self.team_member2.id), None)

        self.assertEqual(member2_suggestion['priority'], 'medium')

    def test_low_priority_for_very_recent_feedback(self):
        """Test that users given feedback <14 days ago get low priority."""
        # Create feedback 5 days ago
        very_recent_date = timezone.now() - timedelta(days=5)
        feedback = QuickFeedback.objects.create(
            sender=self.user,
            recipient=self.team_member1,
            feedback_type='recognition',
            visibility='private',
            title='Very Recent Feedback',
            message='This is very recent'
        )
        QuickFeedback.objects.filter(id=feedback.id).update(created_at=very_recent_date)

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']
        member1_suggestion = next((s for s in suggestions if s['user'].id == self.team_member1.id), None)

        self.assertEqual(member1_suggestion['priority'], 'low')

    def test_suggestions_sorted_by_priority(self):
        """Test that suggestions are sorted by priority (high first)."""
        # Create feedback with different ages
        feedback = QuickFeedback.objects.create(
            sender=self.user,
            recipient=self.team_member1,
            feedback_type='recognition',
            visibility='private',
            title='Feedback',
            message='Message'
        )
        QuickFeedback.objects.filter(id=feedback.id).update(created_at=timezone.now() - timedelta(days=5))

        # team_member2 will be high priority (no feedback)

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']

        # First suggestions should be high priority
        if len(suggestions) > 0:
            self.assertEqual(suggestions[0]['priority'], 'high')

    def test_feedback_statistics_calculation(self):
        """Test that feedback statistics are calculated correctly."""
        # Create some feedback
        QuickFeedback.objects.create(
            sender=self.user,
            recipient=self.team_member1,
            feedback_type='recognition',
            visibility='private',
            title='Feedback 1',
            message='Message 1'
        )

        QuickFeedback.objects.create(
            sender=self.user,
            recipient=self.team_member2,
            feedback_type='improvement',
            visibility='private',
            title='Feedback 2',
            message='Message 2'
        )

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        stats = response.context['feedback_stats']

        self.assertEqual(stats['total_sent'], 2)
        self.assertEqual(stats['recognitions_sent'], 1)
        self.assertIsNotNone(stats['last_feedback_date'])

    def test_engagement_score_calculation(self):
        """Test that engagement score is calculated correctly."""
        # Create 5 feedback items this month
        for i in range(5):
            QuickFeedback.objects.create(
                sender=self.user,
                recipient=self.team_member1,
                feedback_type='recognition',
                visibility='private',
                title=f'Feedback {i}',
                message=f'Message {i}'
            )

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        engagement_score = response.context['engagement_score']

        # 5 feedback * 10 = 50
        self.assertEqual(engagement_score, 50)

    def test_engagement_score_max_100(self):
        """Test that engagement score maxes out at 100."""
        # Create 15 feedback items this month
        for i in range(15):
            QuickFeedback.objects.create(
                sender=self.user,
                recipient=self.team_member1,
                feedback_type='recognition',
                visibility='private',
                title=f'Feedback {i}',
                message=f'Message {i}'
            )

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        engagement_score = response.context['engagement_score']

        # Should be capped at 100
        self.assertEqual(engagement_score, 100)

    def test_milestones_achievement(self):
        """Test that milestones are correctly marked as achieved."""
        # Create 10 feedback items
        for i in range(10):
            QuickFeedback.objects.create(
                sender=self.user,
                recipient=self.team_member1,
                feedback_type='recognition',
                visibility='private',
                title=f'Feedback {i}',
                message=f'Message {i}'
            )

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        milestones = response.context['milestones']

        # First milestone (10 feedback) should be achieved
        first_milestone = next((m for m in milestones if m['count'] == 10), None)
        self.assertTrue(first_milestone['achieved'])

        # Second milestone (25 feedback) should not be achieved
        second_milestone = next((m for m in milestones if m['count'] == 25), None)
        self.assertFalse(second_milestone['achieved'])

    def test_priority_counts(self):
        """Test that priority counts are calculated correctly."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        high_priority_count = response.context['high_priority_count']
        medium_priority_count = response.context['medium_priority_count']

        # Should have at least team members + supervisor as high priority (no feedback yet)
        self.assertGreaterEqual(high_priority_count, 2)

    def test_suggestions_limited_to_15(self):
        """Test that suggestions are limited to top 15."""
        # Create many team members
        for i in range(20):
            User.objects.create_user(
                username=f'extrauser{i}',
                email=f'extra{i}@test.com',
                password='TestPass123!',
                role='employee',
                first_name=f'Extra{i}',
                last_name='User',
                department=self.dept1,
                position='Developer'
            )

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']

        # Should be limited to 15
        self.assertLessEqual(len(suggestions), 15)

    def test_user_without_department(self):
        """Test behavior when user has no department."""
        # Create user without department
        no_dept_user = User.objects.create_user(
            username='nodept',
            email='nodept@test.com',
            password='TestPass123!',
            role='employee',
            first_name='No',
            last_name='Department',
            position='Freelancer'
        )

        self.client.login(username='nodept', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        # Should not crash, but may have limited suggestions
        self.assertEqual(response.status_code, 200)
        suggestions = response.context['suggestions']

        # Should have empty or very limited suggestions
        self.assertIsInstance(suggestions, list)

    def test_days_since_feedback_calculation(self):
        """Test that days since feedback is calculated correctly."""
        # Create feedback 10 days ago
        feedback_date = timezone.now() - timedelta(days=10)
        feedback = QuickFeedback.objects.create(
            sender=self.user,
            recipient=self.team_member1,
            feedback_type='recognition',
            visibility='private',
            title='Feedback',
            message='Message'
        )
        QuickFeedback.objects.filter(id=feedback.id).update(created_at=feedback_date)

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']
        member1_suggestion = next((s for s in suggestions if s['user'].id == self.team_member1.id), None)

        # Should be approximately 10 days
        self.assertAlmostEqual(member1_suggestion['days_since_feedback'], 10, delta=1)

    def test_relationship_labels(self):
        """Test that relationship labels are correctly assigned."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions = response.context['suggestions']

        # Team member should be labeled as "Həmkar"
        member_suggestion = next((s for s in suggestions if s['user'].id == self.team_member1.id), None)
        self.assertEqual(member_suggestion['relationship'], 'Həmkar')

        # Supervisor should be labeled as "Rəhbər"
        supervisor_suggestion = next((s for s in suggestions if s['user'].id == self.supervisor.id), None)
        self.assertEqual(supervisor_suggestion['relationship'], 'Rəhbər')

    def test_multiple_users_suggestions_isolated(self):
        """Test that users only see their own personalized suggestions."""
        # Login as team_member1
        self.client.login(username='team1', password='TestPass123!')
        response1 = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions1 = response1.context['suggestions']
        user_ids1 = [s['user'].id for s in suggestions1]

        # Should not include themselves
        self.assertNotIn(self.team_member1.id, user_ids1)

        # Login as testuser
        self.client.login(username='testuser', password='TestPass123!')
        response2 = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        suggestions2 = response2.context['suggestions']
        user_ids2 = [s['user'].id for s in suggestions2]

        # Should not include themselves
        self.assertNotIn(self.user.id, user_ids2)

    def test_no_feedback_stats_for_new_user(self):
        """Test statistics when user has never sent feedback."""
        new_user = User.objects.create_user(
            username='newuser',
            email='new@test.com',
            password='TestPass123!',
            role='employee',
            first_name='New',
            last_name='User',
            department=self.dept1,
            position='Intern'
        )

        self.client.login(username='newuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        stats = response.context['feedback_stats']

        self.assertEqual(stats['total_sent'], 0)
        self.assertEqual(stats['this_month'], 0)
        self.assertEqual(stats['recognitions_sent'], 0)
        self.assertIsNone(stats['last_feedback_date'])

    def test_engagement_score_zero_for_new_user(self):
        """Test that new users have engagement score of 0."""
        new_user = User.objects.create_user(
            username='newuser',
            email='new@test.com',
            password='TestPass123!',
            role='employee',
            first_name='New',
            last_name='User',
            department=self.dept1,
            position='Intern'
        )

        self.client.login(username='newuser', password='TestPass123!')
        response = self.client.get(reverse('continuous_feedback:proactive-suggestions'))

        engagement_score = response.context['engagement_score']
        self.assertEqual(engagement_score, 0)
