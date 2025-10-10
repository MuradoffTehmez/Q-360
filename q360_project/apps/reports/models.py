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
