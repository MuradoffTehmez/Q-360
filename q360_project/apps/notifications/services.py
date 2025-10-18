import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

def send_notification_to_user(user_id, title, message, notification_type='info', link='', create_in_db=True):
    """
    Send a real-time notification to a specific user

    Args:
        user_id: ID of the user to send notification to
        title: Notification title
        message: Notification message
        notification_type: Type of notification (info, warning, success, error)
        link: Optional link for the notification
        create_in_db: If True, create notification in database. If False, only send via WebSocket
    """
    # Create notification in database if requested
    if create_in_db:
        notification = Notification.objects.create(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link
        )
        notification_id = notification.id
        timestamp = notification.created_at.isoformat()
        is_read = notification.is_read
    else:
        # Just send via WebSocket without DB entry
        from django.utils import timezone
        notification_id = None
        timestamp = timezone.now().isoformat()
        is_read = False

    # Try to send via WebSocket (if configured)
    try:
        channel_layer = get_channel_layer()

        # If channel layer is not configured, skip WebSocket
        if channel_layer is None:
            return

        # Prepare message data
        notification_data = {
            'id': notification_id,
            'title': title,
            'message': message,
            'type': notification_type,
            'timestamp': timestamp,
            'is_read': is_read,
            'link': link
        }

        # Send to user's notification group
        async_to_sync(channel_layer.group_send)(
            f"notifications_{user_id}",
            {
                'type': 'notification_message',
                'message': notification_data
            }
        )
    except Exception as e:
        # Log error but don't fail
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to send WebSocket notification to user {user_id}: {e}")

def broadcast_notification(title, message, notification_type='info', exclude_user_ids=None):
    """
    Broadcast notification to all users (with optional exclusions)
    """
    from django.db.models import Q
    
    query = Q(is_active=True)
    if exclude_user_ids:
        query &= ~Q(id__in=exclude_user_ids)
    
    active_users = User.objects.filter(query).values_list('id', flat=True)
    
    for user_id in active_users:
        send_notification_to_user(user_id, title, message, notification_type)


def broadcast_notification_smart(title, message, notification_type='info', priority='normal', exclude_user_ids=None):
    """
    Smart broadcast notification to all users using intelligent routing.
    
    Args:
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        priority: Priority level
        exclude_user_ids: List of user IDs to exclude
    """
    from django.db.models import Q
    
    query = Q(is_active=True)
    if exclude_user_ids:
        query &= ~Q(id__in=exclude_user_ids)
    
    active_users = User.objects.filter(query)
    
    from .utils import send_notification_by_smart_routing
    for user in active_users:
        send_notification_by_smart_routing(
            recipient=user,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority
        )