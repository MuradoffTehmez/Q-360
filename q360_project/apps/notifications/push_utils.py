"""Push notification utility functions for notifications app."""
import logging
from django.utils import timezone
from .models import PushNotification
from apps.accounts.models import User


logger = logging.getLogger(__name__)


def send_push_notification(user, title, message, data=None, priority='normal'):
    """
    Send a push notification to a user.

    Args:
        user (User): User to send notification to
        title (str): Notification title
        message (str): Notification message
        data (dict): Additional data to include with the notification
        priority (str): Priority level ('normal', 'high')

    Returns:
        bool: True if push notification sent successfully, False otherwise
    """
    from .models import PushNotification
    
    # Create push notification record
    push_notif = PushNotification.objects.create(
        user=user,
        title=title,
        message=message,
        data=data or {},
        status='pending'
    )
    
    try:
        # Send push notification using appropriate service
        # For now, we'll implement a placeholder - in production, this might use
        # services like Firebase Cloud Messaging (FCM), OneSignal, etc.
        success = send_push_via_webpush(user, title, message, data, priority)
        
        if success:
            push_notif.status = 'sent'
            push_notif.sent_at = timezone.now()
        else:
            push_notif.status = 'failed'
            push_notif.error_message = 'Push notification sending failed'
        
        push_notif.save()
        return success
        
    except Exception as e:
        push_notif.status = 'failed'
        push_notif.error_message = str(e)
        push_notif.save()
        logger.error(f"Error sending push notification: {e}")
        return False


def send_push_via_webpush(user, title, message, data=None, priority='normal'):
    """
    Send push notification via Web Push protocol (for browser notifications).

    Args:
        user (User): User to send notification to
        title (str): Notification title
        message (str): Notification message
        data (dict): Additional data
        priority (str): Priority level

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if user has web push subscriptions
        # This would require a model to store user's web push subscription info
        # For now, we'll use a placeholder implementation
        
        # In a real implementation, we would:
        # 1. Get the user's web push subscription from a model
        # 2. Use a web push library like pywebpush to send the notification
        # 3. Handle encryption and VAPID keys
        
        # Placeholder implementation - just return True to indicate success
        # In real implementation, you would use something like:
        # from webpush import send_web_push
        # user_subscription = get_user_webpush_subscription(user)
        # if user_subscription:
        #     send_web_push(
        #         subscription_info=user_subscription,
        #         data=json.dumps({'title': title, 'message': message, 'data': data}),
        #         vapid_private_key=settings.VAPID_PRIVATE_KEY,
        #         timeout=10
        #     )
        return True
        
    except Exception as e:
        logger.error(f"Error sending web push notification: {e}")
        return False


def send_push_via_mobile(user, title, message, data=None, priority='normal', platform='fcm'):
    """
    Send push notification via mobile platform (FCM, APNS, etc.).

    Args:
        user (User): User to send notification to
        title (str): Notification title
        message (str): Notification message
        data (dict): Additional data
        priority (str): Priority level
        platform (str): Platform to use ('fcm' for Firebase, 'apns' for Apple)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if platform == 'fcm':  # Firebase Cloud Messaging
            return send_push_via_fcm(user, title, message, data, priority)
        elif platform == 'apns':  # Apple Push Notification Service
            return send_push_via_apns(user, title, message, data, priority)
        else:
            logger.error(f"Unsupported push platform: {platform}")
            return False
    
    except Exception as e:
        logger.error(f"Error sending push notification via {platform}: {e}")
        return False


