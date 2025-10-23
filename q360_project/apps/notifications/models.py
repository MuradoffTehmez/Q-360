"""Enhanced models for notifications app with SMS and Push notification capabilities."""
from datetime import timedelta

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
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
        ('azercell', 'Azercell'),
        ('bakcell', 'Bakcell'),
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


class SMSNotification(models.Model):
    """Discrete SMS delivery record managed via Celery."""

    STATUS_CHOICES = [
        ('queued', 'Növbədə'),
        ('sending', 'Göndərilir'),
        ('sent', 'Göndərildi'),
        ('failed', 'Uğursuz'),
    ]

    notification = models.ForeignKey(
        Notification,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sms_deliveries',
        verbose_name=_('Bildiriş'),
    )
    provider = models.ForeignKey(
        SMSProvider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sms_deliveries',
        verbose_name=_('SMS Təchizatçısı'),
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sms_notification_entries',
        verbose_name=_('İstifadəçi'),
    )
    recipient_phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?\d{7,15}$', _('Telefon nömrəsi +994xxxxxxxxx formatında olmalıdır'))],
        verbose_name=_('Telefon Nömrəsi'),
    )
    message = models.TextField(verbose_name=_('Mesaj'))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='queued',
        verbose_name=_('Status'),
    )
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_('Metadata'))
    scheduled_for = models.DateTimeField(null=True, blank=True, verbose_name=_('Planlaşdırılan Vaxt'))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Göndərilmə Vaxtı'))
    error_message = models.TextField(blank=True, verbose_name=_('Xəta Mesajı'))
    task_id = models.CharField(max_length=128, blank=True, verbose_name=_('Celery Tapşırıq ID-i'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('SMS Bildirişi')
        verbose_name_plural = _('SMS Bildirişləri')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['recipient_phone']),
        ]

    def __str__(self):
        return f"{self.recipient_phone} • {self.message[:40]}"

    @property
    def is_due(self):
        return self.scheduled_for is None or self.scheduled_for <= timezone.now()

    def mark_sending(self, task_id=None):
        self.status = 'sending'
        if task_id:
            self.task_id = task_id
        self.save(update_fields=['status', 'task_id', 'updated_at'])

    def mark_sent(self):
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.error_message = ''
        self.save(update_fields=['status', 'sent_at', 'error_message', 'updated_at'])

    def mark_failed(self, error_message):
        self.status = 'failed'
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message', 'updated_at'])


class PushDevice(models.Model):
    """Registered device for push notifications."""

    PLATFORM_CHOICES = [
        ('ios', 'iOS'),
        ('android', 'Android'),
        ('web', 'Veb'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_devices', verbose_name=_('İstifadəçi'))
    name = models.CharField(max_length=100, blank=True, verbose_name=_('Cihaz Adı'))
    device_token = models.CharField(max_length=255, unique=True, verbose_name=_('Cihaz Tokeni'))
    device_id = models.CharField(max_length=255, blank=True, verbose_name=_('Cihaz ID'))
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name=_('Platforma'))
    is_active = models.BooleanField(default=True, verbose_name=_('Aktivdir'))
    last_seen_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Son Aktivlik'))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_('Metadata'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Push Cihazı')
        verbose_name_plural = _('Push Cihazları')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} • {self.platform}"

    def mark_seen(self):
        self.last_seen_at = timezone.now()
        self.save(update_fields=['last_seen_at', 'updated_at'])


