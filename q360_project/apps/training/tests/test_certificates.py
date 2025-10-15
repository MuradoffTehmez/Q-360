"""
Tests for certificate management functionality.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.training.models import TrainingResource, UserTraining
from apps.departments.models import Department, Organization

User = get_user_model()


class CertificateManagementTestCase(TestCase):
    """Test certificate management view and functionality."""

    def setUp(self):
        """Set up test data."""
        # Create organization
        self.organization = Organization.objects.create(
            name='Test Organization',
            short_name='TestOrg'
        )

        # Create department
        self.department = Department.objects.create(
            name='IT Department',
            code='IT',
            organization=self.organization,
            is_active=True
        )

        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123!',
            role='employee',
            first_name='Test',
            last_name='User',
            department=self.department,
            position='Developer'
        )

        # Create training resources
        self.training1 = TrainingResource.objects.create(
            title='Python Programming',
            description='Learn Python',
            type='course',
            is_active=True
        )

        self.training2 = TrainingResource.objects.create(
            title='Django Framework',
            description='Learn Django',
            type='certification',
            is_active=True
        )

        self.training3 = TrainingResource.objects.create(
            title='React Basics',
            description='Learn React',
            type='course',
            is_active=True
        )

        # Create user trainings - completed with certificate
        self.user_training1 = UserTraining.objects.create(
            user=self.user,
            resource=self.training1,
            status='completed',
            progress_percentage=100,
            completed_date=timezone.now().date(),
            certificate_url='https://example.com/cert1.pdf'
        )

        # Completed without certificate
        self.user_training2 = UserTraining.objects.create(
            user=self.user,
            resource=self.training2,
            status='completed',
            progress_percentage=100,
            completed_date=timezone.now().date()
        )

        # In progress (should not appear)
        self.user_training3 = UserTraining.objects.create(
            user=self.user,
            resource=self.training3,
            status='in_progress',
            progress_percentage=50
        )

        self.client = Client()

    def test_my_certificates_view_authenticated(self):
        """Test that authenticated users can access certificates page."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'training/my_certificates.html')

    def test_my_certificates_view_unauthenticated(self):
        """Test that unauthenticated users are redirected."""
        response = self.client.get(reverse('training:my-certificates'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_certificates_statistics(self):
        """Test that statistics are calculated correctly."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        self.assertEqual(response.context['total_completed'], 2)
        self.assertEqual(response.context['with_certificates'], 1)
        self.assertEqual(response.context['without_certificates'], 1)
        self.assertEqual(response.context['certificate_rate'], 50.0)

    def test_trainings_with_certificates_listed(self):
        """Test that trainings with certificates are listed."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        trainings_with_certs = response.context['trainings_with_certificates']
        self.assertEqual(trainings_with_certs.count(), 1)
        self.assertEqual(trainings_with_certs.first(), self.user_training1)

    def test_trainings_without_certificates_listed(self):
        """Test that completed trainings without certificates are listed."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        trainings_without_certs = response.context['trainings_without_certificates']
        self.assertEqual(trainings_without_certs.count(), 1)
        self.assertEqual(trainings_without_certs.first(), self.user_training2)

    def test_in_progress_trainings_not_listed(self):
        """Test that in-progress trainings are not listed."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        all_trainings = list(response.context['trainings_with_certificates']) + \
                       list(response.context['trainings_without_certificates'])

        self.assertNotIn(self.user_training3, all_trainings)

    def test_recent_certificates(self):
        """Test that recent certificates are shown."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        recent = response.context['recent_certificates']
        self.assertLessEqual(len(recent), 5)
        self.assertIn(self.user_training1, recent)

    def test_training_types_distribution(self):
        """Test that training types are correctly distributed."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        training_types = response.context['training_types']
        self.assertIn('Kurs', training_types)
        self.assertEqual(training_types['Kurs'], 1)

    def test_no_completed_trainings(self):
        """Test behavior when user has no completed trainings."""
        # Create new user with no completed trainings
        new_user = User.objects.create_user(
            username='newuser',
            email='new@test.com',
            password='TestPass123!',
            role='employee',
            first_name='New',
            last_name='User',
            department=self.department,
            position='Tester'
        )

        self.client.login(username='newuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        self.assertEqual(response.context['total_completed'], 0)
        self.assertEqual(response.context['with_certificates'], 0)
        self.assertEqual(response.context['without_certificates'], 0)
        self.assertEqual(response.context['certificate_rate'], 0)

    def test_all_trainings_have_certificates(self):
        """Test when all completed trainings have certificates."""
        # Add certificate to training2
        self.user_training2.certificate_url = 'https://example.com/cert2.pdf'
        self.user_training2.save()

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        self.assertEqual(response.context['with_certificates'], 2)
        self.assertEqual(response.context['without_certificates'], 0)
        self.assertEqual(response.context['certificate_rate'], 100.0)

    def test_certificate_url_empty_string(self):
        """Test that empty string certificate URLs are treated as no certificate."""
        self.user_training1.certificate_url = ''
        self.user_training1.save()

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        self.assertEqual(response.context['with_certificates'], 0)
        self.assertEqual(response.context['without_certificates'], 2)

    def test_trainings_ordered_by_completion_date(self):
        """Test that trainings are ordered by completion date (newest first)."""
        # Create additional training
        training4 = TrainingResource.objects.create(
            title='Advanced Python',
            description='Advanced Python',
            type='course',
            is_active=True
        )

        # Create older completed training with certificate
        older_training = UserTraining.objects.create(
            user=self.user,
            resource=training4,
            status='completed',
            progress_percentage=100,
            completed_date=timezone.now().date() - timezone.timedelta(days=30),
            certificate_url='https://example.com/cert3.pdf'
        )

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        trainings_with_certs = response.context['trainings_with_certificates']
        # Newest should be first
        self.assertEqual(trainings_with_certs.first(), self.user_training1)
        self.assertEqual(trainings_with_certs.last(), older_training)

    def test_multiple_users_certificates_isolated(self):
        """Test that users only see their own certificates."""
        # Create another user with certificates
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='TestPass123!',
            role='employee',
            first_name='Other',
            last_name='User',
            department=self.department,
            position='Developer'
        )

        UserTraining.objects.create(
            user=other_user,
            resource=self.training1,
            status='completed',
            progress_percentage=100,
            completed_date=timezone.now().date(),
            certificate_url='https://example.com/other_cert.pdf'
        )

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        # Should still only see own certificates
        self.assertEqual(response.context['with_certificates'], 1)
        trainings = response.context['trainings_with_certificates']
        for training in trainings:
            self.assertEqual(training.user, self.user)

    def test_rating_displayed_for_certificates(self):
        """Test that ratings are available in context."""
        self.user_training1.rating = 5
        self.user_training1.save()

        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('training:my-certificates'))

        trainings = response.context['trainings_with_certificates']
        training_with_rating = trainings.first()
        self.assertEqual(training_with_rating.rating, 5)
