import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

def send_notification_to_user(user_id, title, message, notification_type='info'):
    """
    Send a real-time notification to a specific user
    """
    channel_layer = get_channel_layer()
    
    # Create notification in database
    notification = Notification.objects.create(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type
    )
    
    # Prepare message data
    notification_data = {
        'id': notification.id,
        'title': title,
        'message': message,
        'type': notification_type,
        'timestamp': notification.created_at.isoformat(),
        'is_read': notification.is_read
    }
    
    # Send to user's notification group
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user_id}",
        {
            'type': 'notification_message',
            'message': notification_data
        }
    )

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