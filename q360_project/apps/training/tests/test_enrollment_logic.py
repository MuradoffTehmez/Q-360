"""
Comprehensive Tests for Training Enrollment Logic.
Tests user enrollment, completion status, and competency-based recommendations.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from apps.accounts.models import User
from apps.departments.models import Organization, Department
from apps.training.models import TrainingResource, UserTraining
from apps.competencies.models import Competency, ProficiencyLevel, UserSkill
from apps.development_plans.models import DevelopmentGoal


class TrainingEnrollmentTests(TestCase):
    """Test user enrollment in training courses."""

    def setUp(self):
        """Set up test users and training resources."""
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

        self.manager = User.objects.create_user(
            username='manager',
            email='manager@test.com',
            password='test123',
            role='manager',
            department=self.department
        )

        # Create training resource
        self.training = TrainingResource.objects.create(
            title='Python Programming',
            description='Learn Python from scratch',
            type='course',
            is_online=True,
            delivery_method='online',
            difficulty_level='intermediate',
            duration_hours=Decimal('40.00'),
            language='English',
            provider='Tech Academy',
            is_active=True
        )

    def test_self_enrollment(self):
        """Test that user can self-enroll in a training."""
        user_training = UserTraining.objects.create(
            user=self.user,
            resource=self.training,
            assignment_type='self_enrolled',
            status='pending'
        )

        self.assertEqual(user_training.user, self.user)
        self.assertEqual(user_training.resource, self.training)
        self.assertEqual(user_training.assignment_type, 'self_enrolled')
        self.assertEqual(user_training.status, 'pending')

    def test_manager_assigned_enrollment(self):
        """Test that manager can assign training to user."""
        user_training = UserTraining.objects.create(
            user=self.user,
            resource=self.training,
            assigned_by=self.manager,
            assignment_type='manager_assigned',
            status='pending',
            due_date=date.today() + timedelta(days=30)
        )

        self.assertEqual(user_training.assigned_by, self.manager)
        self.assertEqual(user_training.assignment_type, 'manager_assigned')
        self.assertIsNotNone(user_training.due_date)

    def test_duplicate_enrollment_prevented(self):
        """Test that user cannot enroll in same training twice."""
        UserTraining.objects.create(
            user=self.user,
            resource=self.training,
            assignment_type='self_enrolled'
        )

        # Try to create duplicate enrollment (should raise IntegrityError)
        with self.assertRaises(Exception):  # unique_together constraint
            UserTraining.objects.create(
                user=self.user,
                resource=self.training,
                assignment_type='self_enrolled'
            )

    def test_system_recommended_enrollment(self):
        """Test system-recommended training enrollment."""
        user_training = UserTraining.objects.create(
            user=self.user,
            resource=self.training,
            assignment_type='system_recommended',
            status='pending'
        )

        self.assertEqual(user_training.assignment_type, 'system_recommended')

    def test_mandatory_training_enrollment(self):
        """Test mandatory training enrollment."""
        mandatory_training = TrainingResource.objects.create(
            title='Cybersecurity Training',
            description='Mandatory security training',
            type='course',
            is_mandatory=True,
            is_active=True
        )

        user_training = UserTraining.objects.create(
            user=self.user,
            resource=mandatory_training,
            assignment_type='mandatory',
            status='pending'
        )

        self.assertEqual(user_training.assignment_type, 'mandatory')
        self.assertTrue(user_training.resource.is_mandatory)

    def test_enrollment_with_development_goal(self):
        """Test enrollment linked to development goal."""
        goal = DevelopmentGoal.objects.create(
            user=self.user,
            title='Master Python',
            description='Become proficient in Python programming',
            category='Technical Skills',
            target_date=date.today() + timedelta(days=90),
            status='active',
            created_by=self.user
        )

        user_training = UserTraining.objects.create(
            user=self.user,
            resource=self.training,
            assignment_type='self_enrolled',
            related_goal=goal,
            status='pending'
        )

        self.assertEqual(user_training.related_goal, goal)
        self.assertIn(user_training, goal.related_trainings.all())


class TrainingCompletionTests(TestCase):
    """Test training completion status functionality."""

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

        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='test123',
            department=self.department
        )

        self.training = TrainingResource.objects.create(
            title='Django Framework',
            description='Learn Django',
            type='course',
            is_active=True
        )

        self.user_training = UserTraining.objects.create(
            user=self.user,
            resource=self.training,
            assignment_type='self_enrolled',
            status='pending'
        )

    def test_mark_training_in_progress(self):
        """Test marking training as in progress."""
        self.user_training.mark_in_progress()

        self.assertEqual(self.user_training.status, 'in_progress')
        self.assertIsNotNone(self.user_training.start_date)
        self.assertEqual(self.user_training.start_date, date.today())

    def test_mark_training_completed(self):
        """Test marking training as completed."""
        completion_note = 'Successfully completed with certificate'
        self.user_training.mark_completed(completion_note=completion_note)

        self.assertEqual(self.user_training.status, 'completed')
        self.assertEqual(self.user_training.progress_percentage, 100)
        self.assertEqual(self.user_training.completed_date, date.today())
        self.assertEqual(self.user_training.completion_note, completion_note)

    def test_update_progress_percentage(self):
        """Test updating progress percentage."""
        self.user_training.update_progress(50)

        self.assertEqual(self.user_training.progress_percentage, 50)
        self.assertEqual(self.user_training.status, 'in_progress')

    def test_auto_complete_at_100_percent(self):
        """Test that training auto-completes at 100% progress."""
        self.user_training.update_progress(100)

        self.assertEqual(self.user_training.status, 'completed')
        self.assertIsNotNone(self.user_training.completed_date)

    def test_auto_start_on_progress_update(self):
        """Test that training auto-starts when progress is updated from pending."""
        self.assertEqual(self.user_training.status, 'pending')
        self.user_training.update_progress(25)

        self.assertEqual(self.user_training.status, 'in_progress')
        self.assertEqual(self.user_training.progress_percentage, 25)

    def test_invalid_progress_percentage_ignored(self):
        """Test that invalid progress percentages are ignored."""
        initial_progress = self.user_training.progress_percentage

        self.user_training.update_progress(-10)  # Invalid
        self.assertEqual(self.user_training.progress_percentage, initial_progress)

        self.user_training.update_progress(150)  # Invalid
        self.assertEqual(self.user_training.progress_percentage, initial_progress)

    def test_is_overdue_functionality(self):
        """Test that is_overdue() correctly identifies overdue trainings."""
        # Set due date to yesterday
        self.user_training.due_date = date.today() - timedelta(days=1)
        self.user_training.save()

        self.assertTrue(self.user_training.is_overdue())

    def test_not_overdue_when_completed(self):
        """Test that completed training is not considered overdue."""
        self.user_training.due_date = date.today() - timedelta(days=1)
        self.user_training.mark_completed()

        self.assertFalse(self.user_training.is_overdue())

    def test_get_days_until_due(self):
        """Test calculation of days until due date."""
        self.user_training.due_date = date.today() + timedelta(days=7)
        self.user_training.save()

        days_remaining = self.user_training.get_days_until_due()
        self.assertEqual(days_remaining, 7)

    def test_training_with_rating_and_feedback(self):
        """Test training completion with rating and user feedback."""
        self.user_training.mark_completed()
        self.user_training.rating = 5
        self.user_training.user_feedback = 'Excellent course, very informative!'
        self.user_training.certificate_url = 'https://example.com/cert/12345'
        self.user_training.save()

        self.assertEqual(self.user_training.rating, 5)
        self.assertIsNotNone(self.user_training.user_feedback)
        self.assertIsNotNone(self.user_training.certificate_url)


class TrainingRecommendationTests(TestCase):
    """Test competency-based training recommendation logic."""

    def setUp(self):
        """Set up test environment with competencies and trainings."""
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

        # Create competencies
        self.python_competency = Competency.objects.create(
            name='Python Programming',
            description='Python development skills',
            is_active=True
        )

        self.django_competency = Competency.objects.create(
            name='Django Framework',
            description='Django web development',
            is_active=True
        )

        self.leadership_competency = Competency.objects.create(
            name='Leadership',
            description='Team leadership skills',
            is_active=True
        )

        # Create proficiency level
        self.intermediate_level = ProficiencyLevel.objects.create(
            name='intermediate',
            display_name='Intermediate',
            score_min=Decimal('50.00'),
            score_max=Decimal('74.99')
        )

        # Create user skills with low scores (need improvement)
        UserSkill.objects.create(
            user=self.user,
            competency=self.python_competency,
            level=self.intermediate_level,
            current_score=60,  # Low score, needs improvement
            is_approved=True
        )

        # Create training resources
        self.python_training = TrainingResource.objects.create(
            title='Advanced Python Course',
            description='Learn advanced Python',
            type='course',
            is_active=True
        )
        self.python_training.required_competencies.add(self.python_competency)

        self.django_training = TrainingResource.objects.create(
            title='Django Master Class',
            description='Master Django framework',
            type='course',
            is_active=True
        )
        self.django_training.required_competencies.add(self.django_competency)

        self.leadership_training = TrainingResource.objects.create(
            title='Leadership Development',
            description='Develop leadership skills',
            type='workshop',
            is_active=True
        )
        self.leadership_training.required_competencies.add(self.leadership_competency)

    def test_training_has_competency_mapping(self):
        """Test that training resources are properly mapped to competencies."""
        self.assertIn(self.python_competency, self.python_training.required_competencies.all())
        self.assertEqual(self.python_training.get_related_competencies().count(), 1)

    def test_recommend_only_relevant_trainings(self):
        """Test that only trainings matching user's competencies are recommended."""
        # User has Python competency, so Python training should be recommended
        # But not Leadership training (user doesn't have that competency)

        recommended_trainings = TrainingResource.objects.filter(
            required_competencies__in=[self.python_competency],
            is_active=True
        ).distinct()

        self.assertIn(self.python_training, recommended_trainings)
        self.assertNotIn(self.leadership_training, recommended_trainings)

    def test_exclude_already_enrolled_trainings(self):
        """Test that trainings user is already enrolled in are excluded from recommendations."""
        # Enroll user in Python training
        UserTraining.objects.create(
            user=self.user,
            resource=self.python_training,
            status='in_progress'
        )

        # Get recommendations (exclude in_progress trainings)
        recommended_trainings = TrainingResource.objects.filter(
            required_competencies__in=[self.python_competency],
            is_active=True
        ).exclude(
            user_trainings__user=self.user,
            user_trainings__status__in=['pending', 'in_progress']
        ).distinct()

        self.assertNotIn(self.python_training, recommended_trainings)

    def test_allow_completed_training_recommendations(self):
        """Test that completed trainings can be recommended again (retake)."""
        # User completed Python training
        UserTraining.objects.create(
            user=self.user,
            resource=self.python_training,
            status='completed'
        )

        # Get recommendations (allow completed trainings)
        recommended_trainings = TrainingResource.objects.filter(
            required_competencies__in=[self.python_competency],
            is_active=True
        ).exclude(
            user_trainings__user=self.user,
            user_trainings__status__in=['pending', 'in_progress']
        ).distinct()

        # Python training should be allowed for retake
        self.assertIn(self.python_training, recommended_trainings)

    def test_recommend_for_low_score_competencies(self):
        """Test that trainings are recommended for competencies with low scores."""
        # User has low score (60) in Python competency
        user_skill = UserSkill.objects.get(user=self.user, competency=self.python_competency)
        self.assertEqual(user_skill.current_score, 60)
        self.assertLess(user_skill.current_score, 70)  # Below threshold

        # Python training should be recommended
        recommended = TrainingResource.objects.filter(
            required_competencies=self.python_competency,
            is_active=True
        )

        self.assertIn(self.python_training, recommended)

    def test_multi_competency_training_recommendation(self):
        """Test recommendation for training that covers multiple competencies."""
        # Create training that covers both Python and Django
        full_stack_training = TrainingResource.objects.create(
            title='Full Stack Python Developer',
            description='Learn Python and Django together',
            type='course',
            is_active=True
        )
        full_stack_training.required_competencies.add(
            self.python_competency,
            self.django_competency
        )

        # Should be recommended if user needs any of the competencies
        recommended = TrainingResource.objects.filter(
            required_competencies__in=[self.python_competency, self.django_competency],
            is_active=True
        ).distinct()

        self.assertIn(full_stack_training, recommended)
        self.assertEqual(full_stack_training.required_competencies.count(), 2)

    def test_inactive_trainings_not_recommended(self):
        """Test that inactive trainings are not recommended."""
        inactive_training = TrainingResource.objects.create(
            title='Deprecated Python 2 Course',
            description='Old Python version',
            type='course',
            is_active=False
        )
        inactive_training.required_competencies.add(self.python_competency)

        recommended = TrainingResource.objects.filter(
            required_competencies=self.python_competency,
            is_active=True
        ).distinct()

        self.assertNotIn(inactive_training, recommended)

    def test_training_completion_rate_calculation(self):
        """Test that training resource completion rate is calculated correctly."""
        # Create multiple enrollments
        user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='test123',
            department=self.department
        )
        user3 = User.objects.create_user(
            username='user3',
            email='user3@test.com',
            password='test123',
            department=self.department
        )

        UserTraining.objects.create(
            user=self.user,
            resource=self.python_training,
            status='completed'
        )
        UserTraining.objects.create(
            user=user2,
            resource=self.python_training,
            status='completed'
        )
        UserTraining.objects.create(
            user=user3,
            resource=self.python_training,
            status='in_progress'
        )

        completion_rate = self.python_training.get_completion_rate()
        # 2 completed out of 3 total = 66.67%
        self.assertAlmostEqual(completion_rate, 66.67, places=1)

    def test_training_assigned_users_count(self):
        """Test counting assigned users for a training resource."""
        user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='test123',
            department=self.department
        )

        UserTraining.objects.create(
            user=self.user,
            resource=self.python_training,
            status='pending'
        )
        UserTraining.objects.create(
            user=user2,
            resource=self.python_training,
            status='completed'
        )

        assigned_count = self.python_training.get_assigned_users_count()
        self.assertEqual(assigned_count, 2)
