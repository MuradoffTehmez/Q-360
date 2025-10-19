"""Notification service utilities."""
from typing import Optional

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import (
    Notification,
    EmailNotification,
    SMSNotification,
    PushNotification,
    PushDevice,
    NotificationPreference,
)
from .tasks import (
    deliver_email_notification,
    deliver_sms_notification,
    deliver_push_notification,
)

User = get_user_model()


def _should_send_channel(user: User, method: str, category: str, priority: str = 'normal') -> bool:
    """Return True if user allows this notification channel for provided category."""
    if user is None:
        return True

    NotificationPreference.ensure_defaults(user)
    try:
        preference = NotificationPreference.objects.get(user=user, method=method, category=category)
    except NotificationPreference.DoesNotExist:
        return True

    if not preference.enabled:
        return False

    if preference.within_quiet_hours() and priority not in ('high', 'urgent'):
        return False

    return True


def queue_email_notification(
    recipient: User,
    subject: str,
    body: str,
    *,
    template=None,
    notification: Optional[Notification] = None,
    scheduled_for: Optional[timezone.datetime] = None,
    priority: str = 'normal',
    category: str = 'announcement',
    
) -> Optional[EmailNotification]:
    """Create an email notification record and dispatch it asynchronously."""
    email = getattr(recipient, 'email', None) if isinstance(recipient, User) else recipient
    user = recipient if isinstance(recipient, User) else None

    if not email:
        return None

    if user and not _should_send_channel(user, 'email', category, priority):
        return None

    record = EmailNotification.objects.create(
        notification=notification,
        template=template,
        recipient=user,
        recipient_email=email,
        subject=subject,
        body=body,
        priority=priority,
        provider=settings.EMAIL_BACKEND,
        scheduled_for=scheduled_for,
        
    )
    deliver_email_notification.delay(record.id)
    return record


def queue_sms_notification(
    recipient: User,
    message: str,
    *,
    provider=None,
    notification: Optional[Notification] = None,
    scheduled_for: Optional[timezone.datetime] = None,
    priority: str = 'normal',
    category: str = 'announcement',
    
) -> Optional[SMSNotification]:
    """Create an SMS notification record and dispatch it asynchronously."""
    user = recipient if isinstance(recipient, User) else None
    phone = getattr(recipient, 'profile', None).work_phone if user and hasattr(recipient, 'profile') else None
    if user is None:
        phone = recipient

    phone = phone or getattr(user, 'phone_number', None)
    if not phone:
        return None

    if user and not _should_send_channel(user, 'sms', category, priority):
        return None

    record = SMSNotification.objects.create(
        notification=notification,
        recipient=user,
        recipient_phone=phone,
        message=message,
        provider=provider,
        scheduled_for=scheduled_for,
        
    )
    deliver_sms_notification.delay(record.id)
    return record


def register_push_device(user: User, device_token: str, platform: str, name: str = '', metadata: Optional[dict] = None) -> PushDevice:
    """Register or update a push device for the given user."""
    defaults = {
        'user': user,
        'name': name,
        'platform': platform,
        'metadata': metadata or {},
        'is_active': True,
        'last_seen_at': timezone.now(),
    }
    device, _ = PushDevice.objects.update_or_create(device_token=device_token, defaults=defaults)
    return device


def queue_push_notification(
    user: User,
    title: str,
    message: str,
    *,
    data: Optional[dict] = None,
    priority: str = 'normal',
    category: str = 'announcement',
    device: Optional[PushDevice] = None,
    scheduled_for: Optional[timezone.datetime] = None,
    
) -> Optional[PushNotification]:
    """Create and dispatch a push notification for the user."""
    if not _should_send_channel(user, 'push', category, priority):
        return None

    record = PushNotification.objects.create(
        user=user,
        device=device,
        title=title,
        message=message,
        data=data or {},
        priority=priority,
        scheduled_for=scheduled_for,
        
    )
    deliver_push_notification.delay(record.id)
    return record


def send_notification_to_user(user_id, title, message, notification_type='info', link='', create_in_db=True):
    """Send a real-time in-app notification to a specific user."""
    if create_in_db:
        notification = Notification.objects.create(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link,
        )
        notification_id = notification.id
        timestamp = notification.created_at.isoformat()
        is_read = notification.is_read
    else:
        now = timezone.now()
        notification_id = None
        timestamp = now.isoformat()
        is_read = False

    try:
        channel_layer = get_channel_layer()
        if channel_layer is None:
            return

        notification_data = {
            'id': notification_id,
            'title': title,
            'message': message,
            'type': notification_type,
            'timestamp': timestamp,
            'is_read': is_read,
            'link': link,
        }

        async_to_sync(channel_layer.group_send)(
            f'notifications_{user_id}',
            {'type': 'notification_message', 'message': notification_data},
        )
    except Exception as exc:  # pragma: no cover - depends on channel backend
        import logging

        logger = logging.getLogger(__name__)
        logger.warning('Failed to send WebSocket notification to user %s: %s', user_id, exc)


def broadcast_notification(title, message, notification_type='info', exclude_user_ids=None):
    """Broadcast notification to all active users (optionally excluding some)."""
    from django.db.models import Q

    query = Q(is_active=True)
    if exclude_user_ids:
        query &= ~Q(id__in=exclude_user_ids)

    active_users = User.objects.filter(query).values_list('id', flat=True)
    for user_id in active_users:
        send_notification_to_user(user_id, title, message, notification_type)


def broadcast_notification_smart(title, message, notification_type='info', priority='normal', exclude_user_ids=None):
    """Broadcast notification using smart routing utilities."""
    from django.db.models import Q
    from .utils import send_notification_by_smart_routing

    query = Q(is_active=True)
    if exclude_user_ids:
        query &= ~Q(id__in=exclude_user_ids)

    for user in User.objects.filter(query):
        send_notification_by_smart_routing(
            recipient=user,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
        )
