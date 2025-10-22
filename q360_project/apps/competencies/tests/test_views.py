"""
Tests for competencies views.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.competencies.models import Competency, SkillLevel, UserSkill

User = get_user_model()


class CompetencyListViewTest(TestCase):
    """Test competency list view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.competency = Competency.objects.create(
            name='Test Competency',
            category='Technical'
        )

    def test_competency_list_requires_login(self):
        """Test that competency list requires authentication."""
        url = reverse('competencies:competency_list')
        response = self.client.get(url)

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_competency_list_authenticated(self):
        """Test competency list with authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('competencies:competency_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Competency')


class CompetencyDetailViewTest(TestCase):
    """Test competency detail view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='detailuser',
            email='detail@test.com',
            password='testpass123'
        )
        self.competency = Competency.objects.create(
            name='Detail Competency',
            description='Test description',
            category='Technical'
        )

    def test_competency_detail_requires_login(self):
        """Test that competency detail requires authentication."""
        url = reverse('competencies:competency_detail', args=[self.competency.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_competency_detail_authenticated(self):
        """Test competency detail with authenticated user."""
        self.client.login(username='detailuser', password='testpass123')
        url = reverse('competencies:competency_detail', args=[self.competency.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail Competency')
        self.assertContains(response, 'Test description')


class MySkillsViewTest(TestCase):
    """Test my skills view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='skilluser',
            email='skill@test.com',
            password='testpass123'
        )
        self.competency = Competency.objects.create(
            name='My Skill',
            category='Technical'
        )
        self.level = SkillLevel.objects.create(
            name='advanced',
            display_name='Advanced',
            proficiency_score=4
        )
        self.user_skill = UserSkill.objects.create(
            user=self.user,
            competency=self.competency,
            level=self.level,
            is_approved=True
        )

    def test_my_skills_requires_login(self):
        """Test that my skills requires authentication."""
        url = reverse('competencies:my_skills')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_my_skills_authenticated(self):
        """Test my skills view with authenticated user."""
        self.client.login(username='skilluser', password='testpass123')
        url = reverse('competencies:my_skills')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Should show user's skills
        self.assertContains(response, 'My Skill')


class SkillGapAnalysisViewTest(TestCase):
    """Test skill gap analysis view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='gapuser',
            email='gap@test.com',
            password='testpass123'
        )

    def test_skill_gap_requires_login(self):
        """Test that skill gap analysis requires authentication."""
        url = reverse('competencies:skill_gap_analysis')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_skill_gap_authenticated(self):
        """Test skill gap analysis with authenticated user."""
        self.client.login(username='gapuser', password='testpass123')
        url = reverse('competencies:skill_gap_analysis')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
