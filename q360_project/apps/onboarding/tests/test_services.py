from datetime import date
from decimal import Decimal

from django.db.models.signals import post_save
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User
from apps.competencies.models import Competency, PositionCompetency, ProficiencyLevel, UserSkill
from apps.departments.models import Department, Organization, Position
from apps.onboarding.models import MarketSalaryBenchmark
from apps.onboarding.services import create_onboarding_process
from apps.onboarding.signals import ensure_onboarding_process
from apps.training.models import TrainingResource
from apps.compensation.models import SalaryInformation


class OnboardingServiceTests(TestCase):
    def setUp(self):
        post_save.disconnect(ensure_onboarding_process, sender=User)
        self.addCleanup(lambda: post_save.connect(ensure_onboarding_process, sender=User))

        self.organization = Organization.objects.create(
            name="Test Organization",
            short_name="TEST",
            code="ORG-001",
        )
        self.department = Department.objects.create(
            organization=self.organization,
            name="Data Analytics",
            code="DA-01",
        )

        self.position = Position.objects.create(
            organization=self.organization,
            department=self.department,
            title="Data Analyst",
            code="DA-ANL",
            level=3,
        )

        self.manager = User.objects.create_user(
            username="manager1",
            password="pass1234",
            role="manager",
            department=self.department,
            position="Team Lead",
            first_name="Manager",
            last_name="One",
        )

        self.employee = User.objects.create_user(
            username="employee1",
            password="pass1234",
            role="employee",
            department=self.department,
            position="Data Analyst",
            first_name="Employee",
            last_name="One",
        )

        self.proficiency = ProficiencyLevel.objects.create(
            name="basic",
            display_name="Əsas",
            score_min=Decimal("0"),
            score_max=Decimal("69.99"),
        )

        self.competency = Competency.objects.create(
            name="SQL Reporting",
            description="SQL ilə hesabat hazırlamaq bacarığı.",
        )

        PositionCompetency.objects.create(
            position=self.position,
            competency=self.competency,
            weight=60,
            required_level=self.proficiency,
        )

        UserSkill.objects.create(
            user=self.employee,
            competency=self.competency,
            level=self.proficiency,
            current_score=Decimal("55.00"),
            is_approved=True,
            approval_status="approved",
        )

        self.training = TrainingResource.objects.create(
            title="SQL Fundamentals",
            description="SQL sorğularına giriş.",
            type="course",
            is_online=True,
            delivery_method="online",
            difficulty_level="beginner",
        )
        self.training.required_competencies.add(self.competency)

        MarketSalaryBenchmark.objects.create(
            title="Data Analyst",
            department=self.department,
            role_level="mid",
            currency="AZN",
            min_salary=Decimal("1200.00"),
            median_salary=Decimal("1500.00"),
            max_salary=Decimal("1800.00"),
            data_source="Test Benchmark 2025",
            effective_date=date.today(),
        )

        SalaryInformation.objects.create(
            user=self.employee,
            base_salary=Decimal("1300.00"),
            currency="AZN",
            payment_frequency="monthly",
            effective_date=timezone.now().date(),
        )

    def test_create_onboarding_process_generates_tasks_and_metadata(self):
        process = create_onboarding_process(employee=self.employee, created_by=self.manager)

        self.assertEqual(process.employee, self.employee)
        self.assertEqual(process.department, self.department)
        self.assertEqual(process.tasks.count(), 4)

        review_task = process.tasks.filter(task_type="performance_review").first()
        self.assertIsNotNone(review_task)
        self.assertIn("campaign_id", review_task.metadata)

        salary_task = process.tasks.filter(task_type="salary_recommendation").first()
        self.assertIsNotNone(salary_task)
        self.assertEqual(salary_task.assigned_to, self.manager)
        self.assertIn("recommended_salary", salary_task.metadata)

        training_task = process.tasks.filter(task_type="training_plan").first()
        self.assertIsNotNone(training_task)
        recommendations = training_task.metadata.get("resource_recommendations", [])
        self.assertTrue(
            any(rec.get("title") == "SQL Fundamentals" for rec in recommendations),
            "Training recommendations should include SQL Fundamentals",
        )
