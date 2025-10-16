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

    # Approval workflow (managed via status field)
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

    def submit_for_approval(self):
        """
        Submit goal for approval.
        Can only submit from draft status.
        """
        from django.core.exceptions import ValidationError

        if self.status != 'draft':
            raise ValidationError(
                f'Yalnız qaralama statusunda olan məqsədlər təsdiqə göndərilə bilər. '
                f'Hazırki status: {self.get_status_display()}'
            )

        self.status = 'pending_approval'
        self.save()

    def approve(self, approver, note=''):
        """
        Approve the goal.
        Can only approve from pending_approval status.
        """
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        if self.status != 'pending_approval':
            raise ValidationError(
                f'Yalnız təsdiq gözləyən məqsədlər təsdiq edilə bilər. '
                f'Hazırki status: {self.get_status_display()}'
            )

        self.status = 'active'
        self.approved_by = approver
        self.approved_at = timezone.now()
        self.approval_note = note
        self.save()

    def reject(self, rejector, note=''):
        """
        Reject the goal.
        Can only reject from pending_approval status.
        """
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        if self.status != 'pending_approval':
            raise ValidationError(
                f'Yalnız təsdiq gözləyən məqsədlər rədd edilə bilər. '
                f'Hazırki status: {self.get_status_display()}'
            )

        self.status = 'rejected'
        self.approved_by = rejector
        self.approved_at = timezone.now()
        self.approval_note = note
        self.save()

    def mark_completed(self, completion_note=''):
        """
        Mark goal as completed.
        Can only complete active goals.
        """
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        if self.status != 'active':
            raise ValidationError(
                f'Yalnız aktiv məqsədlər tamamlana bilər. '
                f'Hazırki status: {self.get_status_display()}'
            )

        self.status = 'completed'
        self.completion_date = timezone.now().date()
        self.approval_note = completion_note
        self.save()

    def cancel(self, cancel_note=''):
        """
        Cancel the goal.
        Can cancel from any status except completed.
        """
        from django.core.exceptions import ValidationError

        if self.status == 'completed':
            raise ValidationError('Tamamlanmış məqsədlər ləğv edilə bilməz.')

        self.status = 'cancelled'
        self.approval_note = cancel_note
        self.save()


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


# Import OKR models
from .models_okr import StrategicObjective, KeyResult, KPI, KPIMeasurement
