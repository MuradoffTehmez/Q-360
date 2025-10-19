"""
Helper utilities for writing audit events.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from django.http import HttpRequest

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
) -> AuditLog:
    """
    Persist a detailed audit event with optional request information.
    """
    changes = changes or {}
    context = context or {}
    actor_role = getattr(user, "role", "") if user else ""

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
            ip_address=_get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        )

    return AuditLog.objects.create(**log_kwargs)


def _get_client_ip(request: HttpRequest) -> Optional[str]:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
