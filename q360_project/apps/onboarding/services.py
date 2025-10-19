"""
Service layer for the onboarding automation module.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, Iterable, List, Optional

from django.apps import apps as django_apps
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import (
    MarketSalaryBenchmark,
    OnboardingProcess,
    OnboardingTask,
    OnboardingTaskTemplate,
    OnboardingTemplate,
)


@dataclass
class TaskExecutionResult:
    """Lightweight response for task automation helpers."""

    success: bool
    metadata: Dict
    error: Optional[str] = None


def get_default_template() -> Optional[OnboardingTemplate]:
    """Return the active template flagged as default."""
    return (
        OnboardingTemplate.objects.filter(is_default=True, is_active=True)
        .order_by("id")
        .first()
    )


@transaction.atomic
def create_onboarding_process(
    *,
    employee,
    created_by=None,
    template: Optional[OnboardingTemplate] = None,
    start_date: Optional[date] = None,
) -> OnboardingProcess:
    """
    Bootstrap onboarding workflow for a new employee.
    """

    template = template or get_default_template()

    process = OnboardingProcess.objects.create(
        employee=employee,
        template=template,
        department=getattr(employee, "department", None),
        start_date=start_date or timezone.now().date(),
        status="active",
        created_by=created_by,
    )

    if template:
        _generate_tasks_from_template(process, template)
    else:
        _generate_fallback_tasks(process)

    return process


def _generate_tasks_from_template(process: OnboardingProcess, template: OnboardingTemplate) -> None:
    """
    Instantiate runtime tasks based on the template definition.
    """
    tasks = template.task_templates.select_related().order_by("order", "id")
    for task_template in tasks:
        due_date = process.start_date + timedelta(days=task_template.due_in_days)
        assignee = _resolve_assignee(task_template.assignee_role, process)
        _create_task_from_template(process, task_template, due_date, assignee)


def _generate_fallback_tasks(process: OnboardingProcess) -> None:
    """
    Ensure we still track onboarding even if no template exists.
    """
    fallback_tasks = [
        {
            "title": "Profil məlumatlarını tamamlayın",
            "task_type": "general",
            "description": "HR portalında şəxsi məlumatları, sənədləri və bank detalları daxil edin.",
            "due_days": 3,
        },
        {
            "title": "İlkin performans qiymətləndirməsini planlaşdırın",
            "task_type": "performance_review",
            "description": "Başlanğıcdan 3 ay sonra 360 qiymətləndirmə kampaniyası yaradın.",
            "due_days": 30,
        },
        {
            "title": "Maaş bazar uyğunluğunu yoxlayın",
            "task_type": "salary_recommendation",
            "description": "Market benchmark məlumatlarına əsasən maaş tövsiyəsi hazırlayın.",
            "due_days": 45,
        },
        {
            "title": "İlkin təlim planını hazırlayın",
            "task_type": "training_plan",
            "description": "Skill gap analizi əsasında 3 təlim resursu təklif edin.",
            "due_days": 14,
        },
    ]

    for order, payload in enumerate(fallback_tasks, start=1):
        due_date = process.start_date + timedelta(days=payload["due_days"])
        task = OnboardingTask.objects.create(
            process=process,
            title=payload["title"],
            description=payload["description"],
            task_type=payload["task_type"],
            assigned_to=process.employee,
            due_date=due_date,
        )
        _process_automation(task)


def _resolve_assignee(role: Optional[str], process: OnboardingProcess):
    """
    Try to find an assignee for the given role within the employee's department.
    Falls back to the employee.
    """
    UserModel = django_apps.get_model(settings.AUTH_USER_MODEL)
    if not role:
        return process.employee

    qs = UserModel.objects.filter(role=role, is_active=True)
    if process.department_id:
        qs = qs.filter(department_id=process.department_id)
    assignee = qs.order_by("id").first()
    return assignee or process.employee


def _create_task_from_template(
    process: OnboardingProcess,
    task_template: OnboardingTaskTemplate,
    due_date: date,
    assignee,
) -> OnboardingTask:
    task = OnboardingTask.objects.create(
        process=process,
        template_task=task_template,
        title=task_template.title,
        description=task_template.description,
        task_type=task_template.task_type,
        assigned_to=assignee,
        due_date=due_date,
    )
    _process_automation(task, template=task_template)
    return task


def _process_automation(task: OnboardingTask, template: Optional[OnboardingTaskTemplate] = None) -> None:
    """
    Execute automation hooks based on the task type.
    """
    template = template or task.template_task

    handlers = {
        "performance_review": _handle_performance_review_task,
        "salary_recommendation": _handle_salary_recommendation_task,
        "training_plan": _handle_training_plan_task,
    }

    handler = handlers.get(task.task_type)
    if not handler:
        return

    result = handler(task)
    metadata = result.metadata if isinstance(result, TaskExecutionResult) else {}
    if result and not result.success:
        task.status = "blocked"
        metadata = {**metadata, "error": result.error or "Automation failed"}
        task.metadata = {**task.metadata, **metadata}
        task.save(update_fields=["status", "metadata", "updated_at"])
        return

    task.metadata = {**task.metadata, **metadata}
    task.save(update_fields=["metadata", "updated_at"])

    auto_complete = bool(template and template.auto_complete)
    if auto_complete and result and result.success:
        task.mark_completed(metadata=metadata)


def _handle_performance_review_task(task: OnboardingTask) -> TaskExecutionResult:
    """
    Create an evaluation campaign targeting the onboarded employee.
    """
    process = task.process
    template = process.template
    offset_days = template.review_cycle_offset_days if template else 90
    campaign_start = task.due_date or (process.start_date + timedelta(days=offset_days))
    campaign_end = campaign_start + timedelta(days=30)

    EvaluationCampaign = django_apps.get_model("evaluations", "EvaluationCampaign")

    title = f"İlkin Performans Qiymətləndirməsi - {process.employee.get_full_name()}"
    campaign = EvaluationCampaign.objects.filter(
        title=title,
        start_date=campaign_start,
        end_date=campaign_end,
    ).first()

    if not campaign:
        creator = process.created_by or process.employee
        campaign = EvaluationCampaign.objects.create(
            title=title,
            description="Yeni işçi üçün onboarding dövrünün sonunda avtomatik qiymətləndirmə kampaniyası.",
            start_date=campaign_start,
            end_date=campaign_end,
            status="draft",
            created_by=creator,
        )
        campaign.target_users.add(process.employee)

    return TaskExecutionResult(
        success=True,
        metadata={
            "campaign_id": campaign.id,
            "campaign_start": campaign_start.isoformat(),
            "campaign_end": campaign_end.isoformat(),
        },
    )


def _handle_salary_recommendation_task(task: OnboardingTask) -> TaskExecutionResult:
    """
    Suggest a salary adjustment referencing market benchmarks.
    """
    process = task.process
    employee = process.employee

    SalaryInformation = django_apps.get_model("compensation", "SalaryInformation")

    current_salary = (
        SalaryInformation.objects.filter(user=employee, is_active=True)
        .order_by("-effective_date")
        .first()
    )

    benchmark = _find_benchmark(employee, process)
    if not benchmark:
        metadata = {
            "message": "Uyğun market benchmark tapılmadı.",
        }
        return TaskExecutionResult(success=False, metadata=metadata, error="Benchmark not found")

    recommended = benchmark.recommended_salary(weight=Decimal("0.35"))
    increase_amount = None
    increase_percentage = None

    if current_salary:
        increase_amount = recommended - current_salary.base_salary
        if current_salary.base_salary > 0:
            increase_percentage = (increase_amount / current_salary.base_salary) * Decimal("100")

    metadata = {
        "benchmark_id": benchmark.id,
        "benchmark_title": benchmark.title,
        "currency": benchmark.currency,
        "current_salary": str(current_salary.base_salary) if current_salary else None,
        "recommended_salary": str(recommended.quantize(Decimal("0.01"))),
        "increase_amount": str(increase_amount.quantize(Decimal("0.01"))) if increase_amount is not None else None,
        "increase_percentage": str(increase_percentage.quantize(Decimal("0.01"))) if increase_percentage is not None else None,
        "source": benchmark.data_source,
        "effective_date": benchmark.effective_date.isoformat(),
    }

    return TaskExecutionResult(success=True, metadata=metadata)


def _find_benchmark(employee, process: OnboardingProcess) -> Optional[MarketSalaryBenchmark]:
    """
    Locate the best matching salary benchmark.
    """
    if not employee.position:
        qs = MarketSalaryBenchmark.objects.filter(department=process.department).order_by("-effective_date")
        return qs.first()

    qs = MarketSalaryBenchmark.objects.filter(title__iexact=employee.position).order_by("-effective_date")
    benchmark = qs.first()
    if benchmark:
        return benchmark

    qs = MarketSalaryBenchmark.objects.filter(
        department=process.department,
        role_level__in=["mid", "senior"],
    ).order_by("-effective_date")
    return qs.first()


def _handle_training_plan_task(task: OnboardingTask) -> TaskExecutionResult:
    """
    Recommend training resources that address competency gaps.
    """
    process = task.process
    employee = process.employee

    UserSkill = django_apps.get_model("competencies", "UserSkill")
    PositionCompetency = django_apps.get_model("competencies", "PositionCompetency")
    TrainingResource = django_apps.get_model("training", "TrainingResource")
    Position = django_apps.get_model("departments", "Position")

    position_titles = [employee.position] if employee.position else []
    positions = []

    if position_titles:
        positions = list(Position.objects.filter(title__in=position_titles))

    competency_ids: Iterable[int] = []
    if positions:
        competency_ids = (
            PositionCompetency.objects.filter(position__in=positions)
            .values_list("competency_id", flat=True)
            .distinct()
        )

    low_skills = UserSkill.objects.filter(
        user=employee,
        competency_id__in=list(competency_ids),
    ).order_by("current_score")

    missing_competency_ids: List[int] = []
    for skill in low_skills:
        if skill.current_score is None or skill.current_score < Decimal("70"):
            missing_competency_ids.append(skill.competency_id)

    if not missing_competency_ids and competency_ids:
        missing_competency_ids = list(competency_ids)[:3]

    resources = (
        TrainingResource.objects.filter(required_competencies__id__in=missing_competency_ids)
        .distinct()
        .order_by("title")[:5]
    )

    if not resources.exists():
        resources = TrainingResource.objects.filter(is_online=True).order_by("title")[:5]

    recommendations = [
        {
            "id": resource.id,
            "title": resource.title,
            "type": resource.type,
            "delivery_method": resource.delivery_method,
            "link": resource.link,
        }
        for resource in resources
    ]

    metadata = {
        "competency_ids": missing_competency_ids,
        "resource_recommendations": recommendations,
    }

    return TaskExecutionResult(success=True, metadata=metadata)
