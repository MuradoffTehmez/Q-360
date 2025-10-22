"""Tests for training models."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.training.models import (
    TrainingProgram, UserTraining, Certification
)

User = get_user_model()


class TrainingProgramModelTest(TestCase):
    """Test TrainingProgram model."""

    def test_create_training_program(self):
        """Test creating a training program."""
        program = TrainingProgram.objects.create(
            title='Python Advanced Course',
            description='Advanced Python programming',
            training_type='course',
            duration_hours=40,
            status='active',
            capacity=25
        )

        self.assertEqual(program.title, 'Python Advanced Course')
        self.assertEqual(program.duration_hours, 40)
        self.assertEqual(program.status, 'active')
        self.assertIsNotNone(str(program))


class UserTrainingModelTest(TestCase):
    """Test UserTraining model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='traininguser',
            email='training@test.com',
            password='testpass123'
        )
        self.program = TrainingProgram.objects.create(
            title='Test Training',
            training_type='course',
            duration_hours=20,
            status='active'
        )

    def test_create_user_training(self):
        """Test creating user training assignment."""
        user_training = UserTraining.objects.create(
            user=self.user,
            training=self.program,
            status='in_progress',
            assigned_date=timezone.now(),
            due_date=timezone.now() + timedelta(days=30)
        )

        self.assertEqual(user_training.user, self.user)
        self.assertEqual(user_training.training, self.program)
        self.assertEqual(user_training.status, 'in_progress')

    def test_user_training_completion(self):
        """Test completing a user training."""
        user_training = UserTraining.objects.create(
            user=self.user,
            training=self.program,
            status='pending'
        )

        # Complete the training
        user_training.status = 'completed'
        user_training.completion_date = timezone.now()
        user_training.score = 85.5
        user_training.save()

        self.assertEqual(user_training.status, 'completed')
        self.assertEqual(user_training.score, 85.5)
        self.assertIsNotNone(user_training.completion_date)


class CertificationModelTest(TestCase):
    """Test Certification model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='certuser',
            email='cert@test.com',
            password='testpass123'
        )

    def test_create_certification(self):
        """Test creating a certification."""
        certification = Certification.objects.create(
            user=self.user,
            title='AWS Certified Solutions Architect',
            issuing_organization='Amazon Web Services',
            issue_date=timezone.now().date(),
            expiration_date=timezone.now().date() + timedelta(days=1095),  # 3 years
            credential_id='AWS-123456',
            status='active'
        )

        self.assertEqual(certification.title, 'AWS Certified Solutions Architect')
        self.assertEqual(certification.user, self.user)
        self.assertEqual(certification.status, 'active')
        self.assertIsNotNone(certification.expiration_date)
