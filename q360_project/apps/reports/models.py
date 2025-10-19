"""Models for reports app."""
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.evaluations.models import EvaluationCampaign


def default_schedule_time():
    """Return default time of day for scheduled reports."""
    return timezone.localtime().time()


class Report(models.Model):
    """Generated reports for evaluations."""

    REPORT_TYPES = [
        ('individual', 'Fərdi Hesabat'),
        ('department', 'Şöbə Hesabatı'),
        ('organization', 'Təşkilat Hesabatı'),
        ('comparative', 'Müqayisəli Hesabat'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
    campaign = models.ForeignKey(EvaluationCampaign, on_delete=models.CASCADE, related_name='reports')
    generated_for = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='generated_reports')
    file_path = models.FileField(upload_to='reports/', blank=True)
    data = models.JSONField(default=dict, verbose_name=_('Hesabat Məlumatları'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Hesabat')
        verbose_name_plural = _('Hesabatlar')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.created_at.date()}"


class RadarChartData(models.Model):
    """Stores radar chart data for competency visualization."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(EvaluationCampaign, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    self_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    others_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Radar Qrafik Məlumatı')
        verbose_name_plural = _('Radar Qrafik Məlumatları')
        unique_together = [['user', 'campaign', 'category']]

    def __str__(self):
        return f"{self.user.username} - {self.category}"


class ReportGenerationLog(models.Model):
    """
    Tracks asynchronous report generation tasks.
    Stores status, progress, and generated files.
    """

    REPORT_TYPE_CHOICES = [
        ('pdf', 'PDF Hesabat'),
        ('excel', 'Excel Hesabat'),
        ('csv', 'CSV Hesabat'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('processing', 'İşlənir'),
        ('completed', 'Tamamlandı'),
        ('failed', 'Uğursuz'),
    ]

    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPE_CHOICES,
        verbose_name=_('Hesabat Növü')
    )
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='report_requests',
        verbose_name=_('Tələb edən')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    file = models.FileField(
        upload_to='generated_reports/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_('Hesabat Faylı')
    )
    metadata = models.JSONField(
        default=dict,
        verbose_name=_('Metadata'),
        help_text=_('Task ID, parameterlər və s.')
    )
    error_message = models.TextField(
        blank=True,
        verbose_name=_('Xəta Mesajı')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Tamamlanma Tarixi')
    )

    class Meta:
        verbose_name = _('Hesabat Yaratma Loqu')
        verbose_name_plural = _('Hesabat Yaratma Loqları')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['requested_by', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.requested_by.username} ({self.get_status_display()})"

    def get_download_url(self):
        """Get download URL for completed report."""
        if self.status == 'completed' and self.file:
            return f'/reports/download/{self.pk}/'
        return None


class SystemKPI(models.Model):
    """
    System-wide KPI tracking for admin analytics dashboard.
    Stores daily snapshots of key performance indicators.
    """

    date = models.DateField(
        unique=True,
        verbose_name=_('Tarix'),
        help_text=_('KPI snapshot tarixi')
    )

    # User metrics
    total_users = models.IntegerField(
        default=0,
        verbose_name=_('Ümumi İstifadəçilər')
    )
    active_users = models.IntegerField(
        default=0,
        verbose_name=_('Aktiv İstifadəçilər')
    )
    new_users_today = models.IntegerField(
        default=0,
        verbose_name=_('Bu gün qeydiyyatdan keçənlər')
    )
    users_logged_in_today = models.IntegerField(
        default=0,
        verbose_name=_('Bu gün giriş edənlər')
    )

    # Evaluation metrics
    total_campaigns = models.IntegerField(
        default=0,
        verbose_name=_('Ümumi Kampaniyalar')
    )
    active_campaigns = models.IntegerField(
        default=0,
        verbose_name=_('Aktiv Kampaniyalar')
    )
    total_evaluations = models.IntegerField(
        default=0,
        verbose_name=_('Ümumi Qiymətləndirmələr')
    )
    completed_evaluations = models.IntegerField(
        default=0,
        verbose_name=_('Tamamlanmış Qiymətləndirmələr')
    )
    evaluations_completed_today = models.IntegerField(
        default=0,
        verbose_name=_('Bu gün tamamlananlar')
    )
    completion_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_('Tamamlanma Faizi')
    )

    # Department metrics
    total_departments = models.IntegerField(
        default=0,
        verbose_name=_('Ümumi Şöbələr')
    )

    # Training metrics
    total_trainings = models.IntegerField(
        default=0,
        verbose_name=_('Ümumi Təlimlər')
    )
    active_trainings = models.IntegerField(
        default=0,
        verbose_name=_('Davam edən Təlimlər')
    )

    # Security metrics
    login_attempts_today = models.IntegerField(
        default=0,
        verbose_name=_('Bu gün giriş cəhdləri')
    )
    failed_login_attempts_today = models.IntegerField(
        default=0,
        verbose_name=_('Bu gün uğursuz girişlər')
    )
    security_threats_detected = models.IntegerField(
        default=0,
        verbose_name=_('Aşkar edilmiş təhlükələr')
    )

    # System health
    average_response_time = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name=_('Orta cavab müddəti (ms)'),
        help_text=_('Millisaniyə ilə')
    )
    database_size_mb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Verilənlər bazası ölçüsü (MB)')
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    class Meta:
        verbose_name = _('Sistem KPI')
        verbose_name_plural = _('Sistem KPI-ləri')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
        ]

    def __str__(self):
        return f"KPI - {self.date}"

    @classmethod
    def calculate_today_kpis(cls):
        """
        Calculate and save KPIs for today.
        Should be called by a daily scheduled task (Celery beat).
        """
        from datetime import date, timedelta
        from django.utils import timezone
        from django.db.models import Count, Avg
        from apps.accounts.models import User
        from apps.evaluations.models import EvaluationCampaign, EvaluationAssignment
        from apps.departments.models import Department
        from apps.training.models import TrainingResource, UserTraining
        from apps.audit.models import AuditLog

        today = date.today()
        yesterday = today - timedelta(days=1)

        # User metrics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        new_users_today = User.objects.filter(date_joined__date=today).count()

        # Users who logged in today
        users_logged_in_today = AuditLog.objects.filter(
            action='login_success',
            created_at__date=today
        ).values('user').distinct().count()

        # Evaluation metrics
        total_campaigns = EvaluationCampaign.objects.count()
        active_campaigns = EvaluationCampaign.objects.filter(status='active').count()
        total_evaluations = EvaluationAssignment.objects.count()
        completed_evaluations = EvaluationAssignment.objects.filter(status='completed').count()
        evaluations_completed_today = EvaluationAssignment.objects.filter(
            completed_at__date=today
        ).count()

        completion_rate = 0
        if total_evaluations > 0:
            completion_rate = (completed_evaluations / total_evaluations) * 100

        # Department metrics
        total_departments = Department.objects.count()

        # Training metrics
        total_trainings = TrainingResource.objects.count()
        active_trainings = UserTraining.objects.filter(status='in_progress').count()

        # Security metrics
        login_attempts_today = AuditLog.objects.filter(
            action__in=['login_success', 'login_failure'],
            created_at__date=today
        ).count()
        failed_login_attempts_today = AuditLog.objects.filter(
            action='login_failure',
            created_at__date=today
        ).count()

        # Create or update KPI record
        kpi, created = cls.objects.update_or_create(
            date=today,
            defaults={
                'total_users': total_users,
                'active_users': active_users,
                'new_users_today': new_users_today,
                'users_logged_in_today': users_logged_in_today,
                'total_campaigns': total_campaigns,
                'active_campaigns': active_campaigns,
                'total_evaluations': total_evaluations,
                'completed_evaluations': completed_evaluations,
                'evaluations_completed_today': evaluations_completed_today,
                'completion_rate': round(completion_rate, 2),
                'total_departments': total_departments,
                'total_trainings': total_trainings,
                'active_trainings': active_trainings,
                'login_attempts_today': login_attempts_today,
                'failed_login_attempts_today': failed_login_attempts_today,
            }
        )

        return kpi


class ReportBlueprint(models.Model):
    """
    Custom report definitions supporting configurable datasets and exports.
    """

    DATA_SOURCE_CHOICES = [
        ('evaluations', _('Qiymətləndirmələr')),
        ('training', _('Təlim Resursları')),
        ('compensation', _('Kompensasiya')),
        ('workforce', _('İşçi Məlumatları')),
    ]

    EXPORT_FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='report_blueprints',
        verbose_name=_('Müəllif')
    )
    title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
    slug = models.SlugField(max_length=210, unique=True, verbose_name=_('Slug'))
    description = models.TextField(blank=True, verbose_name=_('Təsvir'))
    data_source = models.CharField(
        max_length=50,
        choices=DATA_SOURCE_CHOICES,
        default='evaluations',
        verbose_name=_('Məlumat Mənbəyi')
    )
    configuration = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Konfiqurasiya'),
        help_text=_('Seçilmiş sahələr, aqreqasiyalar və vizual komponentlər.')
    )
    default_filters = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Defolt Filtrlər')
    )
    columns = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_('Sütunlar')
    )
    default_export_format = models.CharField(
        max_length=10,
        choices=EXPORT_FORMAT_CHOICES,
        default='excel',
        verbose_name=_('Defolt Export Formatı')
    )
    is_global = models.BooleanField(default=False, verbose_name=_('Hamı üçün əlçatan'))
    is_active = models.BooleanField(default=True, verbose_name=_('Aktivdir'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaradılma Tarixi'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Yenilənmə Tarixi'))

    class Meta:
        verbose_name = _('Hesabat Şablonu')
        verbose_name_plural = _('Hesabat Şablonları')
        ordering = ['title']
        indexes = [
            models.Index(fields=['data_source', 'is_active']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_columns(self):
        if self.columns:
            return self.columns
        defaults = {
            'evaluations': ['Kampaniya', 'İştirakçı Sayı', 'Ortalama Bal'],
            'training': ['Təlim', 'Növ', 'Çatdırılma', 'Çətinlik'],
            'compensation': ['İşçi', 'Maaş', 'Valyuta', 'Qüvvəyə minmə'],
            'workforce': ['Şöbə', 'İşçi Sayı', 'Menecer'],
        }
        return defaults.get(self.data_source, [])


class ReportVisualization(models.Model):
    """
    Visualization configuration for a report blueprint.
    """

    CHART_TYPE_CHOICES = [
        ('bar', _('Sütun Diaqramı')),
        ('line', _('Xətt Diaqramı')),
        ('pie', _('Piroq Diaqramı')),
        ('radar', _('Radar Diaqramı')),
        ('table', _('Cədvəl')),
    ]

    blueprint = models.ForeignKey(
        ReportBlueprint,
        on_delete=models.CASCADE,
        related_name='visualizations',
        verbose_name=_('Hesabat Şablonu')
    )
    title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
    chart_type = models.CharField(
        max_length=20,
        choices=CHART_TYPE_CHOICES,
        default='table',
        verbose_name=_('Diaqram Tipi')
    )
    configuration = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Vizual Konfiqurasiya')
    )
    order = models.PositiveIntegerField(default=1, verbose_name=_('Sıra'))
    is_primary = models.BooleanField(default=False, verbose_name=_('Əsas Vizual'))

    class Meta:
        verbose_name = _('Hesabat Vizualı')
        verbose_name_plural = _('Hesabat Vizuaları')
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.blueprint.title} → {self.title}"


class CustomReport(models.Model):
    """
    User-defined custom report configuration.
    """

    name = models.CharField(max_length=200, verbose_name=_('Ad'))
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='custom_reports',
        verbose_name=_('Müəllif'),
    )
    description = models.TextField(blank=True, verbose_name=_('Təsvir'))
    blueprint = models.ForeignKey(
        ReportBlueprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='custom_reports',
        verbose_name=_('Əsas Şablon'),
    )
    configuration = models.JSONField(default=dict, blank=True, verbose_name=_('Konfiqurasiya'))
    query_definition = models.JSONField(default=dict, blank=True, verbose_name=_('Sorğu Tərifi'))
    columns = models.JSONField(default=list, blank=True, verbose_name=_('Sütunlar'))
    filters = models.JSONField(default=list, blank=True, verbose_name=_('Filtrlər'))
    visualization = models.JSONField(default=dict, blank=True, verbose_name=_('Vizualizasiyalar'))
    last_run_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Son İcra Vaxtı'))
    last_run_summary = models.JSONField(default=dict, blank=True, verbose_name=_('Son İcra Xülasəsi'))
    is_active = models.BooleanField(default=True, verbose_name=_('Aktivdir'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Fərdi Hesabat')
        verbose_name_plural = _('Fərdi Hesabatlar')
        ordering = ['name']
        indexes = [
            models.Index(fields=['owner', 'is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.name

    def effective_blueprint(self):
        return self.blueprint


class ReportSchedule(models.Model):
    """
    Scheduled exports for custom reports.
    """

    FREQUENCY_CHOICES = [
        ('daily', _('Gündəlik')),
        ('weekly', _('Həftəlik')),
        ('monthly', _('Aylıq')),
        ('once', _('Bir dəfə')),
    ]

    STATUS_CHOICES = [
        ('pending', _('Gözləyir')),
        ('processing', _('İcra olunur')),
        ('completed', _('Tamamlandı')),
        ('failed', _('Uğursuz')),
    ]

    EXPORT_FORMAT_CHOICES = ReportBlueprint.EXPORT_FORMAT_CHOICES

    blueprint = models.ForeignKey(
        ReportBlueprint,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name=_('Hesabat Şablonu')
    )
    custom_report = models.ForeignKey(
        CustomReport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='schedules',
        verbose_name=_('Fərdi Hesabat')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_report_schedules',
        verbose_name=_('Yaradan')
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='weekly',
        verbose_name=_('Tezlik')
    )
    interval = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Interval (ədəd)'),
        help_text=_('Məsələn, 2 yazsanız hər 2 həftədən bir göndəriləcək.')
    )
    run_time = models.TimeField(default=default_schedule_time, verbose_name=_('Göndərilmə Vaxtı'))
    weekday = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Həftənin Günü (0=Bazar ertəsi)'),
        help_text=_('Yalnız həftəlik planlamalar üçün tələb olunur.')
    )
    day_of_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Ayın Günü'),
        help_text=_('Aylıq planlamalar üçün 1-28 arası dəyər tövsiyə olunur.')
    )
    export_format = models.CharField(
        max_length=10,
        choices=EXPORT_FORMAT_CHOICES,
        default='excel',
        verbose_name=_('Export Formatı')
    )
    parameters = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Filtr və Parametrlər')
    )
    recipients = models.ManyToManyField(
        User,
        related_name='report_schedules',
        blank=True,
        verbose_name=_('Qəbul edənlər')
    )
    delivery_emails = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_('Birbaşa E-poçt Ünvanları')
    )
    additional_emails = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_('Birbaşa E-poçt Ünvanları')
    )
    send_email = models.BooleanField(default=True, verbose_name=_('E-poçt Göndər'))
    include_visualizations = models.BooleanField(
        default=True,
        verbose_name=_('Vizualizasiyaları daxil et')
    )
    next_run = models.DateTimeField(null=True, blank=True, verbose_name=_('Növbəti İcra Tarixi'))
    last_run = models.DateTimeField(null=True, blank=True, verbose_name=_('Son İcra Tarixi'))
    last_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Son Status')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Aktivdir'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaradılma Tarixi'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Yenilənmə Tarixi'))

    class Meta:
        verbose_name = _('Hesabat Planlaması')
        verbose_name_plural = _('Hesabat Planlamaları')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'next_run']),
            models.Index(fields=['frequency']),
        ]

    def clean(self):
        if not self.blueprint and not self.custom_report:
            raise ValidationError(_('Şablon və ya fərdi hesabat seçilməlidir.'))
        if self.blueprint and self.custom_report:
            raise ValidationError(_('Şablon və fərdi hesabat eyni vaxtda aktiv ola bilməz.'))

    def get_report_source(self):
        return self.custom_report or self.blueprint

    def __str__(self):
        source = self.get_report_source()
        source_name = getattr(source, 'title', None) or getattr(source, 'name', None) or _("Hesabat")
        return f"{source_name} ({self.get_frequency_display()})"

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.next_run is None:
            self.next_run = self.calculate_next_run()
        super().save(*args, **kwargs)

    def calculate_next_run(self, reference=None):
        """
        Calculate the next run timestamp based on frequency and interval.
        """
        reference = reference or timezone.now()
        scheduled_time = timezone.make_aware(
            timezone.datetime.combine(reference.date(), self.run_time)
        ) if timezone.is_naive(reference) else reference.replace(
            hour=self.run_time.hour,
            minute=self.run_time.minute,
            second=0,
            microsecond=0,
        )

        if self.frequency == 'daily':
            delta = timedelta(days=self.interval)
            return scheduled_time + delta

        if self.frequency == 'weekly':
            weekday = self.weekday if self.weekday is not None else scheduled_time.weekday()
            days_ahead = (weekday - scheduled_time.weekday()) % 7
            next_run = scheduled_time + timedelta(days=days_ahead)
            if next_run <= reference:
                next_run += timedelta(weeks=self.interval)
            return next_run

        if self.frequency == 'monthly':
            day = self.day_of_month or scheduled_time.day
            month = scheduled_time.month
            year = scheduled_time.year
            month += self.interval
            while month > 12:
                month -= 12
                year += 1
            day = min(day, 28)
            next_run = timezone.make_aware(
                timezone.datetime(year, month, day, self.run_time.hour, self.run_time.minute)
            )
            if next_run <= reference:
                return self.calculate_next_run(reference=next_run + timedelta(days=1))
            return next_run

        if self.frequency == 'once':
            if self.next_run:
                return None
            return scheduled_time if scheduled_time > reference else reference

        return scheduled_time + timedelta(days=1)

    def mark_run(self, status, run_time=None):
        self.last_status = status
        self.last_run = run_time or timezone.now()
        self.next_run = self.calculate_next_run(reference=self.last_run)
        self.save(update_fields=['last_status', 'last_run', 'next_run', 'updated_at'])


class ScheduledReport(ReportSchedule):
    """Proxy model to expose ReportSchedule with a friendlier name."""

    class Meta:
        proxy = True
        verbose_name = _('Cədvəl Hesabatı')
        verbose_name_plural = _('Cədvəl Hesabatları')


class ReportScheduleLog(models.Model):
    """
    Execution log for scheduled reports.
    """

    STATUS_CHOICES = ReportSchedule.STATUS_CHOICES

    schedule = models.ForeignKey(
        ReportSchedule,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name=_('Planlama')
    )
    triggered_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Başlama Tarixi'))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Tamamlanma Tarixi'))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    export_log = models.ForeignKey(
        ReportGenerationLog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='schedule_logs',
        verbose_name=_('Export Qeydi')
    )
    message = models.TextField(blank=True, verbose_name=_('Mesaj'))

    class Meta:
        verbose_name = _('Planlama Loqu')
        verbose_name_plural = _('Planlama Loqları')
        ordering = ['-triggered_at']

    def __str__(self):
        return f"{self.schedule} → {self.get_status_display()}"
