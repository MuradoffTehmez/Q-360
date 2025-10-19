"""
Django admin registrations for onboarding module.
"""
from django.contrib import admin

from .models import (
    MarketSalaryBenchmark,
    OnboardingProcess,
    OnboardingTask,
    OnboardingTaskTemplate,
    OnboardingTemplate,
)


@admin.register(OnboardingTemplate)
class OnboardingTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "is_default", "is_active", "review_cycle_offset_days", "updated_at")
    list_filter = ("is_default", "is_active")
    search_fields = ("name", "description")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class OnboardingTaskInline(admin.TabularInline):
    model = OnboardingTask
    extra = 0
    ordering = ("due_date",)
    readonly_fields = ("title", "task_type", "status", "due_date", "assigned_to")


@admin.register(OnboardingProcess)
class OnboardingProcessAdmin(admin.ModelAdmin):
    list_display = ("employee", "status", "template", "start_date", "created_at")
    list_filter = ("status", "template")
    search_fields = ("employee__username", "employee__first_name", "employee__last_name")
    date_hierarchy = "start_date"
    autocomplete_fields = ("employee", "template", "department", "created_by")
    inlines = [OnboardingTaskInline]


@admin.register(OnboardingTask)
class OnboardingTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "process", "task_type", "status", "due_date")
    list_filter = ("task_type", "status")
    search_fields = ("title", "process__employee__username", "process__employee__first_name")
    autocomplete_fields = ("process", "template_task", "assigned_to", "completed_by")
    date_hierarchy = "due_date"


@admin.register(OnboardingTaskTemplate)
class OnboardingTaskTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "template", "task_type", "due_in_days", "order")
    list_filter = ("task_type", "template")
    search_fields = ("title", "template__name")
    ordering = ("template", "order")


@admin.register(MarketSalaryBenchmark)
class MarketSalaryBenchmarkAdmin(admin.ModelAdmin):
    list_display = ("title", "role_level", "currency", "median_salary", "effective_date")
    list_filter = ("role_level", "currency", "department")
    search_fields = ("title", "data_source")
    autocomplete_fields = ("department",)
    date_hierarchy = "effective_date"
