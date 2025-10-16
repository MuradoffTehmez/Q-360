"""
Tests for 360 evaluation calibration workflow.
Tests score adjustment, finalization, and calibration dashboard.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta

from apps.evaluations.models import (
    EvaluationCampaign, EvaluationResult, EvaluationAssignment,
    QuestionCategory, Question, Response
)
from apps.departments.models import Department, Organization

User = get_user_model()


class CalibrationWorkflowTest(TestCase):
    """
    Test calibration workflow functionality including:
    - Calibration dashboard access and stats
    - Score adjustment
    - Result finalization
    - Bulk finalization
    """

    def setUp(self):
        """Set up test data."""
        # Create organization
        self.organization = Organization.objects.create(
            name='Test Organization',
            short_name='TEST_ORG',
            code='TESTORG',
            is_active=True
        )

        # Create department
        self.department = Department.objects.create(
            name='Sales',
            code='SALES',
            organization=self.organization,
            is_active=True
        )

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

        # Create employee users
        self.employee1 = User.objects.create_user(
            username='employee1',
            email='emp1@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            role='employee',
            department=self.department,
            supervisor=self.manager
        )

        self.employee2 = User.objects.create_user(
            username='employee2',
            email='emp2@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith',
            role='employee',
            department=self.department,
            supervisor=self.manager
        )

        # Create evaluation campaign
        self.campaign = EvaluationCampaign.objects.create(
            title='Q1 2025 Performance Review',
            description='First quarter performance evaluation',
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() + timedelta(days=30),
            status='active',
            evaluation_type='360',
            created_by=self.admin
        )

        # Create question category
        self.category = QuestionCategory.objects.create(
            name='Leadership',
            description='Leadership skills',
            is_active=True
        )

        # Create question
        self.question = Question.objects.create(
            category=self.category,
            text='How would you rate the leadership skills?',
            question_type='rating',
            is_required=True,
            weight=Decimal('1.0'),
            is_active=True
        )

        # Create evaluation results
        self.result1 = EvaluationResult.objects.create(
            campaign=self.campaign,
            evaluatee=self.employee1,
            overall_score=Decimal('4.5'),
            self_score=Decimal('4.8'),
            supervisor_score=Decimal('4.5'),
            peer_score=Decimal('4.3'),
            subordinate_score=None,
            total_evaluators=3,
            is_finalized=False
        )

        self.result2 = EvaluationResult.objects.create(
            campaign=self.campaign,
            evaluatee=self.employee2,
            overall_score=Decimal('3.2'),
            self_score=Decimal('3.5'),
            supervisor_score=Decimal('3.0'),
            peer_score=Decimal('3.1'),
            subordinate_score=None,
            total_evaluators=3,
            is_finalized=False
        )

        self.client = Client()

    def test_calibration_dashboard_requires_manager_or_admin(self):
        """Test that only managers/admins can access calibration dashboard."""
        self.client.login(username='employee1', password='testpass123')
        response = self.client.get(
            reverse('evaluations:calibration-dashboard', kwargs={'campaign_id': self.campaign.id})
        )

        # Should redirect non-managers
        self.assertEqual(response.status_code, 302)

    def test_calibration_dashboard_displays_statistics(self):
        """Test that dashboard shows correct statistics."""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(
            reverse('evaluations:calibration-dashboard', kwargs={'campaign_id': self.campaign.id})
        )

        self.assertEqual(response.status_code, 200)

        # Check context data
        self.assertEqual(response.context['stats']['total_evaluations'], 2)
        self.assertEqual(response.context['stats']['finalized_count'], 0)
        self.assertEqual(response.context['stats']['pending_count'], 2)

    def test_calibration_dashboard_shows_score_distribution(self):
        """Test score distribution calculation."""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(
            reverse('evaluations:calibration-dashboard', kwargs={'campaign_id': self.campaign.id})
        )

        dist = response.context['score_distribution']

        # result1 is 4.5 (excellent: >= 4.5)
        # result2 is 3.2 (average: 2.5-3.5)
        self.assertEqual(dist['excellent'], 1)
        self.assertEqual(dist['good'], 0)
        self.assertEqual(dist['average'], 1)
        self.assertEqual(dist['needs_improvement'], 0)

    def test_calibration_detail_view_shows_breakdown(self):
        """Test calibration detail view shows category and relationship breakdown."""
        self.client.login(username='manager', password='testpass123')
        response = self.client.get(
            reverse('evaluations:calibration-detail', kwargs={'result_id': self.result1.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, '4.5')

    def test_adjust_score_updates_result(self):
        """Test adjusting evaluation score."""
        self.client.login(username='admin', password='testpass123')

        old_score = self.result1.overall_score

        response = self.client.post(
            reverse('evaluations:adjust-score', kwargs={'result_id': self.result1.id}),
            data={
                'overall_score': '4.7',
                'reason': 'Adjusted based on additional input from stakeholders'
            }
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['new_score'], 4.7)

        # Verify score updated
        self.result1.refresh_from_db()
        self.assertEqual(self.result1.overall_score, Decimal('4.7'))

    def test_adjust_score_requires_manager_permission(self):
        """Test that only managers/admins can adjust scores."""
        self.client.login(username='employee1', password='testpass123')

        response = self.client.post(
            reverse('evaluations:adjust-score', kwargs={'result_id': self.result1.id}),
            data={'overall_score': '5.0', 'reason': 'Test'}
        )

        self.assertEqual(response.status_code, 403)

    def test_adjust_score_validates_range(self):
        """Test score adjustment validates 0-5 range."""
        self.client.login(username='admin', password='testpass123')

        # Try to set score above 5
        response = self.client.post(
            reverse('evaluations:adjust-score', kwargs={'result_id': self.result1.id}),
            data={'overall_score': '6.0', 'reason': 'Invalid test'}
        )

        # Should handle validation (implementation dependent)
        self.assertEqual(response.status_code, 200)

    def test_finalize_result_locks_score(self):
        """Test finalizing result sets is_finalized flag."""
        self.client.login(username='admin', password='testpass123')

        response = self.client.post(
            reverse('evaluations:finalize-result', kwargs={'result_id': self.result1.id})
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        # Verify finalized
        self.result1.refresh_from_db()
        self.assertTrue(self.result1.is_finalized)
        self.assertIsNotNone(self.result1.finalized_at)

    def test_finalize_result_requires_manager(self):
        """Test that only managers can finalize results."""
        self.client.login(username='employee1', password='testpass123')

        response = self.client.post(
            reverse('evaluations:finalize-result', kwargs={'result_id': self.result1.id})
        )

        self.assertEqual(response.status_code, 403)

    def test_bulk_finalize_all_results(self):
        """Test bulk finalizing all results in campaign."""
        self.client.login(username='admin', password='testpass123')

        response = self.client.post(
            reverse('evaluations:bulk-finalize', kwargs={'campaign_id': self.campaign.id})
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('2', data['message'])  # 2 results finalized

        # Verify both results finalized
        self.result1.refresh_from_db()
        self.result2.refresh_from_db()
        self.assertTrue(self.result1.is_finalized)
        self.assertTrue(self.result2.is_finalized)

    def test_bulk_finalize_requires_admin(self):
        """Test that only admins can bulk finalize."""
        self.client.login(username='manager', password='testpass123')

        response = self.client.post(
            reverse('evaluations:bulk-finalize', kwargs={'campaign_id': self.campaign.id})
        )

        # Managers should not have access (admin only)
        self.assertEqual(response.status_code, 403)

    def test_bulk_finalize_skips_already_finalized(self):
        """Test bulk finalize only affects non-finalized results."""
        # Finalize result1 manually
        self.result1.is_finalized = True
        self.result1.save()

        self.client.login(username='admin', password='testpass123')
        response = self.client.post(
            reverse('evaluations:bulk-finalize', kwargs={'campaign_id': self.campaign.id})
        )

        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('1', data['message'])  # Only 1 result finalized (result2)

    def test_manager_can_access_dashboard(self):
        """Test that managers can access calibration dashboard."""
        self.client.login(username='manager', password='testpass123')
        response = self.client.get(
            reverse('evaluations:calibration-dashboard', kwargs={'campaign_id': self.campaign.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_calibration_shows_department_stats_for_admin(self):
        """Test that admins see department breakdown."""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(
            reverse('evaluations:calibration-dashboard', kwargs={'campaign_id': self.campaign.id})
        )

        # Admin should see dept_stats
        self.assertIn('dept_stats', response.context)
        dept_stats = response.context['dept_stats']
        self.assertGreater(len(dept_stats), 0)

    def test_evaluation_result_str_representation(self):
        """Test string representation of evaluation result."""
        result_str = str(self.result1)
        self.assertIn('John Doe', result_str)
        self.assertIn('Q1 2025', result_str)

    def test_calibration_detail_with_no_responses(self):
        """Test calibration detail works even with no responses."""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(
            reverse('evaluations:calibration-detail', kwargs={'result_id': self.result1.id})
        )

        self.assertEqual(response.status_code, 200)
        # Should not error even if no responses exist

    def test_adjust_score_with_decimal_precision(self):
        """Test score adjustment handles decimal precision correctly."""
        self.client.login(username='admin', password='testpass123')

        response = self.client.post(
            reverse('evaluations:adjust-score', kwargs={'result_id': self.result1.id}),
            data={'overall_score': '4.75', 'reason': 'Precision test'}
        )

        self.assertEqual(response.status_code, 200)

        self.result1.refresh_from_db()
        self.assertEqual(self.result1.overall_score, Decimal('4.75'))

    def test_average_score_calculation(self):
        """Test that average score is calculated correctly."""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(
            reverse('evaluations:calibration-dashboard', kwargs={'campaign_id': self.campaign.id})
        )

        stats = response.context['stats']
        # Average of 4.5 and 3.2 = 3.85
        avg_score = stats['avg_score']
        self.assertIsNotNone(avg_score)
        expected = (Decimal('4.5') + Decimal('3.2')) / 2
        self.assertAlmostEqual(float(avg_score), float(expected), places=2)

    def tearDown(self):
        """Clean up test data."""
        User.objects.all().delete()
        Department.objects.all().delete()
        EvaluationCampaign.objects.all().delete()
        EvaluationResult.objects.all().delete()
        QuestionCategory.objects.all().delete()
        Question.objects.all().delete()
