"""
Tests for Custom Report Builder functionality.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.evaluations.models import (
    EvaluationCampaign, EvaluationResult, EvaluationAssignment,
    Question, QuestionCategory, Response
)
from apps.departments.models import Department, Position, Organization

User = get_user_model()


class CustomReportBuilderTestCase(TestCase):
    """Test custom report builder view and functionality."""

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

        # Create positions
        self.position1 = Position.objects.create(
            title='Developer',
            code='DEV',
            department=self.dept1,
            organization=self.organization,
            is_active=True
        )
        self.position2 = Position.objects.create(
            title='HR Manager',
            code='HR_MGR',
            department=self.dept2,
            organization=self.organization,
            is_active=True
        )

        # Create users
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='TestPass123!',
            role='admin',
            first_name='Admin',
            last_name='User',
            department=self.dept1,
            position='Developer'
        )

        self.manager = User.objects.create_user(
            username='manager',
            email='manager@test.com',
            password='TestPass123!',
            role='manager',
            first_name='Manager',
            last_name='User',
            department=self.dept1,
            position='Developer'
        )

        self.employee = User.objects.create_user(
            username='employee',
            email='employee@test.com',
            password='TestPass123!',
            role='employee',
            first_name='Employee',
            last_name='User',
            department=self.dept2,
            position='HR Manager'
        )

        # Create campaign
        self.campaign = EvaluationCampaign.objects.create(
            title='Q1 2024 Evaluation',
            description='First quarter evaluation',
            start_date='2024-01-01',
            end_date='2024-03-31',
            status='completed',
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
            text='How effective is the leadership?',
            question_type='scale',
            category=self.category,
            is_active=True
        )

        # Create evaluation results
        self.result1 = EvaluationResult.objects.create(
            campaign=self.campaign,
            evaluatee=self.employee,
            overall_score=4.5,
            self_score=4.2,
            supervisor_score=4.8,
            peer_score=4.3,
            subordinate_score=4.7,
            total_evaluators=5
        )

        self.result2 = EvaluationResult.objects.create(
            campaign=self.campaign,
            evaluatee=self.manager,
            overall_score=3.8,
            self_score=3.5,
            supervisor_score=4.0,
            peer_score=3.9,
            subordinate_score=3.8,
            total_evaluators=4
        )

        # Create assignments and responses
        self.assignment1 = EvaluationAssignment.objects.create(
            campaign=self.campaign,
            evaluator=self.admin,
            evaluatee=self.employee,
            relationship='supervisor',
            status='completed'
        )

        self.response1 = Response.objects.create(
            assignment=self.assignment1,
            question=self.question,
            score=5
        )

        self.client = Client()

    def test_custom_report_builder_get_as_employee(self):
        """Test GET request to custom report builder as employee."""
        self.client.login(username='employee', password='TestPass123!')
        response = self.client.get(reverse('reports:custom-builder'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/custom_report_builder.html')
        self.assertIn('campaigns', response.context)
        self.assertIn('users', response.context)

        # Employee should only see themselves
        users = response.context['users']
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], self.employee)

    def test_custom_report_builder_get_as_manager(self):
        """Test GET request to custom report builder as manager."""
        # Set manager's subordinate
        self.employee.supervisor = self.manager
        self.employee.save()

        self.client.login(username='manager', password='TestPass123!')
        response = self.client.get(reverse('reports:custom-builder'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.context)

        # Manager should see subordinates
        users = list(response.context['users'])
        self.assertIn(self.employee, users)

    def test_custom_report_builder_get_as_admin(self):
        """Test GET request to custom report builder as admin."""
        self.client.login(username='admin', password='TestPass123!')
        response = self.client.get(reverse('reports:custom-builder'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.context)
        self.assertIn('departments', response.context)

        # Admin should see all active users
        users = response.context['users']
        self.assertEqual(users.count(), 3)  # admin, manager, employee

    def test_custom_report_builder_post_with_overall_metrics(self):
        """Test POST request with overall metrics enabled."""
        self.client.login(username='admin', password='TestPass123!')

        post_data = {
            'campaign': self.campaign.pk,
            'include_overall': 'on',
            'chart_types': ['bar']
        }

        response = self.client.post(reverse('reports:custom-builder'), post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/custom_report_view.html')
        self.assertIn('report_data', response.context)
        self.assertIn('summary', response.context['report_data'])
        self.assertIn('overall', response.context['report_data']['summary'])

        # Check overall statistics
        overall = response.context['report_data']['summary']['overall']
        self.assertEqual(overall['total_evaluations'], 2)
        self.assertIsNotNone(overall['avg_score'])
        self.assertIsNotNone(overall['max_score'])
        self.assertIsNotNone(overall['min_score'])

    def test_custom_report_builder_post_with_category_analysis(self):
        """Test POST request with category analysis."""
        self.client.login(username='admin', password='TestPass123!')

        post_data = {
            'campaign': self.campaign.pk,
            'include_category': 'on',
            'chart_types': ['bar']
        }

        response = self.client.post(reverse('reports:custom-builder'), post_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('charts', response.context['report_data'])

        # Check if category chart data exists
        if 'category' in response.context['report_data']['charts']:
            category_chart = response.context['report_data']['charts']['category']
            self.assertIn('labels', category_chart)
            self.assertIn('data', category_chart)

    def test_custom_report_builder_post_with_relationship_analysis(self):
        """Test POST request with relationship type analysis."""
        self.client.login(username='admin', password='TestPass123!')

        post_data = {
            'campaign': self.campaign.pk,
            'include_relationship': 'on',
            'chart_types': ['bar']
        }

        response = self.client.post(reverse('reports:custom-builder'), post_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('charts', response.context['report_data'])

        # Check if relationship chart data exists
        if 'relationship' in response.context['report_data']['charts']:
            relationship_chart = response.context['report_data']['charts']['relationship']
            self.assertIn('labels', relationship_chart)
            self.assertIn('data', relationship_chart)

    def test_custom_report_builder_post_with_trends(self):
        """Test POST request with trend analysis."""
        self.client.login(username='admin', password='TestPass123!')

        post_data = {
            'campaign': self.campaign.pk,
            'include_trends': 'on',
            'chart_types': ['line']
        }

        response = self.client.post(reverse('reports:custom-builder'), post_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('charts', response.context['report_data'])

        # Check if trend chart data exists
        if 'trend' in response.context['report_data']['charts']:
            trend_chart = response.context['report_data']['charts']['trend']
            self.assertIn('labels', trend_chart)
            self.assertIn('data', trend_chart)

    def test_custom_report_builder_post_with_department_filter(self):
        """Test POST request with department filter."""
        self.client.login(username='admin', password='TestPass123!')

        post_data = {
            'campaign': self.campaign.pk,
            'department': self.dept2.pk,
            'include_overall': 'on',
            'chart_types': ['bar']
        }

        response = self.client.post(reverse('reports:custom-builder'), post_data)

        self.assertEqual(response.status_code, 200)

        # Should only show results from dept2 (employee)
        results = response.context['report_data']['results']
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().evaluatee, self.employee)

    def test_custom_report_builder_post_with_user_filter(self):
        """Test POST request with user filter."""
        self.client.login(username='admin', password='TestPass123!')

        post_data = {
            'campaign': self.campaign.pk,
            'users': [self.employee.pk],
            'include_overall': 'on',
            'chart_types': ['bar']
        }

        response = self.client.post(reverse('reports:custom-builder'), post_data)

        self.assertEqual(response.status_code, 200)

        # Should only show results for selected user
        results = response.context['report_data']['results']
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().evaluatee, self.employee)

    def test_custom_report_builder_post_with_multiple_chart_types(self):
        """Test POST request with multiple chart types."""
        self.client.login(username='admin', password='TestPass123!')

        post_data = {
            'campaign': self.campaign.pk,
            'include_overall': 'on',
            'chart_types': ['bar', 'line', 'radar', 'pie']
        }

        response = self.client.post(reverse('reports:custom-builder'), post_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('chart_types', response.context)
        self.assertEqual(len(response.context['chart_types']), 4)

    def test_custom_report_builder_post_with_all_metrics(self):
        """Test POST request with all metrics enabled."""
        self.client.login(username='admin', password='TestPass123!')

        post_data = {
            'campaign': self.campaign.pk,
            'include_overall': 'on',
            'include_category': 'on',
            'include_relationship': 'on',
            'include_trends': 'on',
            'chart_types': ['bar']
        }

        response = self.client.post(reverse('reports:custom-builder'), post_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('report_data', response.context)
        self.assertIn('report_json', response.context)

        # Verify report_json has proper structure
        report_json = response.context['report_json']
        self.assertIn('summary', report_json)
        self.assertIn('charts', report_json)

    def test_custom_report_builder_unauthenticated(self):
        """Test that unauthenticated users are redirected."""
        response = self.client.get(reverse('reports:custom-builder'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_custom_report_builder_no_campaigns(self):
        """Test behavior when no campaigns exist."""
        # Delete all campaigns
        EvaluationCampaign.objects.all().delete()

        self.client.login(username='admin', password='TestPass123!')
        response = self.client.get(reverse('reports:custom-builder'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['campaigns'].count(), 0)

    def test_custom_report_builder_no_results_for_campaign(self):
        """Test behavior when campaign has no results."""
        # Create new campaign with no results
        new_campaign = EvaluationCampaign.objects.create(
            title='Q2 2024 Evaluation',
            description='Second quarter evaluation',
            start_date='2024-04-01',
            end_date='2024-06-30',
            status='active',
            created_by=self.admin
        )

        self.client.login(username='admin', password='TestPass123!')

        post_data = {
            'campaign': new_campaign.pk,
            'include_overall': 'on',
            'chart_types': ['bar']
        }

        response = self.client.post(reverse('reports:custom-builder'), post_data)

        self.assertEqual(response.status_code, 200)

        # Should have 0 results
        overall = response.context['report_data']['summary']['overall']
        self.assertEqual(overall['total_evaluations'], 0)

    def test_custom_report_builder_results_display(self):
        """Test that results are properly displayed in the table."""
        self.client.login(username='admin', password='TestPass123!')

        post_data = {
            'campaign': self.campaign.pk,
            'include_overall': 'on',
            'chart_types': ['bar']
        }

        response = self.client.post(reverse('reports:custom-builder'), post_data)

        self.assertEqual(response.status_code, 200)

        results = response.context['report_data']['results']
        self.assertEqual(results.count(), 2)

        # Check that results have necessary fields
        for result in results:
            self.assertIsNotNone(result.evaluatee)
            # Overall score can be None for incomplete evaluations
            self.assertIsNotNone(result.campaign)