class PushNotification(models.Model):
    """
    Push notification model for mobile/web push
    """
    STATUS_CHOICES = [
        ('queued', 'Növbədə'),
        ('sending', 'Göndərilir'),
        ('sent', 'Göndərildi'),
        ('failed', 'Uğursuz'),
    ]

    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('high', 'Yüksək'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('İstifadəçi'))
    device = models.ForeignKey(
        PushDevice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='push_notifications',
        verbose_name=_('Cihaz'),
    )
    title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
    message = models.TextField(verbose_name=_('Mesaj'))
    data = models.JSONField(default=dict, blank=True, verbose_name=_('Əlavə Məlumat'))
    provider = models.CharField(max_length=100, blank=True, verbose_name=_('Təchizatçı'))
    topic = models.CharField(max_length=100, blank=True, verbose_name=_('Mövzu/Topic'))
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal', verbose_name=_('Prioritet'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued', verbose_name=_('Status'))
    error_message = models.TextField(blank=True, verbose_name=_('Xəta Mesajı'))
    task_id = models.CharField(max_length=128, blank=True, verbose_name=_('Celery Tapşırıq ID-i'))
    scheduled_for = models.DateTimeField(null=True, blank=True, verbose_name=_('Planlaşdırılan Vaxt'))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Göndərilmə Vaxtı'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Push Bildirişi')
        verbose_name_plural = _('Push Bildirişləri')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    @property
    def is_due(self):
        return self.scheduled_for is None or self.scheduled_for <= timezone.now()

    def mark_sending(self, task_id=None):
        self.status = 'sending'
        if task_id:
            self.task_id = task_id
        self.save(update_fields=['status', 'task_id', 'updated_at'])

    def mark_sent(self):
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.error_message = ''
        self.save(update_fields=['status', 'sent_at', 'error_message', 'updated_at'])

    def mark_failed(self, error_message):
        self.status = 'failed'
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message', 'updated_at'])



