"""Models for notifications app."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class Notification(models.Model):
    """System notifications for users."""

    NOTIFICATION_TYPES = [
        ('info', 'Məlumat'),
        ('warning', 'Xəbərdarlıq'),
        ('success', 'Uğur'),
        ('error', 'Xəta'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
    message = models.TextField(verbose_name=_('Mesaj'))
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    is_read = models.BooleanField(default=False, verbose_name=_('Oxundu'))
    link = models.CharField(max_length=500, blank=True, verbose_name=_('Keçid'))
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Bildiriş')
        verbose_name_plural = _('Bildirişlər')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class EmailTemplate(models.Model):
    """Email templates for various notifications."""

    name = models.CharField(max_length=100, unique=True, verbose_name=_('Şablon Adı'))
    subject = models.CharField(max_length=200, verbose_name=_('Mövzu'))
    html_content = models.TextField(verbose_name=_('HTML Məzmun'))
    text_content = models.TextField(blank=True, verbose_name=_('Mətn Məzmunu'))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('E-poçt Şablonu')
        verbose_name_plural = _('E-poçt Şablonları')

    def __str__(self):
        return self.name
