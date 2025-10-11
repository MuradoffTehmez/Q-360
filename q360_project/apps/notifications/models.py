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
    
    def save(self, *args, **kwargs):
        # Call the original save method
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # If this is a new notification, send it via WebSocket
        if is_new:
            self.send_real_time_notification()
    
    def send_real_time_notification(self):
        """Send this notification via WebSocket to the user"""
        from .services import send_notification_to_user
        
        send_notification_to_user(
            user_id=self.user.id,
            title=self.title,
            message=self.message,
            notification_type=self.notification_type
        )
    
    def mark_as_read(self):
        """Mark notification as read and update read_at timestamp"""
        self.is_read = True
        self.read_at = self._current_timestamp()
        self.save(update_fields=['is_read', 'read_at'])
        
        return self
    
    def _current_timestamp(self):
        """Get current timestamp (helper method)"""
        from django.utils import timezone
        return timezone.now()


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

    def get_statistics(self):
        """Get email statistics for this template."""
        logs = self.email_logs.all()
        total_sent = logs.count()
        total_opened = logs.filter(opened_at__isnull=False).count()
        total_clicked = logs.filter(clicked_at__isnull=False).count()
        total_failed = logs.filter(status='failed').count()

        return {
            'total_sent': total_sent,
            'total_opened': total_opened,
            'total_clicked': total_clicked,
            'total_failed': total_failed,
            'open_rate': round((total_opened / total_sent * 100), 2) if total_sent > 0 else 0,
            'click_rate': round((total_clicked / total_sent * 100), 2) if total_sent > 0 else 0,
            'failure_rate': round((total_failed / total_sent * 100), 2) if total_sent > 0 else 0,
        }


class EmailLog(models.Model):
    """Log for tracking sent emails."""

    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('sent', 'Göndərildi'),
        ('failed', 'Uğursuz'),
    ]

    template = models.ForeignKey(
        EmailTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_logs',
        verbose_name=_('Şablon')
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_emails',
        verbose_name=_('Alıcı')
    )
    recipient_email = models.EmailField(verbose_name=_('E-poçt'))
    subject = models.CharField(max_length=200, verbose_name=_('Mövzu'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, verbose_name=_('Xəta Mesajı'))

    # Tracking fields
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('E-poçt Loqu')
        verbose_name_plural = _('E-poçt Loqları')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient_email} - {self.subject}"
