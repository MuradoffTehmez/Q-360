"""Models for audit app."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
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

    THREAT_LEVELS = [
        ('none', 'Təhlükə yoxdur'),
        ('low', 'Aşağı'),
        ('medium', 'Orta'),
        ('high', 'Yüksək'),
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
    threat_level = models.CharField(max_length=10, choices=THREAT_LEVELS, default='none', verbose_name=_('Təhlükə Səviyyəsi'))
    threat_score = models.IntegerField(default=0, verbose_name=_('Təhlükə Skoru'))
    actor_role = models.CharField(max_length=30, blank=True, verbose_name=_('İstifadəçi Rolu'))
    context = models.JSONField(default=dict, blank=True, verbose_name=_('Kontekst'))
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Full-text search field
    search_vector = SearchVectorField(null=True, editable=False)

    class Meta:
        verbose_name = _('Audit Qeydi')
        verbose_name_plural = _('Audit Qeydləri')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['action', 'model_name']),
            models.Index(fields=['severity', 'created_at']),
            GinIndex(fields=['search_vector'], name='audit_search_idx'),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"

    @classmethod
    def calculate_threat_level(cls, user, action, ip_address=None, time_window_minutes=60):
        """
        Təhlükə səviyyəsini hesablayır.

        Args:
            user: İstifadəçi obyekti
            action: Edilən əməliyyat
            ip_address: IP ünvanı
            time_window_minutes: Zaman pəncərəsi (dəqiqə)

        Returns:
            tuple: (threat_level, threat_score)
        """
        from django.utils import timezone
        from datetime import timedelta

        threat_score = 0
        start_time = timezone.now() - timedelta(minutes=time_window_minutes)

        # Son zaman ərzindəki uğursuz giriş cəhdləri
        failed_logins = cls.objects.filter(
            user=user,
            action='login_failure',
            created_at__gte=start_time
        ).count()

        # IP əsaslı təhdid analizi
        if ip_address:
            ip_failed_attempts = cls.objects.filter(
                ip_address=ip_address,
                action='login_failure',
                created_at__gte=start_time
            ).count()
            threat_score += min(ip_failed_attempts * 15, 50)

        # İstifadəçi əsaslı təhdid analizi
        threat_score += min(failed_logins * 10, 40)

        # İcazə rədd edilmələr
        permission_denials = cls.objects.filter(
            user=user,
            action='permission_denied',
            created_at__gte=start_time
        ).count()
        threat_score += min(permission_denials * 8, 30)

        # Kritik əməliyyatlar
        critical_actions = cls.objects.filter(
            user=user,
            severity='critical',
            created_at__gte=start_time
        ).count()
        threat_score += min(critical_actions * 20, 60)

        # Threat level təyini
        if threat_score >= 80:
            threat_level = 'critical'
        elif threat_score >= 60:
            threat_level = 'high'
        elif threat_score >= 40:
            threat_level = 'medium'
        elif threat_score >= 20:
            threat_level = 'low'
        else:
            threat_level = 'none'

        return threat_level, threat_score

    def save(self, *args, **kwargs):
        """Threat level avtomatik hesablanması."""
        if not self.threat_level or self.threat_level == 'none':
            if self.user:
                threat_level, threat_score = self.calculate_threat_level(
                    user=self.user,
                    action=self.action,
                    ip_address=self.ip_address
                )
                self.threat_level = threat_level
                self.threat_score = threat_score
        super().save(*args, **kwargs)
