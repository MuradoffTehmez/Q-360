"""Real-time statistics API endpoints."""
from __future__ import annotations

from datetime import timedelta

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import User
from apps.audit.models import AuditLog
from apps.dashboard.models import SystemKPI
from apps.notifications.models import Notification
from apps.onboarding.models import OnboardingProcess, OnboardingTask


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def realtime_stats(request):
    """Return lightweight real-time dashboard metrics."""
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)
    one_day_ago = now - timedelta(days=1)

    active_users = User.objects.filter(is_active=True).count()
    new_users = User.objects.filter(date_joined__gte=one_day_ago).count()

    onboarding_active = OnboardingProcess.objects.filter(status="active").count()
    onboarding_pending_tasks = OnboardingTask.objects.filter(status="pending").count()

    notifications_unread = Notification.objects.filter(is_read=False).count()

    latest_kpi = (
        SystemKPI.objects.order_by("-created_at")
        .values("name", "value", "unit", "created_at")
        .first()
    )

    audit_alerts = AuditLog.objects.filter(
        action__in=["permission_denied", "login_failure"],
        created_at__gte=one_hour_ago,
    ).count()

    payload = {
        "users": {
            "active": active_users,
            "new_last_24h": new_users,
        },
        "onboarding": {
            "active_processes": onboarding_active,
            "pending_tasks": onboarding_pending_tasks,
        },
        "notifications": {
            "unread": notifications_unread,
        },
        "security": {
            "alerts_last_hour": audit_alerts,
        },
        "latest_kpi": latest_kpi or None,
        "generated_at": now.isoformat(),
    }

    return Response(payload)
