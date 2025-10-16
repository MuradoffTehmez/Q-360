"""
OKR (Objectives and Key Results) models for goal cascading.
Supports strategic goal alignment from organization → department → individual.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from apps.departments.models import Department


class StrategicObjective(models.Model):
    """
    Organization-level strategic objectives.
    Top-level goals that cascade down to departments and individuals.
    """

    LEVEL_CHOICES = [
        ('organization', 'Təşkilat'),
        ('department', 'Şöbə'),
        ('individual', 'Fərdi'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Qaralama'),
        ('active', 'Aktiv'),
        ('completed', 'Tamamlanmış'),
        ('cancelled', 'Ləğv Edilmiş'),
    ]

    QUARTER_CHOICES = [
        ('Q1', '1-ci Rüb'),
        ('Q2', '2-ci Rüb'),
        ('Q3', '3-cü Rüb'),
        ('Q4', '4-cü Rüb'),
        ('annual', 'İllik'),
    ]

    title = models.CharField(
        max_length=300,
        verbose_name=_('Məqsəd')
    )
    description = models.TextField(
        verbose_name=_('Təsvir')
    )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='organization',
        verbose_name=_('Səviyyə')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('Status')
    )

    # Ownership
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_objectives',
        verbose_name=_('Məsul Şəxs')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='objectives',
        verbose_name=_('Şöbə')
    )

    # Hierarchy (for cascading)
    parent_objective = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_objectives',
        verbose_name=_('Əsas Məqsəd')
    )

    # Timeline
    fiscal_year = models.IntegerField(
        verbose_name=_('Maliyyə İli')
    )
    quarter = models.CharField(
        max_length=10,
        choices=QUARTER_CHOICES,
        default='annual',
        verbose_name=_('Rüb')
    )
    start_date = models.DateField(
        verbose_name=_('Başlanğıc Tarixi')
    )
    end_date = models.DateField(
        verbose_name=_('Bitmə Tarixi')
    )

    # Progress tracking
    progress_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        verbose_name=_('İrəliləyiş %')
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('100.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        verbose_name=_('Çəki %')
    )

    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_objectives',
        verbose_name=_('Yaradan')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Strateji Məqsəd')
        verbose_name_plural = _('Strateji Məqsədlər')
        ordering = ['-fiscal_year', '-created_at']
        indexes = [
            models.Index(fields=['level', 'status']),
            models.Index(fields=['fiscal_year', 'quarter']),
            models.Index(fields=['owner']),
            models.Index(fields=['department']),
        ]

    def __str__(self):
        return f"{self.title} ({self.fiscal_year} - {self.quarter})"

    def update_progress(self):
        """
        Update progress based on key results.
        Automatically calculates weighted average of all key results.
        """
        key_results = self.key_results.filter(is_active=True)
        if not key_results.exists():
            return

        total_weight = sum(kr.weight for kr in key_results)
        if total_weight == 0:
            return

        weighted_progress = sum(
            (kr.current_value / kr.target_value * 100 if kr.target_value > 0 else 0) * kr.weight
            for kr in key_results
        )

        self.progress_percentage = Decimal(str(weighted_progress / total_weight))
        self.save(update_fields=['progress_percentage', 'updated_at'])

    def cascade_to_departments(self):
        """Create department-level objectives from organization-level objective."""
        if self.level != 'organization':
            return

        departments = Department.objects.filter(is_active=True)
        for dept in departments:
            StrategicObjective.objects.create(
                title=f"{self.title} - {dept.name}",
                description=self.description,
                level='department',
                status='draft',
                department=dept,
                owner=dept.manager if hasattr(dept, 'manager') else None,
                parent_objective=self,
                fiscal_year=self.fiscal_year,
                quarter=self.quarter,
                start_date=self.start_date,
                end_date=self.end_date,
                created_by=self.created_by
            )


class KeyResult(models.Model):
    """
    Key Results for measuring objective achievement.
    Each objective has multiple measurable key results.
    """

    UNIT_CHOICES = [
        ('number', 'Ədəd'),
        ('percentage', 'Faiz'),
        ('currency', 'Valyuta'),
        ('boolean', 'Hə/Yox'),
    ]

    objective = models.ForeignKey(
        StrategicObjective,
        on_delete=models.CASCADE,
        related_name='key_results',
        verbose_name=_('Məqsəd')
    )
    title = models.CharField(
        max_length=300,
        verbose_name=_('Açar Nəticə')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )

    # Measurement
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default='number',
        verbose_name=_('Ölçü Vahidi')
    )
    baseline_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_('Başlanğıc Dəyər')
    )
    target_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Hədəf Dəyər')
    )
    current_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_('Cari Dəyər')
    )

    # Weight in objective
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('100.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        verbose_name=_('Çəki %')
    )

    # Metadata
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Açar Nəticə')
        verbose_name_plural = _('Açar Nəticələr')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['objective']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.objective.title} - {self.title}"

    @property
    def progress_percentage(self):
        """Calculate progress percentage."""
        if self.target_value == 0:
            return Decimal('0.00')
        return (self.current_value / self.target_value * 100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update parent objective progress
        self.objective.update_progress()


class KPI(models.Model):
    """
    Key Performance Indicators for tracking performance metrics.
    Can be linked to objectives or standalone.
    """

    FREQUENCY_CHOICES = [
        ('daily', 'Gündəlik'),
        ('weekly', 'Həftəlik'),
        ('monthly', 'Aylıq'),
        ('quarterly', 'Rüblük'),
        ('annual', 'İllik'),
    ]

    TREND_CHOICES = [
        ('up', 'Yuxarı'),
        ('down', 'Aşağı'),
        ('stable', 'Sabit'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name=_('KPI Adı')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('KPI Kodu')
    )

    # Ownership
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_kpis',
        verbose_name=_('Məsul Şəxs')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='kpis',
        verbose_name=_('Şöbə')
    )

    # Link to objective
    objective = models.ForeignKey(
        StrategicObjective,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='kpis',
        verbose_name=_('Strateji Məqsəd')
    )

    # Measurement
    unit = models.CharField(
        max_length=50,
        verbose_name=_('Ölçü Vahidi')
    )
    target_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Hədəf Dəyər')
    )
    measurement_frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='monthly',
        verbose_name=_('Ölçmə Tezliyi')
    )

    # Thresholds
    red_threshold = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Qırmızı Həddi')
    )
    yellow_threshold = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Sarı Həddi')
    )
    green_threshold = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Yaşıl Həddi')
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('KPI')
        verbose_name_plural = _('KPI-lər')
        ordering = ['name']
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['department']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class KPIMeasurement(models.Model):
    """
    Actual measurements for KPIs over time.
    """

    kpi = models.ForeignKey(
        KPI,
        on_delete=models.CASCADE,
        related_name='measurements',
        verbose_name=_('KPI')
    )
    measurement_date = models.DateField(
        verbose_name=_('Ölçmə Tarixi')
    )
    actual_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Faktiki Dəyər')
    )
    trend = models.CharField(
        max_length=10,
        choices=KPI.TREND_CHOICES,
        null=True,
        blank=True,
        verbose_name=_('Tendensiya')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )
    measured_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='kpi_measurements',
        verbose_name=_('Ölçən')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('KPI Ölçməsi')
        verbose_name_plural = _('KPI Ölçmələri')
        ordering = ['-measurement_date']
        unique_together = ['kpi', 'measurement_date']
        indexes = [
            models.Index(fields=['kpi', 'measurement_date']),
        ]

    def __str__(self):
        return f"{self.kpi.code} - {self.measurement_date}: {self.actual_value}"

    @property
    def status_color(self):
        """Determine status color based on thresholds."""
        if self.actual_value >= self.kpi.green_threshold:
            return 'green'
        elif self.actual_value >= self.kpi.yellow_threshold:
            return 'yellow'
        else:
            return 'red'

    @property
    def achievement_percentage(self):
        """Calculate achievement percentage."""
        if self.kpi.target_value == 0:
            return Decimal('0.00')
        return (self.actual_value / self.kpi.target_value * 100)
