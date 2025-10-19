from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User
from apps.reports.models import ReportBlueprint, ReportSchedule, ReportScheduleLog, ReportGenerationLog
from apps.reports.services import build_dataset_for_blueprint, export_blueprint, process_due_schedules
from apps.training.models import TrainingResource


class ReportBlueprintServiceTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="pass1234",
            role="manager",
            email="owner@example.com",
        )
        self.training = TrainingResource.objects.create(
            title="Data Literacy",
            description="Foundational data skills.",
            type="course",
            delivery_method="online",
            difficulty_level="beginner",
        )
        self.blueprint = ReportBlueprint.objects.create(
            owner=self.owner,
            title="Training Coverage",
            slug="training-coverage",
            data_source="training",
            columns=["Təlim", "Növ", "Çatdırılma", "Çətinlik"],
        )

    def test_build_dataset_for_training_blueprint(self):
        dataset = build_dataset_for_blueprint(self.blueprint)
        self.assertEqual(dataset.columns, ["Təlim", "Növ", "Çatdırılma", "Çətinlik"])
        self.assertGreaterEqual(len(dataset.rows), 1)
        first_row = dataset.rows[0]
        self.assertIn(self.training.title, first_row)
        self.assertIn("total_resources", dataset.metadata)

    def test_export_blueprint_creates_generation_log(self):
        log = export_blueprint(self.blueprint, "excel", requested_by=self.owner)
        self.assertEqual(log.status, "completed")
        self.assertTrue(log.file)
        self.assertEqual(ReportGenerationLog.objects.count(), 1)

    def test_process_due_schedules_generates_exports(self):
        schedule = ReportSchedule.objects.create(
            blueprint=self.blueprint,
            created_by=self.owner,
            frequency="daily",
            interval=1,
            export_format="pdf",
        )
        # Force schedule to be due
        schedule.next_run = timezone.now() - timedelta(minutes=5)
        schedule.save(update_fields=["next_run"])

        processed = process_due_schedules()
        self.assertEqual(processed, 1)
        schedule.refresh_from_db()
        self.assertIsNotNone(schedule.last_run)
        self.assertEqual(schedule.last_status, "completed")
        self.assertTrue(ReportScheduleLog.objects.filter(schedule=schedule, status="completed").exists())
