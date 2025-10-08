"""Models for audit app."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class AuditLog(models.Model):
    """Comprehensive audit trail for system actions."""

    ACTION_TYPES = [
        ('create', 'Yaratma'),
        ('update', 'Yenilənmə'),
        ('delete', 'Silinmə'),
        ('login', 'Giriş'),
        ('logout', 'Çıxış'),
        ('export', 'İxrac'),
        ('import', 'İdxal'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100, verbose_name=_('Model'))
    object_id = models.CharField(max_length=50, blank=True)
    changes = models.JSONField(default=dict, verbose_name=_('Dəyişikliklər'))
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Audit Qeydi')
        verbose_name_plural = _('Audit Qeydləri')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['action', 'model_name']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"
