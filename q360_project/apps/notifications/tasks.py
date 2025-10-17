"""Celery tasks for notifications."""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import EmailLog
from apps.accounts.models import User
from .sms_utils import send_sms_notification
from .models import PushNotification, SMSLog


@shared_task
def send_email_notification(subject, message, recipient_list):
    """Send email notification asynchronously."""
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )


@shared_task
def send_campaign_start_notification(campaign_id):
    """Send notification when a campaign starts."""
    from apps.evaluations.models import EvaluationCampaign
    campaign = EvaluationCampaign.objects.get(id=campaign_id)
    # Implementation for sending notifications
    pass


@shared_task
def send_email_notification_task(recipient_email, subject, message, recipient_name='', recipient_user_id=None):
    """
    Asynchronous task to send a single email notification.
    """
    from .utils import send_simple_email
    
    recipient_user = None
    if recipient_user_id:
        try:
            recipient_user = User.objects.get(id=recipient_user_id)
        except User.DoesNotExist:
            pass
    
    send_simple_email(
        recipient_email=recipient_email,
        subject=subject,
        message=message,
        recipient_name=recipient_name,
        recipient_user=recipient_user
    )


@shared_task
def send_scheduled_email_task(recipient_email, subject, message, recipient_user_id=None):
    """
    Task for sending scheduled emails.
    """
    from .utils import send_simple_email
    
    recipient_user = None
    if recipient_user_id:
        try:
            recipient_user = User.objects.get(id=recipient_user_id)
        except User.DoesNotExist:
            pass
    
    send_simple_email(
        recipient_email=recipient_email,
        subject=subject,
        message=message,
        recipient_user=recipient_user
    )


@shared_task
def send_sms_notification_task(recipient_phone, message, recipient_user_id=None, provider_name=None):
    """
    Asynchronous task to send an SMS notification.
    """
    from .sms_utils import send_sms_notification
    
    recipient_user = None
    if recipient_user_id:
        try:
            recipient_user = User.objects.get(id=recipient_user_id)
        except User.DoesNotExist:
            pass
    
    send_sms_notification(
        recipient_phone=recipient_phone,
        message=message,
        user=recipient_user,
        provider_name=provider_name
    )


@shared_task
def send_push_notification_task(user_id, title, message, data=None):
    """
    Asynchronous task to send a push notification.
    """
    try:
        from .models import PushNotification
        user = User.objects.get(id=user_id)
        
        push_notif = PushNotification.objects.create(
            user=user,
            title=title,
            message=message,
            data=data or {}
        )
        
        # Here we would implement the actual push notification sending
        # using a service like Firebase Cloud Messaging (FCM)
        # For now, we'll just mark it as sent
        push_notif.status = 'sent'
        push_notif.sent_at = timezone.now()
        push_notif.save()
        
    except User.DoesNotExist:
        # Log the error but don't retry
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"User with ID {user_id} does not exist for push notification")
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error sending push notification: {e}")