def send_push_via_fcm(user, title, message, data=None, priority='normal'):
    """
    Send push notification via Firebase Cloud Messaging.
    Real implementation with firebase-admin SDK.
    """
    try:
        import firebase_admin
        from firebase_admin import credentials, messaging
        from django.conf import settings

        # Initialize Firebase Admin if not already initialized
        if not firebase_admin._apps:
            cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', None)
            if cred_path:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                logger.warning("Firebase credentials not configured")
                return False

        # Get user's FCM token
        fcm_token = get_user_fcm_token(user)
        if not fcm_token:
            logger.info(f"No FCM token for user {user.id}")
            return False

        # Create message
        fcm_message = messaging.Message(
            data=data or {},
            notification=messaging.Notification(
                title=title,
                body=message
            ),
            android=messaging.AndroidConfig(
                priority='high' if priority == 'high' else 'normal',
                notification=messaging.AndroidNotification(
                    title=title,
                    body=message,
                    sound='default'
                ),
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        alert=messaging.ApsAlert(title=title, body=message),
                        sound='default'
                    ),
                )
            ),
            token=fcm_token
        )

        # Send message
        response = messaging.send(fcm_message)
        logger.info(f"FCM message sent successfully: {response}")
        return True

    except ImportError:
        logger.error("Firebase Admin SDK not installed. Run: pip install firebase-admin")
        return False
    except Exception as e:
        logger.error(f"Error sending FCM push notification: {e}")
        return False


def send_push_via_apns(user, title, message, data=None, priority='normal'):
    """
    Send push notification via Apple Push Notification Service.

    Args:
        user (User): User to send notification to
        title (str): Notification title
        message (str): Notification message
        data (dict): Additional data
        priority (str): Priority level (normal, high)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # This would require the apns2 library
        # For now, we'll provide a placeholder implementation
        
        # In a real implementation:
        # from apns2.client import APNsClient
        # from apns2.payload import Payload
        #
        # # Get user's APNS token
        # apns_token = get_user_apns_token(user)
        # if not apns_token:
        #     return False
        #
        # # Create payload
        # payload = Payload(
        #     alert={'title': title, 'body': message},
        #     sound="default",
        #     badge=1,
        #     custom=data or {}
        # )
        #
        # # Send notification
        # client = APNsClient(settings.APNS_CERTIFICATE_FILE, use_sandbox=settings.APNS_USE_SANDBOX)
        # client.send_notification(apns_token, payload, priority=priority)
        
        # Placeholder implementation
        return True
        
    except ImportError:
        logger.error("APNs2 library not installed")
        return False
    except Exception as e:
        logger.error(f"Error sending APNS push notification: {e}")
        return False


def send_bulk_push_notifications(users, title, message, data=None):
    """
    Send bulk push notifications to multiple users.

    Args:
        users: Queryset of User objects or list of User objects
        title (str): Notification title
        message (str): Notification message
        data (dict): Additional data to include

    Returns:
        dict: Result with sent, failed counts
    """
    sent_count = 0
    failed_count = 0
    
    for user in users:
        success = send_push_notification(user, title, message, data)
        if success:
            sent_count += 1
        else:
            failed_count += 1
    
    return {
        'total': len(users),
        'sent': sent_count,
        'failed': failed_count
    }


def get_user_push_tokens(user):
    """
    Get push notification tokens for a user (placeholder implementation).

    Args:
        user (User): User object

    Returns:
        list: List of push tokens
    """
    # This would normally retrieve tokens from a dedicated model
    # For example, UserPushToken model that stores FCM/APNS tokens
    # Placeholder implementation
    return []


def register_user_push_token(user, token, platform='web'):
    """
    Register a push notification token for a user (placeholder implementation).

    Args:
        user (User): User object
        token (str): Push token
        platform (str): Platform ('web', 'fcm', 'apns')

    Returns:
        bool: True if registration was successful
    """
    # This would normally store the token in a UserPushToken model
    # Placeholder implementation
    return True

def get_user_fcm_token(user):
    """Get user's FCM token from profile or dedicated model."""
    try:
        if hasattr(user, 'profile') and hasattr(user.profile, 'fcm_token'):
            return user.profile.fcm_token
        # Alternative: Check PushToken model if exists
        # from .models import PushToken
        # token = PushToken.objects.filter(user=user, platform='fcm', is_active=True).first()
        # return token.token if token else None
        return None
    except Exception as e:
        logger.error(f"Error getting FCM token: {e}")
        return None


def get_user_apns_token(user):
    """Get user's APNS token from profile."""
    try:
        if hasattr(user, 'profile') and hasattr(user.profile, 'apns_token'):
            return user.profile.apns_token
        return None
    except Exception as e:
        logger.error(f"Error getting APNS token: {e}")
        return None
