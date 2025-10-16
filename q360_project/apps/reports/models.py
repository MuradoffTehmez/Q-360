"""Models for reports app."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.evaluations.models import EvaluationCampaign


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
