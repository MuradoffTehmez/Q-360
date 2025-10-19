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
        ('login_failure', 'Uğursuz Giriş'),
        ('export', 'İxrac'),
        ('import', 'İdxal'),
        ('view', 'Baxış'),
        ('permission_denied', 'İcazə Rədd Edildi'),
    ]

    SEVERITY_CHOICES = [
        ('info', 'Məlumat'),
        ('warning', 'Xəbərdarlıq'),
        ('critical', 'Kritik'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100, verbose_name=_('Model'))
    object_id = models.CharField(max_length=50, blank=True)
    changes = models.JSONField(default=dict, verbose_name=_('Dəyişikliklər'))
    request_path = models.CharField(max_length=255, blank=True, verbose_name=_('Sorğu Yolu'))
    http_method = models.CharField(max_length=10, blank=True, verbose_name=_('HTTP metodu'))
    status_code = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Status Kodu'))
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='info', verbose_name=_('Şiddət'))
    actor_role = models.CharField(max_length=30, blank=True, verbose_name=_('İstifadəçi Rolu'))
    context = models.JSONField(default=dict, blank=True, verbose_name=_('Kontekst'))
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
            models.Index(fields=['severity', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"
