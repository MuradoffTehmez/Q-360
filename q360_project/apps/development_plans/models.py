"""Models for development plans app."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class DevelopmentGoal(models.Model):
    """Individual development goals based on evaluation results."""

    STATUS_CHOICES = [
        ('draft', 'Qaralama'),
        ('pending_approval', 'Təsdiq Gözləyir'),
        ('active', 'Aktiv'),
        ('completed', 'Tamamlanmış'),
        ('cancelled', 'Ləğv Edilmiş'),
        ('rejected', 'Rədd Edilmiş'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='development_goals')
    title = models.CharField(max_length=200, verbose_name=_('Məqsəd'))
    description = models.TextField(verbose_name=_('Təsvir'))
    category = models.CharField(max_length=100, verbose_name=_('Kateqoriya'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    target_date = models.DateField(verbose_name=_('Hədəf Tarixi'))
    completion_date = models.DateField(null=True, blank=True)

    # Approval workflow
    is_approved = models.BooleanField(default=False, verbose_name=_('Təsdiqlənib'))
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_goals')
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_note = models.TextField(blank=True, verbose_name=_('Təsdiq Qeydi'))

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_goals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('İnkişaf Məqsədi')
        verbose_name_plural = _('İnkişaf Məqsədləri')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ProgressLog(models.Model):
    """Progress tracking for development goals."""

    goal = models.ForeignKey(DevelopmentGoal, on_delete=models.CASCADE, related_name='progress_logs')
    note = models.TextField(verbose_name=_('Qeyd'))
    progress_percentage = models.IntegerField(default=0, verbose_name=_('İrəliləyiş %'))
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_draft = models.BooleanField(default=False, verbose_name=_('Layihə'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('İrəliləyiş Qeydi')
        verbose_name_plural = _('İrəliləyiş Qeydləri')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.goal.title} - {self.progress_percentage}%"
