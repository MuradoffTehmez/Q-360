"""
Helper utilities for writing audit events.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from django.http import HttpRequest
from django.utils import timezone

from .models import AuditLog


def record_audit_event(
    *,
    user,
    action: str,
    model_name: str,
    object_id: Optional[str] = None,
    changes: Optional[Dict[str, Any]] = None,
    severity: str = "info",
    status_code: Optional[int] = None,
    request: Optional[HttpRequest] = None,
    context: Optional[Dict[str, Any]] = None,
    check_policy: bool = True,
) -> AuditLog:
    """
    Persist a detailed audit event with optional request information.

    Args:
        user: User performing the action
        action: Action type (login, create, update, etc.)
        model_name: Model name being affected
        object_id: Object ID
        changes: Dict of changes
        severity: Severity level (info, warning, critical)
        status_code: HTTP status code
        request: Django request object
        context: Additional context data
        check_policy: Whether to check audit policy violations

    Returns:
        AuditLog: Created audit log entry
    """
    from apps.security.audit_policy import default_audit_policy

    changes = changes or {}
    context = context or {}
    actor_role = getattr(user, "role", "") if user else ""

    ip_address = None
    if request:
        ip_address = _get_client_ip(request)

    # Check audit policy if enabled
    if check_policy and user:
        policy_check = default_audit_policy.validate_user_action(
            user=user,
            action=action,
            severity=severity,
            ip_address=ip_address
        )

        # Add policy violations to context
        if policy_check['violations'] or policy_check['warnings']:
            context['policy_check'] = policy_check

    log_kwargs = dict(
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        model_name=model_name,
        object_id=object_id or "",
        changes=changes,
        severity=severity,
        actor_role=actor_role,
        status_code=status_code,
        context=context,
    )

    if request:
        log_kwargs.update(
            request_path=request.path[:255] if hasattr(request, "path") else "",
            http_method=getattr(request, "method", ""),
            ip_address=ip_address,
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        )

    return AuditLog.objects.create(**log_kwargs)


def record_login_event(user, request: HttpRequest, success: bool = True) -> AuditLog:
    """
    Record a login event with session tracking.

    Args:
        user: User attempting login
        request: Django request object
        success: Whether login was successful

    Returns:
        AuditLog: Created audit log entry
    """
    from apps.security.session_tracking import UserSessionManager

    action = 'login' if success else 'login_failure'
    severity = 'info' if success else 'warning'

    # Create session snapshot if successful
    session_context = {}
    if success and user:
        session_context = UserSessionManager.create_session_snapshot(user, request)

    return record_audit_event(
        user=user,
        action=action,
        model_name='User',
        object_id=str(user.pk) if user else None,
        severity=severity,
        request=request,
        context={'session': session_context} if session_context else {},
        check_policy=not success  # Only check policy on failed logins
    )


def record_logout_event(user, request: HttpRequest) -> AuditLog:
    """
    Record a logout event.

    Args:
        user: User logging out
        request: Django request object

    Returns:
        AuditLog: Created audit log entry
    """
    session_key = request.session.session_key if hasattr(request, 'session') else None

    return record_audit_event(
        user=user,
        action='logout',
        model_name='User',
        object_id=str(user.pk),
        severity='info',
        request=request,
        context={'session_key': session_key},
        check_policy=False
    )


def get_user_activity_summary(user, days: int = 7) -> Dict[str, Any]:
    """
    Get user activity summary for the last N days.

    Args:
        user: User object
        days: Number of days to analyze

    Returns:
        dict: Activity summary
    """
    from datetime import timedelta

    start_date = timezone.now() - timedelta(days=days)

    logs = AuditLog.objects.filter(user=user, created_at__gte=start_date)

    # Action breakdown
    action_counts = {}
    for log in logs.values('action').annotate(count=AuditLog.objects.count()):
        action_counts[log['action']] = log['count']

    # Severity breakdown
    severity_counts = {}
    for log in logs.values('severity').annotate(count=AuditLog.objects.count()):
        severity_counts[log['severity']] = log['count']

    # Most accessed models
    model_counts = logs.values('model_name').annotate(
        count=AuditLog.objects.count()
    ).order_by('-count')[:5]

    # Get risk assessment
    from apps.security.audit_policy import default_audit_policy
    risk_assessment = default_audit_policy.get_user_risk_score(user)

    return {
        'period_days': days,
        'total_actions': logs.count(),
        'action_breakdown': action_counts,
        'severity_breakdown': severity_counts,
        'most_accessed_models': list(model_counts),
        'risk_assessment': risk_assessment,
        'last_activity': logs.order_by('-created_at').first().created_at if logs.exists() else None
    }


def _get_client_ip(request: HttpRequest) -> Optional[str]:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
