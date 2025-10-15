"""
Comprehensive Tests for Continuous Feedback Module.
Tests anonymity, visibility logic, and public recognition.
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from apps.accounts.models import User
from apps.departments.models import Organization, Department
from apps.continuous_feedback.models import (
    QuickFeedback, FeedbackBank, PublicRecognition,
    RecognitionLike, RecognitionComment
)


class AnonymityTests(TestCase):
    """Test anonymity logic in feedback system."""

    def setUp(self):
        """Set up test users."""
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

        self.sender = User.objects.create_user(
            username='sender',
            email='sender@test.com',
            password='test123',
            first_name='John',
            last_name='Sender',
            department=self.department
        )

        self.recipient = User.objects.create_user(
            username='recipient',
            email='recipient@test.com',
            password='test123',
            first_name='Jane',
            last_name='Recipient',
            department=self.department
        )

    def test_anonymous_feedback_hides_sender(self):
        """Test that anonymous feedback hides sender identity."""
        feedback = QuickFeedback.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            feedback_type='improvement',
            visibility='private',
            title='Test Feedback',
            message='Good job!',
            is_anonymous=True
        )

        # Check that __str__ returns "Anonim" instead of sender name
        self.assertIn('Anonim', str(feedback))
        self.assertNotIn('John Sender', str(feedback))

    def test_non_anonymous_feedback_shows_sender(self):
        """Test that non-anonymous feedback shows sender identity."""
        feedback = QuickFeedback.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            feedback_type='recognition',
            visibility='public',
            title='Great Work',
            message='Excellent teamwork!',
            is_anonymous=False
        )

        # Check that __str__ includes sender name
        self.assertIn('John Sender', str(feedback))

    def test_anonymous_feedback_stored_with_sender_reference(self):
        """Test that anonymous feedback still maintains sender reference in DB."""
        feedback = QuickFeedback.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            feedback_type='improvement',
            visibility='private',
            title='Improvement Suggestion',
            message='Consider improving communication',
            is_anonymous=True
        )

        # Sender should still be stored in database
        self.assertEqual(feedback.sender, self.sender)
        # But is_anonymous flag should be True
        self.assertTrue(feedback.is_anonymous)


class VisibilityLogicTests(TestCase):
    """Test visibility and access control logic."""

    def setUp(self):
        """Set up test environment."""
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

        self.manager = User.objects.create_user(
            username='manager',
            email='manager@test.com',
            password='test123',
            role='manager',
            department=self.department
        )

        self.employee1 = User.objects.create_user(
            username='employee1',
            email='employee1@test.com',
            password='test123',
            role='employee',
            department=self.department,
            supervisor=self.manager
        )

        self.employee2 = User.objects.create_user(
            username='employee2',
            email='employee2@test.com',
            password='test123',
            role='employee',
            department=self.department,
            supervisor=self.manager
        )

        # Other department
        self.other_dept = Department.objects.create(
            organization=self.organization,
            name='Other Dept',
            code='OTHER'
        )
        self.other_employee = User.objects.create_user(
            username='other',
            email='other@test.com',
            password='test123',
            role='employee',
            department=self.other_dept
        )

    def test_private_feedback_visibility(self):
        """Test that private feedback is only visible to sender and recipient."""
        feedback = QuickFeedback.objects.create(
            sender=self.employee1,
            recipient=self.employee2,
            feedback_type='recognition',
            visibility='private',
            title='Private Recognition',
            message='Great job on the project!',
            is_anonymous=False
        )

        self.assertEqual(feedback.visibility, 'private')

    def test_team_feedback_visibility(self):
        """Test that team feedback is visible to team members."""
        feedback = QuickFeedback.objects.create(
            sender=self.employee1,
            recipient=self.employee2,
            feedback_type='recognition',
            visibility='team',
            title='Team Recognition',
            message='Excellent teamwork!',
            is_anonymous=False
        )

        # Team feedback should be filterable by department
        team_feedbacks = QuickFeedback.objects.filter(
            visibility='team',
            sender__department=self.department
        )
        self.assertIn(feedback, team_feedbacks)

    def test_public_feedback_visibility(self):
        """Test that public feedback is visible to all."""
        feedback = QuickFeedback.objects.create(
            sender=self.employee1,
            recipient=self.employee2,
            feedback_type='recognition',
            visibility='public',
            title='Public Recognition',
            message='Outstanding performance!',
            is_anonymous=False
        )

        # Public feedback should be accessible to everyone
        public_feedbacks = QuickFeedback.objects.filter(visibility='public')
        self.assertIn(feedback, public_feedbacks)

    def test_manager_can_see_team_recognition(self):
        """Test that manager can see team-level recognition."""
        # Create team visibility recognition
        feedback = QuickFeedback.objects.create(
            sender=self.employee1,
            recipient=self.employee2,
            feedback_type='recognition',
            visibility='team',
            title='Team Recognition',
            message='Great collaboration!',
            is_anonymous=False
        )

        # Manager should be able to filter team feedbacks
        team_feedbacks = QuickFeedback.objects.filter(
            visibility='team',
            sender__department=self.manager.department
        )
        self.assertIn(feedback, team_feedbacks)


class FeedbackBankTests(TestCase):
    """Test FeedbackBank statistics and aggregation."""

    def setUp(self):
        """Set up test data."""
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

        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='test123',
            department=self.department
        )

        self.sender1 = User.objects.create_user(
            username='sender1',
            email='sender1@test.com',
            password='test123',
            department=self.department
        )

        self.sender2 = User.objects.create_user(
            username='sender2',
            email='sender2@test.com',
            password='test123',
            department=self.department
        )

        # Create feedback bank
        self.feedback_bank = FeedbackBank.objects.create(user=self.user)

    def test_feedback_bank_creation(self):
        """Test that feedback bank is created for user."""
        self.assertIsNotNone(self.feedback_bank)
        self.assertEqual(self.feedback_bank.user, self.user)
        self.assertEqual(self.feedback_bank.total_feedbacks_received, 0)

    def test_feedback_bank_stats_update(self):
        """Test that feedback bank statistics are updated correctly."""
        # Create multiple feedbacks
        QuickFeedback.objects.create(
            sender=self.sender1,
            recipient=self.user,
            feedback_type='recognition',
            visibility='private',
            title='Recognition 1',
            message='Great work!',
            rating=5
        )

        QuickFeedback.objects.create(
            sender=self.sender2,
            recipient=self.user,
            feedback_type='improvement',
            visibility='private',
            title='Improvement 1',
            message='Consider improving time management',
            rating=4
        )

        QuickFeedback.objects.create(
            sender=self.sender1,
            recipient=self.user,
            feedback_type='recognition',
            visibility='public',
            title='Recognition 2',
            message='Excellent presentation!',
            rating=5
        )

        # Update stats
        self.feedback_bank.update_stats()

        # Verify counts
        self.assertEqual(self.feedback_bank.total_feedbacks_received, 3)
        self.assertEqual(self.feedback_bank.total_recognitions, 2)
        self.assertEqual(self.feedback_bank.total_improvements, 1)

        # Verify average rating: (5 + 4 + 5) / 3 = 4.67
        self.assertAlmostEqual(float(self.feedback_bank.average_rating), 4.67, places=2)

    def test_feedback_bank_last_feedback_date(self):
        """Test that last feedback date is tracked."""
        feedback1 = QuickFeedback.objects.create(
            sender=self.sender1,
            recipient=self.user,
            feedback_type='recognition',
            visibility='private',
            title='Old Feedback',
            message='Good job!'
        )
        feedback1.created_at = timezone.now() - timedelta(days=5)
        feedback1.save()

        feedback2 = QuickFeedback.objects.create(
            sender=self.sender2,
            recipient=self.user,
            feedback_type='recognition',
            visibility='private',
            title='Recent Feedback',
            message='Excellent!'
        )

        self.feedback_bank.update_stats()

        # Last feedback date should be from feedback2
        self.assertIsNotNone(self.feedback_bank.last_feedback_date)
        self.assertEqual(
            self.feedback_bank.last_feedback_date.date(),
            feedback2.created_at.date()
        )


class PublicRecognitionTests(TestCase):
    """Test PublicRecognition functionality."""

    def setUp(self):
        """Set up test environment."""
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

        self.sender = User.objects.create_user(
            username='sender',
            email='sender@test.com',
            password='test123',
            department=self.department
        )

        self.recipient = User.objects.create_user(
            username='recipient',
            email='recipient@test.com',
            password='test123',
            department=self.department
        )

        self.viewer = User.objects.create_user(
            username='viewer',
            email='viewer@test.com',
            password='test123',
            department=self.department
        )

    def test_public_recognition_creation(self):
        """Test creating public recognition from feedback."""
        feedback = QuickFeedback.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            feedback_type='recognition',
            visibility='public',
            title='Outstanding Achievement',
            message='Completed project ahead of schedule!',
            is_anonymous=False
        )

        recognition = PublicRecognition.objects.create(feedback=feedback)

        self.assertEqual(recognition.feedback, feedback)
        self.assertEqual(recognition.likes_count, 0)
        self.assertEqual(recognition.comments_count, 0)

    def test_recognition_likes(self):
        """Test liking a recognition."""
        feedback = QuickFeedback.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            feedback_type='recognition',
            visibility='public',
            title='Great Work',
            message='Excellent job!',
            is_anonymous=False
        )

        recognition = PublicRecognition.objects.create(feedback=feedback)

        # User likes the recognition
        like = RecognitionLike.objects.create(
            recognition=recognition,
            user=self.viewer
        )

        # Update like count
        recognition.likes_count = recognition.likes.count()
        recognition.save()

        self.assertEqual(recognition.likes_count, 1)
        self.assertIn(like, recognition.likes.all())

    def test_duplicate_like_prevented(self):
        """Test that user cannot like the same recognition twice."""
        feedback = QuickFeedback.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            feedback_type='recognition',
            visibility='public',
            title='Great Work',
            message='Well done!',
            is_anonymous=False
        )

        recognition = PublicRecognition.objects.create(feedback=feedback)

        RecognitionLike.objects.create(recognition=recognition, user=self.viewer)

        # Try to create duplicate like
        with self.assertRaises(Exception):  # unique_together constraint
            RecognitionLike.objects.create(recognition=recognition, user=self.viewer)

    def test_recognition_comments(self):
        """Test commenting on recognition."""
        feedback = QuickFeedback.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            feedback_type='recognition',
            visibility='public',
            title='Amazing Work',
            message='Incredible achievement!',
            is_anonymous=False
        )

        recognition = PublicRecognition.objects.create(feedback=feedback)

        comment = RecognitionComment.objects.create(
            recognition=recognition,
            user=self.viewer,
            comment='I totally agree! Great work!'
        )

        # Update comment count
        recognition.comments_count = recognition.comments.count()
        recognition.save()

        self.assertEqual(recognition.comments_count, 1)
        self.assertIn(comment, recognition.comments.all())
