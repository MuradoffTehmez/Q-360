from django.test import RequestFactory, TestCase

from apps.accounts.models import User
from apps.audit.models import AuditLog
from apps.audit.services import record_audit_event


class AuditServiceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="auditor",
            password="pass1234",
            role="manager",
        )

    def test_record_audit_event_without_request(self):
        log = record_audit_event(
            user=self.user,
            action="update",
            model_name="apps.accounts.User",
            object_id=str(self.user.pk),
            changes={"field": ["old", "new"]},
            severity="warning",
            context={"source": "unit-test"},
        )

        self.assertEqual(log.actor_role, "manager")
        self.assertEqual(log.severity, "warning")
        self.assertEqual(log.changes["field"], ["old", "new"])
        self.assertEqual(log.context["source"], "unit-test")

    def test_record_audit_event_with_request(self):
        request = self.factory.get("/test-path/", HTTP_USER_AGENT="pytest")
        request.META["REMOTE_ADDR"] = "127.0.0.1"

        log = record_audit_event(
            user=self.user,
            action="view",
            model_name="reports.Report",
            request=request,
            status_code=200,
            object_id="123",
        )

        self.assertEqual(log.request_path, "/test-path/")
        self.assertEqual(log.http_method, "GET")
        self.assertEqual(log.status_code, 200)
        self.assertEqual(log.ip_address, "127.0.0.1")
        self.assertEqual(log.user_agent, "pytest")
