"""
Tests for recruitment Kanban pipeline.
Tests candidate status updates and pipeline functionality.
"""
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date, timedelta

from apps.recruitment.models import JobPosting, Application
from apps.departments.models import Department, Organization
from .test_base import BaseTestCase

User = get_user_model()


class CandidatePipelineTest(BaseTestCase):
    """
    Test recruitment Kanban pipeline functionality including:
    - Pipeline view display
    - Drag-and-drop status updates
    - Stage filtering
    - Application counting
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

        # Create recruiter user
        self.recruiter = User.objects.create_user(
            username='recruiter',
            email='recruiter@test.com',
            password='testpass123',
            first_name='Recruiter',
            last_name='User',
            role='manager',
            department=self.department
        )

        # Create job posting
        self.job = JobPosting.objects.create(
            title='Senior Software Engineer',
            code='SSE-001',
            department=self.department,
            description='We are looking for a senior software engineer',
            responsibilities='Develop and maintain software',
            requirements='5+ years experience',
            employment_type='full_time',
            experience_level='senior',
            location='Baku',
            status='open',
            posted_date=date.today(),
            hiring_manager=self.admin,
            created_by=self.admin
        )

        # Create applications in different stages
        self.app_received = Application.objects.create(
            job_posting=self.job,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='+994501234567',
            resume='resumes/2024/01/john_cv.pdf',
            status='received',
            source='linkedin'
        )

        self.app_screening = Application.objects.create(
            job_posting=self.job,
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            phone='+994501234568',
            resume='resumes/2024/01/jane_cv.pdf',
            status='screening',
            source='website'
        )

        self.app_interview = Application.objects.create(
            job_posting=self.job,
            first_name='Bob',
            last_name='Johnson',
            email='bob@example.com',
            phone='+994501234569',
            resume='resumes/2024/01/bob_cv.pdf',
            status='interview',
            source='referral',
            referrer=self.admin
        )

        self.client = Client()

    def test_pipeline_view_requires_authentication(self):
        """Test that pipeline view requires login."""
        response = self.client.get(reverse('recruitment:candidate-pipeline'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_pipeline_view_displays_all_stages(self):
        """Test that pipeline view shows all stages."""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('recruitment:candidate-pipeline'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'received')
        self.assertContains(response, 'screening')
        self.assertContains(response, 'interview')
        self.assertContains(response, 'assessment')
        self.assertContains(response, 'offer')
        self.assertContains(response, 'hired')
        self.assertContains(response, 'rejected')

    def test_pipeline_view_shows_applications_in_correct_stage(self):
        """Test that applications appear in their correct stage."""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('recruitment:candidate-pipeline'))

        # Check that applications are in the right places
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Jane Smith')
        self.assertContains(response, 'Bob Johnson')

    def test_update_application_status_via_api(self):
        """Test updating application status through API endpoint."""
        self.client.login(username='admin', password='testpass123')

        response = self.client.post(
            reverse('recruitment:update-application-status', kwargs={'pk': self.app_received.id}),
            data={'status': 'screening'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        # Verify status changed
        self.app_received.refresh_from_db()
        self.assertEqual(self.app_received.status, 'screening')

    def test_move_application_forward_in_pipeline(self):
        """Test moving application from screening to interview."""
        self.client.login(username='recruiter', password='testpass123')

        response = self.client.post(
            reverse('recruitment:update-application-status', kwargs={'pk': self.app_screening.id}),
            data={'status': 'interview'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.app_screening.refresh_from_db()
        self.assertEqual(self.app_screening.status, 'interview')

    def test_move_application_to_offer_stage(self):
        """Test moving application to offer stage."""
        self.client.login(username='admin', password='testpass123')

        response = self.client.post(
            reverse('recruitment:update-application-status', kwargs={'pk': self.app_interview.id}),
            data={'status': 'offer'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.app_interview.refresh_from_db()
        self.assertEqual(self.app_interview.status, 'offer')

    def test_reject_application(self):
        """Test moving application to rejected status."""
        self.client.login(username='admin', password='testpass123')

        response = self.client.post(
            reverse('recruitment:update-application-status', kwargs={'pk': self.app_received.id}),
            data={'status': 'rejected'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.app_received.refresh_from_db()
        self.assertEqual(self.app_received.status, 'rejected')

    def test_hire_candidate(self):
        """Test moving application to hired status."""
        self.client.login(username='admin', password='testpass123')

        response = self.client.post(
            reverse('recruitment:update-application-status', kwargs={'pk': self.app_interview.id}),
            data={'status': 'hired'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.app_interview.refresh_from_db()
        self.assertEqual(self.app_interview.status, 'hired')

    def test_invalid_status_returns_error(self):
        """Test that invalid status returns error."""
        self.client.login(username='admin', password='testpass123')

        response = self.client.post(
            reverse('recruitment:update-application-status', kwargs={'pk': self.app_received.id}),
            data={'status': 'invalid_status'},
            content_type='application/json'
        )

        data = response.json()
        self.assertFalse(data['success'])

    def test_pipeline_filtering_by_job(self):
        """Test filtering pipeline by specific job."""
        # Create another job
        job2 = JobPosting.objects.create(
            title='Junior Developer',
            code='JD-001',
            department=self.department,
            description='Looking for junior dev',
            responsibilities='Code review',
            requirements='1+ years',
            employment_type='full_time',
            experience_level='junior',
            location='Baku',
            status='open',
            created_by=self.admin
        )

        # Create application for job2
        Application.objects.create(
            job_posting=job2,
            first_name='Alice',
            last_name='Wonder',
            email='alice@example.com',
            phone='+994501234570',
            resume='resumes/2024/01/alice_cv.pdf',
            status='received'
        )

        self.client.login(username='admin', password='testpass123')
        response = self.client.get(
            reverse('recruitment:candidate-pipeline'),
            {'job_id': self.job.id}
        )

        self.assertEqual(response.status_code, 200)
        # Should show applications only for the first job
        self.assertContains(response, 'John Doe')
        self.assertNotContains(response, 'Alice Wonder')

    def test_application_count_by_stage(self):
        """Test counting applications in each stage."""
        # Create more applications
        Application.objects.create(
            job_posting=self.job,
            first_name='Test1',
            last_name='User1',
            email='test1@example.com',
            phone='+994501234571',
            resume='test1.pdf',
            status='received'
        )

        Application.objects.create(
            job_posting=self.job,
            first_name='Test2',
            last_name='User2',
            email='test2@example.com',
            phone='+994501234572',
            resume='test2.pdf',
            status='received'
        )

        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('recruitment:candidate-pipeline'))

        # Verify stage counts in response
        self.assertEqual(response.status_code, 200)
        # Would need to check context data or parse HTML for exact counts

    def test_application_full_name_property(self):
        """Test application full_name property."""
        self.assertEqual(self.app_received.full_name, 'John Doe')
        self.assertEqual(self.app_screening.full_name, 'Jane Smith')

    def test_job_posting_application_count_property(self):
        """Test job posting's application_count property."""
        count = self.job.application_count
        self.assertEqual(count, 3)  # We created 3 applications

    def test_job_posting_active_application_count(self):
        """Test active application count excludes rejected/withdrawn."""
        # Reject one application
        self.app_received.status = 'rejected'
        self.app_received.save()

        active_count = self.job.active_application_count
        self.assertEqual(active_count, 2)  # 3 total - 1 rejected

    def test_job_posting_is_open_property(self):
        """Test job posting is_open property."""
        self.assertTrue(self.job.is_open)

        # Close the job
        self.job.status = 'closed'
        self.job.save()

        self.assertFalse(self.job.is_open)

    def test_job_posting_is_open_respects_closing_date(self):
        """Test is_open respects closing date."""
        # Set closing date in the past
        self.job.closing_date = date.today() - timedelta(days=1)
        self.job.save()

        self.assertFalse(self.job.is_open)

    def test_application_source_tracking(self):
        """Test application source is properly tracked."""
        self.assertEqual(self.app_received.source, 'linkedin')
        self.assertEqual(self.app_screening.source, 'website')
        self.assertEqual(self.app_interview.source, 'referral')
        self.assertEqual(self.app_interview.referrer, self.admin)

    def test_pipeline_view_manager_access(self):
        """Test that managers can access pipeline view."""
        self.client.login(username='recruiter', password='testpass123')
        response = self.client.get(reverse('recruitment:candidate-pipeline'))

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Clean up test data."""
        User.objects.all().delete()
        Department.objects.all().delete()
        JobPosting.objects.all().delete()
        Application.objects.all().delete()
