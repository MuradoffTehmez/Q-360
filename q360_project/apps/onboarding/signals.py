"""
Signal handlers for onboarding automation.
"""
from __future__ import annotations

from django.apps import apps as django_apps
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import OnboardingProcess
from .services import create_onboarding_process


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_onboarding_process(sender, instance, created, **kwargs):
    """
    Automatically create an onboarding process for newly created employees.
    """
    if not created:
        return

    try:
        role = getattr(instance, "role", None)
    except Exception:
        role = None

    if role not in {"employee", "manager"}:
        return

    if OnboardingProcess.objects.filter(employee=instance, status__in=["draft", "active"]).exists():
        return

    # Delay creation while migrations are running.
    if not django_apps.ready:
        return

    create_onboarding_process(employee=instance)

