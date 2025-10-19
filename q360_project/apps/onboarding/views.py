"""
Template-driven views for onboarding automation frontend.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView

from apps.accounts.models import User
from apps.departments.models import Department

from .models import OnboardingProcess, OnboardingTask, OnboardingTemplate


class OnboardingDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "onboarding/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        processes_qs = (
            OnboardingProcess.objects.select_related("employee", "template", "department", "created_by")
            .prefetch_related("tasks__assigned_to")
            .order_by("-created_at")
        )

        process_list = list(processes_qs[:6])
        completion_totals: list[Decimal] = []
        for process in process_list:
            tasks = list(process.tasks.all())
            process.total_tasks = len(tasks)
            process.completed_tasks = sum(1 for task in tasks if task.status == "completed")
            process.next_due_date = min(
                (task.due_date for task in tasks if task.due_date), default=None
            )
            completion = process.completion_rate()
            completion_totals.append(completion)

        avg_completion = (
            sum(completion_totals) / len(completion_totals)
            if completion_totals
            else Decimal("0")
        )

        pending_tasks_qs = OnboardingTask.objects.filter(status__in=["pending", "in_progress"])
        upcoming_tasks = (
            pending_tasks_qs.select_related("process__employee", "assigned_to")
            .order_by("due_date")[:6]
        )

        review_window = timezone.now().date() + timedelta(days=30)
        review_tasks = (
            OnboardingTask.objects.select_related("process__employee")
            .filter(task_type="performance_review", due_date__lte=review_window)
            .order_by("due_date")
        )
        salary_tasks = (
            OnboardingTask.objects.select_related("process__employee")
            .filter(task_type="salary_recommendation")
            .order_by("due_date")[:5]
        )
        training_tasks = (
            OnboardingTask.objects.select_related("process__employee")
            .filter(task_type="training_plan")
            .order_by("due_date")[:5]
        )

        context.update(
            {
                "processes": process_list,
                "kpis": {
                    "active_processes": processes_qs.filter(status="active").count(),
                    "avg_completion_rate": f"{avg_completion.quantize(Decimal('1'))}%",
                    "pending_tasks": pending_tasks_qs.count(),
                    "upcoming_reviews": review_tasks.count(),
                },
                "upcoming_tasks": list(upcoming_tasks),
                "templates": OnboardingTemplate.objects.filter(is_active=True).prefetch_related(
                    "task_templates"
                )[:6],
                "upcoming_reviews": [
                    {
                        "employee_name": task.process.employee.get_full_name()
                        or task.process.employee.username,
                        "start_date": task.due_date or task.process.start_date,
                    }
                    for task in review_tasks
                ],
                "salary_recommendations": [
                    {
                        "employee_name": task.process.employee.get_full_name()
                        or task.process.employee.username,
                        "recommended_salary": task.metadata.get("recommended_salary"),
                        "role": task.process.employee.position,
                    }
                    for task in salary_tasks
                    if task.metadata.get("recommended_salary")
                ],
                "training_recommendations": [
                    {
                        "employee_name": task.process.employee.get_full_name()
                        or task.process.employee.username,
                        "title": resource.get("title"),
                        "due_date": task.due_date,
                    }
                    for task in training_tasks
                    for resource in task.metadata.get("resource_recommendations", [])
                ],
                "last_sync": timezone.now(),
            }
        )
        return context


class OnboardingProcessListView(LoginRequiredMixin, TemplateView):
    template_name = "onboarding/process_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        processes = (
            OnboardingProcess.objects.select_related("employee", "template", "department")
            .prefetch_related("tasks")
            .order_by("-created_at")
        )

        status = self.request.GET.get("status")
        department = self.request.GET.get("department")
        template_id = self.request.GET.get("template")

        if status:
            processes = processes.filter(status=status)
        if department:
            processes = processes.filter(department_id=department)
        if template_id:
            processes = processes.filter(template_id=template_id)

        process_list = list(processes)
        for process in process_list:
            tasks = list(process.tasks.all())
            process.total_tasks = len(tasks)
            process.completed_tasks = sum(1 for task in tasks if task.status == "completed")

        paginator = Paginator(process_list, 15)
        page_number = self.request.GET.get("page") or 1
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context.update(
            {
                "page_obj": page_obj,
                "status_choices": OnboardingProcess.STATUS_CHOICES,
                "departments": Department.objects.filter(is_active=True).order_by("name"),
                "templates": OnboardingTemplate.objects.filter(is_active=True).order_by("name"),
            }
        )
        return context


class OnboardingProcessDetailView(LoginRequiredMixin, TemplateView):
    template_name = "onboarding/process_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.process = get_object_or_404(
            OnboardingProcess.objects.select_related(
                "employee", "department", "template", "created_by"
            ).prefetch_related("tasks__assigned_to", "tasks__template_task"),
            pk=kwargs["pk"],
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = list(self.process.tasks.all())
        task_tabs = [
            ("pending", _("Gözləyən")),
            ("in_progress", _("İcrada")),
            ("completed", _("Tamamlanmış")),
            ("blocked", _("Bloklanmış")),
        ]
        tasks_by_status = defaultdict(list)
        task_counts = {}

        for task in tasks:
            tasks_by_status[task.status].append(task)
        for status, _ in task_tabs:
            task_counts[status] = len(tasks_by_status.get(status, []))

        automation_events = []
        for task in tasks:
            if task.task_type in {"performance_review", "salary_recommendation", "training_plan"}:
                badge = {
                    "performance_review": "info",
                    "salary_recommendation": "warning",
                    "training_plan": "success",
                }.get(task.task_type, "secondary")
                automation_events.append(
                    {
                        "title": task.title,
                        "description": task.metadata.get("message")
                        or task.description
                        or "",
                        "trigger_date": task.due_date or self.process.start_date,
                        "badge": badge,
                        "event_type": task.get_task_type_display(),
                    }
                )

        context.update(
            {
                "process": self.process,
                "tasks_by_status": tasks_by_status,
                "task_tabs": task_tabs,
                "task_counts": task_counts,
                "automation_events": automation_events,
                "recent_notes": [],
            }
        )
        return context


class OnboardingTemplateLibraryView(LoginRequiredMixin, TemplateView):
    template_name = "onboarding/template_library.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        templates = OnboardingTemplate.objects.prefetch_related("task_templates").order_by("name")
        if self.request.GET.get("type"):
            templates = templates.filter(task_templates__task_type=self.request.GET["type"]).distinct()
        if self.request.GET.get("default"):
            templates = templates.filter(is_default=True)

        context.update(
            {
                "templates": templates,
                "type_choices": OnboardingTask.TASK_TYPE_CHOICES,
            }
        )
        return context


class OnboardingTemplateDetailView(LoginRequiredMixin, TemplateView):
    template_name = "onboarding/template_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template = get_object_or_404(
            OnboardingTemplate.objects.prefetch_related("task_templates"),
            slug=kwargs["slug"],
        )
        context["template"] = template
        return context


class OnboardingTemplateFormView(LoginRequiredMixin, TemplateView):
    template_name = "onboarding/template_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template = None
        if kwargs.get("slug"):
            template = get_object_or_404(OnboardingTemplate, slug=kwargs["slug"])

        context["mode"] = "edit" if template else "create"
        context["form_data"] = {
            "name": getattr(template, "name", ""),
            "slug": getattr(template, "slug", ""),
            "description": getattr(template, "description", ""),
            "review_cycle_offset_days": getattr(template, "review_cycle_offset_days", 90),
            "salary_review_offset_days": getattr(template, "salary_review_offset_days", 60),
            "training_plan_offset_days": getattr(template, "training_plan_offset_days", 14),
            "is_default": getattr(template, "is_default", False),
        }
        return context


class TemplateDuplicateView(LoginRequiredMixin, View):
    def get(self, request, slug):
        template = get_object_or_404(OnboardingTemplate.objects.prefetch_related("task_templates"), slug=slug)
        clone = OnboardingTemplate.objects.create(
            name=f"{template.name} ({_('Kopya')})",
            slug=f"{template.slug}-copy-{int(timezone.now().timestamp())}",
            description=template.description,
            is_default=False,
            is_active=template.is_active,
            review_cycle_offset_days=template.review_cycle_offset_days,
            salary_review_offset_days=template.salary_review_offset_days,
            training_plan_offset_days=template.training_plan_offset_days,
        )
        for task in template.task_templates.all():
            clone.task_templates.create(
                title=task.title,
                description=task.description,
                task_type=task.task_type,
                due_in_days=task.due_in_days,
                assignee_role=task.assignee_role,
                auto_complete=task.auto_complete,
                metadata_schema=task.metadata_schema,
                order=task.order,
            )
        messages.success(request, _("Şablon uğurla kopyalandı."))
        return redirect("onboarding:template-library")


class TemplateDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        template = get_object_or_404(OnboardingTemplate, slug=slug)
        template.delete()
        messages.success(request, _("Şablon silindi."))
        return redirect("onboarding:template-library")


class OnboardingProcessCreateView(LoginRequiredMixin, TemplateView):
    template_name = "onboarding/process_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "employees": User.objects.filter(is_active=True).order_by("first_name"),
                "templates": OnboardingTemplate.objects.filter(is_active=True).order_by("name"),
                "selected": {
                    "employee": self.request.GET.get("employee", ""),
                    "template": self.request.GET.get("template", ""),
                    "start_date": timezone.now().date().isoformat(),
                },
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        employee_id = request.POST.get("employee")
        template_id = request.POST.get("template")
        start_date = request.POST.get("start_date")

        if not employee_id or not template_id:
            messages.error(request, _("İşçi və şablon seçimləri tələb olunur."))
            return self.get(request, *args, **kwargs)

        employee = get_object_or_404(User, pk=employee_id)
        template = get_object_or_404(OnboardingTemplate, pk=template_id)
        start = timezone.datetime.fromisoformat(start_date) if start_date else timezone.now()
        process = OnboardingProcess.objects.create(
            employee=employee,
            template=template,
            department=employee.department,
            start_date=start.date(),
            created_by=request.user,
        )
        for task_template in template.task_templates.all():
            due_date = start.date() + timedelta(days=task_template.due_in_days)
            OnboardingTask.objects.create(
                process=process,
                template_task=task_template,
                title=task_template.title,
                description=task_template.description,
                task_type=task_template.task_type,
                assigned_to=employee if not task_template.assignee_role else None,
                due_date=due_date,
                metadata=task_template.metadata_schema,
            )
        messages.success(request, _("Onboarding prosesi yaradıldı."))
        return redirect("onboarding:process-detail", pk=process.pk)


class ProcessStatusActionView(LoginRequiredMixin, View):
    action = None

    def get(self, request, pk):
        return self.post(request, pk)

    def post(self, request, pk):
        process = get_object_or_404(OnboardingProcess, pk=pk)
        if self.action == "complete":
            process.status = "completed"
            process.save(update_fields=["status", "updated_at"])
            messages.success(request, _("Proses tamamlandı."))
        elif self.action == "cancel":
            process.status = "cancelled"
            process.save(update_fields=["status", "updated_at"])
            messages.info(request, _("Proses ləğv edildi."))
        return redirect("onboarding:process-detail", pk=pk)


class CompleteTaskView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return self.post(request, pk)

    def post(self, request, pk):
        task = get_object_or_404(OnboardingTask.objects.select_related("process"), pk=pk)
        task.mark_completed(user=request.user)
        messages.success(request, _("Tapşırıq tamamlandı."))
        return redirect("onboarding:process-detail", pk=task.process_id)


class ProcessNoteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Placeholder for future implementation
        note = request.POST.get("note")
        if note:
            messages.success(request, _("Qeyd qəbul edildi."))
        return redirect("onboarding:process-detail", pk=pk)


class ProcessCompleteView(ProcessStatusActionView):
    action = "complete"


class ProcessCancelView(ProcessStatusActionView):
    action = "cancel"
