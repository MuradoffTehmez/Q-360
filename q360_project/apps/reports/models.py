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
