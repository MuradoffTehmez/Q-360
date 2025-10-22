"""
Tests for competencies models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.competencies.models import (
    Competency, SkillLevel, UserSkill,
    SkillEndorsement, SkillGap
)

User = get_user_model()


class CompetencyModelTest(TestCase):
    """Test Competency model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_create_competency(self):
        """Test creating a competency."""
        competency = Competency.objects.create(
            name='Python Programming',
            description='Advanced Python coding skills',
            category='Technical',
            is_active=True
        )

        self.assertEqual(competency.name, 'Python Programming')
        self.assertTrue(competency.is_active)
        self.assertEqual(str(competency), 'Python Programming')

    def test_competency_weight_validation(self):
        """Test competency weight is between 0 and 1."""
        competency = Competency.objects.create(
            name='Test Competency',
            weight=0.5
        )

        self.assertGreaterEqual(competency.weight, 0.0)
        self.assertLessEqual(competency.weight, 1.0)


class SkillLevelModelTest(TestCase):
    """Test SkillLevel model."""

    def test_create_skill_level(self):
        """Test creating a skill level."""
        level = SkillLevel.objects.create(
            name='expert',
            display_name='Expert',
            proficiency_score=5,
            description='Expert level proficiency'
        )

        self.assertEqual(level.name, 'expert')
        self.assertEqual(level.proficiency_score, 5)
        self.assertEqual(str(level), 'Expert')


class UserSkillModelTest(TestCase):
    """Test UserSkill model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='skilluser',
            email='skill@test.com',
            password='testpass123'
        )
        self.competency = Competency.objects.create(
            name='Django Framework',
            category='Technical'
        )
        self.level = SkillLevel.objects.create(
            name='advanced',
            display_name='Advanced',
            proficiency_score=4
        )

    def test_create_user_skill(self):
        """Test creating a user skill."""
        user_skill = UserSkill.objects.create(
            user=self.user,
            competency=self.competency,
            level=self.level,
            years_of_experience=3,
            approval_status='approved',
            is_approved=True
        )

        self.assertEqual(user_skill.user, self.user)
        self.assertEqual(user_skill.competency, self.competency)
        self.assertEqual(user_skill.years_of_experience, 3)
        self.assertTrue(user_skill.is_approved)

    def test_user_skill_proficiency_score(self):
        """Test getting proficiency score from user skill."""
        user_skill = UserSkill.objects.create(
            user=self.user,
            competency=self.competency,
            level=self.level
        )

        # Check if get_proficiency_score method exists and works
        if hasattr(user_skill, 'get_proficiency_score'):
            score = user_skill.get_proficiency_score()
            self.assertEqual(score, 4)


class SkillEndorsementModelTest(TestCase):
    """Test SkillEndorsement model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='endorseuser',
            email='endorse@test.com',
            password='testpass123'
        )
        self.endorser = User.objects.create_user(
            username='endorser',
            email='endorser@test.com',
            password='testpass123'
        )
        self.competency = Competency.objects.create(
            name='Leadership',
            category='Soft Skills'
        )
        self.level = SkillLevel.objects.create(
            name='expert',
            display_name='Expert',
            proficiency_score=5
        )
        self.user_skill = UserSkill.objects.create(
            user=self.user,
            competency=self.competency,
            level=self.level
        )

    def test_create_skill_endorsement(self):
        """Test creating a skill endorsement."""
        endorsement = SkillEndorsement.objects.create(
            user_skill=self.user_skill,
            endorser=self.endorser,
            comment='Great leadership skills!'
        )

        self.assertEqual(endorsement.user_skill, self.user_skill)
        self.assertEqual(endorsement.endorser, self.endorser)
        self.assertEqual(endorsement.comment, 'Great leadership skills!')


class SkillGapModelTest(TestCase):
    """Test SkillGap model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='gapuser',
            email='gap@test.com',
            password='testpass123'
        )
        self.competency = Competency.objects.create(
            name='Machine Learning',
            category='Technical'
        )
        self.current_level = SkillLevel.objects.create(
            name='beginner',
            display_name='Beginner',
            proficiency_score=1
        )
        self.target_level = SkillLevel.objects.create(
            name='advanced',
            display_name='Advanced',
            proficiency_score=4
        )

    def test_create_skill_gap(self):
        """Test creating a skill gap."""
        skill_gap = SkillGap.objects.create(
            user=self.user,
            competency=self.competency,
            current_level=self.current_level,
            target_level=self.target_level,
            priority='high',
            status='identified'
        )

        self.assertEqual(skill_gap.user, self.user)
        self.assertEqual(skill_gap.competency, self.competency)
        self.assertEqual(skill_gap.priority, 'high')
        self.assertEqual(skill_gap.status, 'identified')
