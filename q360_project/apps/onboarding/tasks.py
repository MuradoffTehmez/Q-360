"""
Celery tasks for onboarding automation.
"""
from __future__ import annotations

from celery import shared_task
from django.utils import timezone

from .models import OnboardingTask
from .services import _process_automation  # internal helper for reuse


@shared_task(name="onboarding.run_due_automations")
def run_due_automations() -> int:
    """
    Re-run automation hooks for tasks that are still pending on their due date.
    """
    today = timezone.now().date()
    tasks = OnboardingTask.objects.filter(
        status="pending",
        task_type__in=["performance_review", "salary_recommendation", "training_plan"],
        due_date__lte=today,
    ).select_related("template_task", "process__template")

    processed = 0
    for task in tasks:
        _process_automation(task)
        processed += 1

    return processed

