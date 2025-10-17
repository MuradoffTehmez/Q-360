"""Enhanced models for notifications app with SMS and Push notification capabilities."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.departments.models import Department, Organization
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class NotificationMethod(models.Model):
    """
    Notification method configuration (Email, SMS, Push)
    """
    METHOD_CHOICES = [
        ('email', 'E-poçt'),
        ('sms', 'SMS'),
        ('push', 'Push Bildirişi'),
        ('in_app', 'Tətbiqdaxili'),
    ]

    name = models.CharField(max_length=50, unique=True, verbose_name=_('Ad'))
    method_type = models.CharField(max_length=20, choices=METHOD_CHOICES, verbose_name=_('Metod Növü'))
    is_active = models.BooleanField(default=True, verbose_name=_('Aktivdir'))
    configuration = models.JSONField(default=dict, blank=True, verbose_name=_('Konfiqurasiya'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Bildiriş Metodu')
        verbose_name_plural = _('Bildiriş Metodları')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.method_type})"


class NotificationTemplate(models.Model):
    """
    Enhanced notification template with methods and triggers
    """
    TRIGGER_CHOICES = [
        ('campaign_start', 'Qiymətləndirmə Kampaniyası Başlayır'),
        ('campaign_end', 'Qiymətləndirmə Kampaniyası Bitir'),
        ('evaluation_assigned', 'Qiymətləndirmə Tapşırılır'),
        ('evaluation_completed', 'Qiymətləndirmə Tamamlanır'),
        ('report_ready', 'Hesabat Hazırdır'),
        ('deadline_reminder', 'Bitmə Vaxtına Xatırlatma'),
        ('new_training', 'Yeni Təlim Təyin Edilir'),
        ('training_complete', 'Təlim Tamamlanır'),
        ('salary_change', 'Maaş Dəyişikliyi'),
        ('performance_result', 'Performans Nəticələri'),
        ('system_maintenance', 'Sistem Texniki Xidmət'),
        ('password_change', 'Şifrə Dəyişikliyi'),
        ('account_lock', 'Hesab Bloklanır'),
        ('security_alert', 'Təhlükəsizlik Xəbərdarlığı'),
        ('general_announcement', 'Ümumi Elan'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name=_('Şablon Adı'))
    trigger = models.CharField(max_length=50, choices=TRIGGER_CHOICES, verbose_name=_('Tətik'))
    subject = models.CharField(max_length=200, verbose_name=_('Mövzu'))
    email_content = models.TextField(verbose_name=_('E-poçt Məzmunu'))
    sms_content = models.CharField(max_length=160, verbose_name=_('SMS Məzmunu'))
    push_content = models.CharField(max_length=200, verbose_name=_('Push Məzmunu'))
    inapp_content = models.TextField(verbose_name=_('Tətbiqdaxili Məzmun'))
    methods = models.ManyToManyField(NotificationMethod, blank=True, verbose_name=_('Bildiriş Metodları'))
    is_active = models.BooleanField(default=True, verbose_name=_('Aktivdir'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Bildiriş Şablonu')
        verbose_name_plural = _('Bildiriş Şablonları')
        ordering = ['name']

    def __str__(self):
        return self.name


class Notification(models.Model):
    """Enhanced notification model with multiple channels and scheduling."""
    
    NOTIFICATION_TYPES = [
        ('info', 'Məlumat'),
        ('warning', 'Xəbərdarlıq'),
        ('success', 'Uğur'),
        ('error', 'Xəta'),
        ('assignment', 'Tapşırıq'),
        ('reminder', 'Xatırlatma'),
        ('security', 'Təhlükəsizlik'),
        ('announcement', 'Elan'),
    ]

    # Notification channels
    CHANNEL_CHOICES = [
        ('email', 'E-poçt'),
        ('sms', 'SMS'),
        ('push', 'Push'),
        ('in_app', 'Tətbiqdaxili'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
    message = models.TextField(verbose_name=_('Mesaj'))
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='in_app', verbose_name=_('Kanal'))
    is_read = models.BooleanField(default=False, verbose_name=_('Oxundu'))
    link = models.CharField(max_length=500, blank=True, verbose_name=_('Keçid'))
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Reference to related object (for generic relations)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional metadata
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Aşağı'),
        ('normal', 'Normal'),
        ('high', 'Yüksək'),
        ('urgent', 'Təcili'),
    ], default='normal', verbose_name=_('Prioritet'))
    
    scheduled_time = models.DateTimeField(null=True, blank=True, verbose_name=_('Planlaşdırılmış Vaxt'))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Göndərilmə Vaxtı'))

    class Meta:
        verbose_name = _('Bildiriş')
        verbose_name_plural = _('Bildirişlər')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Call the original save method
        is_new = self.pk is None
        skip_websocket = kwargs.pop('skip_websocket', False)
        super().save(*args, **kwargs)

        # If this is a new notification and it's not scheduled, send it via WebSocket
        if is_new and not skip_websocket and self.scheduled_time is None:
            self.send_real_time_notification()

    def send_real_time_notification(self):
        """Send this notification via WebSocket to the user (without creating a new notification)"""
        try:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync

            channel_layer = get_channel_layer()

            # If channel layer is not configured, skip WebSocket notification
            if channel_layer is None:
                return

            # Prepare message data
            notification_data = {
                'id': self.id,
                'title': self.title,
                'message': self.message,
                'type': self.notification_type,
                'timestamp': self.created_at.isoformat(),
                'is_read': self.is_read,
                'link': self.link
            }

            # Send to user's notification group
            async_to_sync(channel_layer.group_send)(
                f"notifications_{self.user.id}",
                {
                    'type': 'notification_message',
                    'message': notification_data
                }
            )
        except Exception as e:
            # Log error but don't fail the notification creation
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to send real-time notification: {e}")
    
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

    @property
    def is_scheduled(self):
        """Check if notification is scheduled for later"""
        return self.scheduled_time is not None and self.scheduled_time > self._current_timestamp()


class SMSProvider(models.Model):
    """
    SMS provider configuration (Twilio, AWS SNS, etc.)
    """
    PROVIDER_CHOICES = [
        ('twilio', 'Twilio'),
        ('aws_sns', 'AWS SNS'),
        ('clickatell', 'Clickatell'),
        ('custom', 'Fərdi'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name=_('Ad'))
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, verbose_name=_('Təchizatçı'))
    is_active = models.BooleanField(default=True, verbose_name=_('Aktivdir'))
    configuration = models.JSONField(default=dict, verbose_name=_('Konfiqurasiya'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('SMS Təchizatçısı')
        verbose_name_plural = _('SMS Təchizatçıları')
        ordering = ['name']

    def __str__(self):
        return self.name


class SMSLog(models.Model):
    """
    SMS sending logs
    """
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('sent', 'Göndərildi'),
        ('failed', 'Uğursuz'),
        ('delivered', 'Çatdırıldı'),
        ('undelivered', 'Çatdırılmadı'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Alıcı'))
    recipient_phone = models.CharField(max_length=20, verbose_name=_('Telefon Nömrəsi'))
    message = models.TextField(verbose_name=_('Mesaj'))
    provider = models.ForeignKey(SMSProvider, on_delete=models.SET_NULL, null=True, verbose_name=_('Təchizatçı'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    external_id = models.CharField(max_length=100, blank=True, verbose_name=_('Xarici ID'))
    error_message = models.TextField(blank=True, verbose_name=_('Xəta Mesajı'))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Göndərilmə Vaxtı'))
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Çatdırılma Vaxtı'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('SMS Loqu')
        verbose_name_plural = _('SMS Loqları')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient_phone} - {self.status}"


class PushNotification(models.Model):
    """
    Push notification model for mobile/web push
    """
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('sent', 'Göndərildi'),
        ('failed', 'Uğursuz'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('İstifadəçi'))
    title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
    message = models.TextField(verbose_name=_('Mesaj'))
    data = models.JSONField(default=dict, blank=True, verbose_name=_('Əlavə Məlumat'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    error_message = models.TextField(blank=True, verbose_name=_('Xəta Mesajı'))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Göndərilmə Vaxtı'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Push Bildirişi')
        verbose_name_plural = _('Push Bildirişləri')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class UserNotificationPreference(models.Model):
    """
    User-specific notification preferences
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('İstifadəçi'))
    
    # Email preferences
    email_notifications = models.BooleanField(default=True, verbose_name=_('E-poçt Bildirişləri'))
    email_assignment = models.BooleanField(default=True, verbose_name=_('Tapşırıq Bildirişləri'))
    email_reminder = models.BooleanField(default=True, verbose_name=_('Xatırlatma Bildirişləri'))
    email_announcement = models.BooleanField(default=True, verbose_name=_('Elan Bildirişləri'))
    email_security = models.BooleanField(default=True, verbose_name=_('Təhlükəsizlik Bildirişləri'))
    
    # SMS preferences
    sms_notifications = models.BooleanField(default=False, verbose_name=_('SMS Bildirişləri'))
    sms_important_only = models.BooleanField(default=True, verbose_name=_('Yalnız Vacib Bildirişlər'))
    sms_assignment = models.BooleanField(default=False, verbose_name=_('Tapşırıq Bildirişləri'))
    sms_reminder = models.BooleanField(default=False, verbose_name=_('Xatırlatma Bildirişləri'))
    sms_security = models.BooleanField(default=True, verbose_name=_('Təhlükəsizlik Bildirişləri'))
    
    # Push notification preferences
    push_notifications = models.BooleanField(default=True, verbose_name=_('Push Bildirişləri'))
    push_assignment = models.BooleanField(default=True, verbose_name=_('Tapşırıq Bildirişləri'))
    push_reminder = models.BooleanField(default=True, verbose_name=_('Xatırlatma Bildirişləri'))
    push_announcement = models.BooleanField(default=True, verbose_name=_('Elan Bildirişləri'))
    
    # Do not disturb settings
    dnd_start_time = models.TimeField(null=True, blank=True, verbose_name=_('Sakitlik Rejimi - Başlama'))
    dnd_end_time = models.TimeField(null=True, blank=True, verbose_name=_('Sakitlik Rejimi - Bitmə'))
    
    # Notification schedule
    weekend_notifications = models.BooleanField(default=True, verbose_name=_('Həftə Sonu Bildirişləri'))
    weekday_start = models.TimeField(default='08:00', verbose_name=_('İş Günü Başlama'))
    weekday_end = models.TimeField(default='18:00', verbose_name=_('İş Günü Bitmə'))

    class Meta:
        verbose_name = _('İstifadəçi Bildiriş Tənzimləmələri')
        verbose_name_plural = _('İstifadəçi Bildiriş Tənzimləmələri')

    def __str__(self):
        return f"{self.user.username} - Bildiriş Tənzimləmələri"

    def save(self, *args, **kwargs):
        # Create if not exists
        if not self.pk:
            super().save(*args, **kwargs)
            # Link with user's profile if exists
            try:
                from apps.accounts.models import Profile
                profile, created = Profile.objects.get_or_create(user=self.user)
                if created:
                    profile.email_notifications = self.email_notifications
                    profile.sms_notifications = self.sms_notifications
                    profile.save()
            except:
                # Profile might not exist, continue without error
                pass
        else:
            super().save(*args, **kwargs)


class BulkNotification(models.Model):
    """
    Bulk notification for multiple recipients
    """
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('in_progress', 'Davam Edir'),
        ('completed', 'Tamamlandı'),
        ('failed', 'Uğursuz'),
    ]

    title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
    message = models.TextField(verbose_name=_('Mesaj'))
    recipients_count = models.IntegerField(verbose_name=_('Alıcı Sayı'))
    filter_criteria = models.JSONField(default=dict, verbose_name=_('Filtrləmə Kriteriyaları'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    initiated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('Başlatan'))
    channels = models.JSONField(default=list, verbose_name=_('Kanallar'))
    sent_count = models.IntegerField(default=0, verbose_name=_('Göndərilənlər Sayı'))
    failed_count = models.IntegerField(default=0, verbose_name=_('Uğursuzlar Sayı'))
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Kütləvi Bildiriş')
        verbose_name_plural = _('Kütləvi Bildirişlər')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.status}"


class EmailTemplate(models.Model):
    """Updated email templates for various notifications."""

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
    """Updated log for tracking sent emails."""

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