class NotificationPreference(models.Model):
    """Fine grained notification preference per channel and category."""

    METHOD_CHOICES = NotificationMethod.METHOD_CHOICES
    CATEGORY_CHOICES = [
        ('assignment', _('Tapşırıq')),
        ('reminder', _('Xatırlatma')),
        ('announcement', _('Elan')),
        ('security', _('Təhlükəsizlik')),
        ('report', _('Hesabat')),
        ('system', _('Sistem')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channel_preferences', verbose_name=_('İstifadəçi'))
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, verbose_name=_('Metod'))
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, verbose_name=_('Kateqoriya'))
    enabled = models.BooleanField(default=True, verbose_name=_('Aktivdir'))
    quiet_hours_start = models.TimeField(null=True, blank=True, verbose_name=_('Sakitlik Başlama'))
    quiet_hours_end = models.TimeField(null=True, blank=True, verbose_name=_('Sakitlik Bitmə'))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_('Metadata'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Bildiriş Parametri')
        verbose_name_plural = _('Bildiriş Parametrləri')
        unique_together = ('user', 'method', 'category')
        ordering = ['user', 'method', 'category']
        indexes = [
            models.Index(fields=['user', 'method']),
            models.Index(fields=['method', 'category']),
        ]

    def __str__(self):
        return f"{self.user.username} • {self.get_method_display()} • {self.get_category_display()}"

    @classmethod
    def ensure_defaults(cls, user):
        """Ensure preference rows exist for every method/category combination."""
        methods = [choice[0] for choice in cls.METHOD_CHOICES]
        categories = [choice[0] for choice in cls.CATEGORY_CHOICES]
        existing = cls.objects.filter(user=user).values_list('method', 'category')
        existing_set = {(m, c) for m, c in existing}
        bulk = []
        for method in methods:
            for category in categories:
                if (method, category) not in existing_set:
                    bulk.append(
                        cls(user=user, method=method, category=category, enabled=True)
                    )
        if bulk:
            cls.objects.bulk_create(bulk)

    @classmethod
    def sync_from_legacy(cls, user_pref):
        """Sync legacy boolean preferences into channel records."""
        cls.ensure_defaults(user_pref.user)
        mapping = [
            ('email', 'assignment', user_pref.email_notifications and user_pref.email_assignment),
            ('email', 'reminder', user_pref.email_notifications and user_pref.email_reminder),
            ('email', 'announcement', user_pref.email_notifications and user_pref.email_announcement),
            ('email', 'security', user_pref.email_notifications and user_pref.email_security),
            ('sms', 'assignment', user_pref.sms_notifications and user_pref.sms_assignment),
            ('sms', 'reminder', user_pref.sms_notifications and user_pref.sms_reminder),
            ('sms', 'security', user_pref.sms_notifications and user_pref.sms_security),
            ('sms', 'announcement', user_pref.sms_notifications and not user_pref.sms_important_only),
            ('push', 'assignment', user_pref.push_notifications and user_pref.push_assignment),
            ('push', 'reminder', user_pref.push_notifications and user_pref.push_reminder),
            ('push', 'announcement', user_pref.push_notifications and user_pref.push_announcement),
        ]
        for method, category, enabled in mapping:
            cls.objects.filter(user=user_pref.user, method=method, category=category).update(enabled=enabled)

    def within_quiet_hours(self, check_time=None):
        """Check if a given time is within configured quiet hours."""
        if not self.quiet_hours_start or not self.quiet_hours_end:
            return False
        check_time = check_time or timezone.localtime().time()
        if self.quiet_hours_start <= self.quiet_hours_end:
            return self.quiet_hours_start <= check_time <= self.quiet_hours_end
        # Overnight quiet hours
        return check_time >= self.quiet_hours_start or check_time <= self.quiet_hours_end


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
        creating = self.pk is None
        super().save(*args, **kwargs)

        if creating:
            try:
                from apps.accounts.models import Profile
                profile, created = Profile.objects.get_or_create(user=self.user)
                if created:
                    profile.email_notifications = self.email_notifications
                    profile.sms_notifications = self.sms_notifications
                    profile.save()
            except Exception:
                # Profile might not exist, continue without error
                pass

        try:
            NotificationPreference.ensure_defaults(self.user)
            NotificationPreference.sync_from_legacy(self)
        except Exception:
            # Preference sync failures should not block save
            pass


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


class EmailNotification(models.Model):
    """Discrete email delivery instance."""

    STATUS_CHOICES = [
        ('queued', 'Növbədə'),
        ('sending', 'Göndərilir'),
        ('sent', 'Göndərildi'),
        ('failed', 'Uğursuz'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Aşağı'),
        ('normal', 'Normal'),
        ('high', 'Yüksək'),
    ]

    notification = models.ForeignKey(
        Notification,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_notifications',
        verbose_name=_('Bildiriş'),
    )
    template = models.ForeignKey(
        EmailTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_notifications',
        verbose_name=_('Şablon'),
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_notification_records',
        verbose_name=_('İstifadəçi'),
    )
    recipient_email = models.EmailField(verbose_name=_('E-poçt'))
    subject = models.CharField(max_length=255, verbose_name=_('Mövzu'))
    body = models.TextField(verbose_name=_('Məzmun'))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='queued',
        verbose_name=_('Status'),
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='normal',
        verbose_name=_('Prioritet'),
    )
    provider = models.CharField(max_length=100, blank=True, verbose_name=_('Təchizatçı'))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_('Metadata'))
    scheduled_for = models.DateTimeField(null=True, blank=True, verbose_name=_('Planlaşdırılan Vaxt'))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Göndərilmə Vaxtı'))
    error_message = models.TextField(blank=True, verbose_name=_('Xəta Mesajı'))
    task_id = models.CharField(max_length=128, blank=True, verbose_name=_('Celery Tapşırıq ID-i'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('E-poçt Bildirişi')
        verbose_name_plural = _('E-poçt Bildirişləri')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['scheduled_for']),
            models.Index(fields=['recipient_email']),
        ]

    def __str__(self):
        return f"{self.recipient_email} • {self.subject}"

    @property
    def is_due(self):
        return self.scheduled_for is None or self.scheduled_for <= timezone.now()

    def mark_sending(self, task_id=None):
        self.status = 'sending'
        if task_id:
            self.task_id = task_id
        self.save(update_fields=['status', 'task_id', 'updated_at'])

    def mark_sent(self):
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.error_message = ''
        self.save(update_fields=['status', 'sent_at', 'error_message', 'updated_at'])

    def mark_failed(self, error_message):
        self.status = 'failed'
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message', 'updated_at'])
