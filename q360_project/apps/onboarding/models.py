"""
Core models for the onboarding automation module.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Optional

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


ROLE_CHOICES = [
    ("superadmin", _("Super Administrator")),
    ("admin", _("Administrator")),
    ("manager", _("Menecer")),
    ("employee", _("İşçi")),
]


class OnboardingTemplate(models.Model):
    """
    Template that defines the default onboarding flow for new employees.
    """

    name = models.CharField(max_length=150, verbose_name=_("Şablon Adı"))
    slug = models.SlugField(max_length=160, unique=True, verbose_name=_("Slug"))
    description = models.TextField(blank=True, verbose_name=_("Təsvir"))
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Defolt Şablon"),
        help_text=_("Yeni işçilər üçün avtomatik seçilən şablon."),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Aktivdir"))
    review_cycle_offset_days = models.PositiveIntegerField(
        default=90,
        verbose_name=_("Performans Qiymətləndirmə Startı (gün)"),
        help_text=_("İşçinin start tarixindən neçə gün sonra qiymətləndirmə kampaniyası başlasın."),
    )
    salary_review_offset_days = models.PositiveIntegerField(
        default=60,
        verbose_name=_("Maaş İcmalı Startı (gün)"),
        help_text=_("İşçinin start tarixindən neçə gün sonra maaş təklifi hazırlansın."),
    )
    training_plan_offset_days = models.PositiveIntegerField(
        default=14,
        verbose_name=_("Təlim Planı Startı (gün)"),
        help_text=_("İşçinin start tarixindən neçə gün sonra təlim planı yaradılsın."),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaradılma Tarixi"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yenilənmə Tarixi"))

    class Meta:
        verbose_name = _("Onboarding Şablonu")
        verbose_name_plural = _("Onboarding Şablonları")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        """Ensure only a single template is flagged as default at a time."""
        super().clean()
        if self.is_default:
            existing_default = OnboardingTemplate.objects.filter(is_default=True).exclude(pk=self.pk)
            if existing_default.exists():
                raise ValidationError(
                    {"is_default": _("Artıq defolt şablon mövcuddur. Əvvəlkini deaktiv edin.")}
                )

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class OnboardingTaskTemplate(models.Model):
    """
    Individual task definition that belongs to an onboarding template.
    """

    TASK_TYPE_CHOICES = [
        ("general", _("Ümumi Tapşırıq")),
        ("performance_review", _("Performans Qiymətləndirmə Başlat")),
        ("salary_recommendation", _("Maaş Artımı Tövsiyəsi")),
        ("training_plan", _("Təlim Planı Yarat")),
    ]

    template = models.ForeignKey(
        OnboardingTemplate,
        on_delete=models.CASCADE,
        related_name="task_templates",
        verbose_name=_("Şablon"),
    )
    title = models.CharField(max_length=200, verbose_name=_("Başlıq"))
    description = models.TextField(blank=True, verbose_name=_("Təsvir"))
    task_type = models.CharField(
        max_length=40,
        choices=TASK_TYPE_CHOICES,
        default="general",
        verbose_name=_("Tapşırıq Tipi"),
    )
    due_in_days = models.PositiveIntegerField(
        default=7,
        verbose_name=_("Son Tarix (gün)"),
        help_text=_("Onboarding start tarixindən neçə gün sonra tamamlanmalıdır."),
    )
    assignee_role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        blank=True,
        verbose_name=_("Məsul Rol"),
        help_text=_("Boş olduqda tapşırıq işçiyə təyin ediləcək."),
    )
    auto_complete = models.BooleanField(
        default=False,
        verbose_name=_("Avtomatik Tamamla"),
        help_text=_("İnteqrasiya uğurla başa çatdıqda tapşırıq avtomatik tamamlanır."),
    )
    metadata_schema = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Metadata Sxemi"),
        help_text=_("İnteqrasiya məlumatları üçün JSON təsviri."),
    )
    order = models.PositiveIntegerField(default=1, verbose_name=_("Sıra"))

    class Meta:
        verbose_name = _("Onboarding Tapşırıq Şablonu")
        verbose_name_plural = _("Onboarding Tapşırıq Şablonları")
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.template.name} → {self.title}"


class OnboardingProcess(models.Model):
    """
    Concrete onboarding workflow for a specific employee.
    """

    STATUS_CHOICES = [
        ("draft", _("Qaralama")),
        ("active", _("Aktiv")),
        ("completed", _("Tamamlandı")),
        ("cancelled", _("Ləğv edildi")),
    ]

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="onboarding_processes",
        verbose_name=_("İşçi"),
    )
    template = models.ForeignKey(
        OnboardingTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processes",
        verbose_name=_("Şablon"),
    )
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="onboarding_processes",
        verbose_name=_("Şöbə"),
    )
    start_date = models.DateField(default=timezone.now, verbose_name=_("Başlama Tarixi"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", verbose_name=_("Status"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="initiated_onboarding_processes",
        verbose_name=_("Yaradan"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaradılma Tarixi"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yenilənmə Tarixi"))

    class Meta:
        verbose_name = _("Onboarding Prosesi")
        verbose_name_plural = _("Onboarding Prosesləri")
        ordering = ["-created_at"]
        unique_together = [["employee", "status"]]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["employee", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.employee.get_full_name()} ({self.get_status_display()})"

    def activate(self) -> None:
        if self.status == "draft":
            self.status = "active"
            self.save(update_fields=["status", "updated_at"])

    def mark_completed(self) -> None:
        self.status = "completed"
        self.save(update_fields=["status", "updated_at"])

    def completion_rate(self) -> Decimal:
        total = self.tasks.count()
        if total == 0:
            return Decimal("0")
        completed = self.tasks.filter(status="completed").count()
        return (Decimal(completed) / Decimal(total)) * Decimal("100")


class OnboardingTask(models.Model):
    """
    Track the execution of onboarding tasks for the employee.
    """

    STATUS_CHOICES = [
        ("pending", _("Gözləyir")),
        ("in_progress", _("İcrada")),
        ("completed", _("Tamamlandı")),
        ("blocked", _("Bloklanıb")),
        ("skipped", _("Atlandı")),
    ]

    process = models.ForeignKey(
        OnboardingProcess,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name=_("Prosess"),
    )
    template_task = models.ForeignKey(
        OnboardingTaskTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_tasks",
        verbose_name=_("Tapşırıq Şablonu"),
    )
    title = models.CharField(max_length=200, verbose_name=_("Başlıq"))
    description = models.TextField(blank=True, verbose_name=_("Təsvir"))
    task_type = models.CharField(max_length=40, default="general", verbose_name=_("Tapşırıq Tipi"))
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="people_onboarding_tasks",
        verbose_name=_("Məsul Şəxs"),
    )
    due_date = models.DateField(null=True, blank=True, verbose_name=_("Son Tarix"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name=_("Status"))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("Əlavə Məlumat"))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Tamamlama Tarixi"))
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="completed_onboarding_tasks",
        verbose_name=_("Tamamlayan"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaradılma Tarixi"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yenilənmə Tarixi"))

    class Meta:
        verbose_name = _("Onboarding Tapşırığı")
        verbose_name_plural = _("Onboarding Tapşırıqları")
        ordering = ["due_date", "id"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["task_type"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.process.employee.get_full_name()} → {self.title}"

    def mark_completed(self, user: Optional[models.Model] = None, metadata: Optional[dict] = None) -> None:
        self.status = "completed"
        self.completed_at = timezone.now()
        if user:
            self.completed_by = user
        if metadata:
            self.metadata = {**self.metadata, **metadata}
        self.save(update_fields=["status", "completed_at", "completed_by", "metadata", "updated_at"])


class MarketSalaryBenchmark(models.Model):
    """
    Market benchmark data used for salary recommendation automation.
    """

    ROLE_LEVEL_CHOICES = [
        ("entry", _("Başlanğıc")),
        ("mid", _("Orta Səviyyə")),
        ("senior", _("Təcrübəli")),
        ("lead", _("Rəhbər")),
    ]

    title = models.CharField(max_length=200, verbose_name=_("Vəzifə / Rol"))
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="salary_benchmarks",
        verbose_name=_("Şöbə"),
    )
    role_level = models.CharField(
        max_length=20,
        choices=ROLE_LEVEL_CHOICES,
        default="mid",
        verbose_name=_("Səviyyə"),
    )
    currency = models.CharField(max_length=3, default="AZN", verbose_name=_("Valyuta"))
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Minimum Maaş"))
    median_salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Median Maaş"))
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Maksimum Maaş"))
    data_source = models.CharField(max_length=255, blank=True, verbose_name=_("Məlumat Mənbəyi"))
    effective_date = models.DateField(default=timezone.now, verbose_name=_("Tarix"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaradılma Tarixi"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yenilənmə Tarixi"))

    class Meta:
        verbose_name = _("Market Maaş Benchmark")
        verbose_name_plural = _("Market Maaş Benchmarkları")
        ordering = ["-effective_date", "title"]
        indexes = [
            models.Index(fields=["title", "role_level"]),
            models.Index(fields=["department", "role_level"]),
            models.Index(fields=["effective_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.get_role_level_display()})"

    def recommended_salary(self, weight: Decimal = Decimal("0.5")) -> Decimal:
        """
        Calculate a weighted recommendation leaning towards the top quartile.
        """
        weight = min(max(weight, Decimal("0")), Decimal("1"))
        spread = self.max_salary - self.median_salary
        return self.median_salary + (spread * weight)
