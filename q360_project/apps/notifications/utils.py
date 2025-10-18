"""
Utility functions for notifications app.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from .models import Notification, EmailTemplate, EmailLog


def send_notification(recipient, title, message, notification_type='info', link='', send_email=True, send_sms=False, send_push=False, channel='in_app', priority='normal'):
    """
    Send a system notification and optionally to email, SMS, or push to a user.

    Args:
        recipient: User object to receive the notification
        title: Notification title
        message: Notification message
        notification_type: Type of notification (info, success, warning, error, etc.)
        link: Optional link for the notification
        send_email: Whether to send email notification as well
        send_sms: Whether to send SMS notification as well
        send_push: Whether to send push notification as well
        channel: The primary channel for the notification
        priority: Priority level ('low', 'normal', 'high', 'urgent')

    Returns:
        Notification object
    """
    from .models import UserNotificationPreference
    from django.utils import timezone
    from datetime import datetime, time
    
    # Get user preferences
    user_prefs, created = UserNotificationPreference.objects.get_or_create(user=recipient)
    
    # Check Do Not Disturb settings
    current_time = timezone.now().time()
    is_dnd_time = False
    if user_prefs.dnd_start_time and user_prefs.dnd_end_time:
        if user_prefs.dnd_start_time <= user_prefs.dnd_end_time:
            # Same day DND (e.g., 22:00 to 08:00)
            is_dnd_time = user_prefs.dnd_start_time <= current_time <= user_prefs.dnd_end_time
        else:
            # Overnight DND (e.g., 22:00 to 08:00 next day)
            is_dnd_time = current_time >= user_prefs.dnd_start_time or current_time <= user_prefs.dnd_end_time
    
    # Check if it's a weekend and user doesn't want weekend notifications
    if not user_prefs.weekend_notifications and timezone.now().weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        is_dnd_time = True
    
    # Check if it's outside working hours
    is_working_hours = False
    if not (user_prefs.weekday_start <= current_time <= user_prefs.weekday_end):
        is_working_hours = True
    if timezone.now().weekday() >= 5:  # Weekend
        is_working_hours = False
    
    # Check if user wants this type of notification via this channel
    notification_allowed = True
    if channel == 'email':
        notification_allowed = user_prefs.email_notifications
        if notification_type == 'assignment' and not user_prefs.email_assignment:
            notification_allowed = False
        elif notification_type == 'reminder' and not user_prefs.email_reminder:
            notification_allowed = False
        elif notification_type == 'announcement' and not user_prefs.email_announcement:
            notification_allowed = False
        elif notification_type == 'security' and not user_prefs.email_security:
            notification_allowed = False
    elif channel == 'sms':
        # For SMS, also check if it's urgent and user only wants urgent SMS
        notification_allowed = user_prefs.sms_notifications
        if user_prefs.sms_important_only and priority not in ['high', 'urgent']:
            notification_allowed = False
        if notification_type == 'assignment' and not user_prefs.sms_assignment:
            notification_allowed = False
        elif notification_type == 'reminder' and not user_prefs.sms_reminder:
            notification_allowed = False
        elif notification_type == 'security' and not user_prefs.sms_security:
            notification_allowed = False
    elif channel == 'push':
        notification_allowed = user_prefs.push_notifications
        if notification_type == 'assignment' and not user_prefs.push_assignment:
            notification_allowed = False
        elif notification_type == 'reminder' and not user_prefs.push_reminder:
            notification_allowed = False
        elif notification_type == 'announcement' and not user_prefs.push_announcement:
            notification_allowed = False

    # If in DND time and notification is not urgent, defer it
    if is_dnd_time and priority not in ['high', 'urgent']:
        # Create a scheduled notification for when DND ends
        from .models import Notification
        scheduled_time = None
        if user_prefs.dnd_end_time:
            now = timezone.now()
            if current_time < user_prefs.dnd_end_time:
                # DND ends today
                scheduled_time = now.replace(
                    hour=user_prefs.dnd_end_time.hour,
                    minute=user_prefs.dnd_end_time.minute,
                    second=0,
                    microsecond=0
                )
            else:
                # DND ends tomorrow
                from datetime import timedelta
                scheduled_time = (now + timedelta(days=1)).replace(
                    hour=user_prefs.dnd_end_time.hour,
                    minute=user_prefs.dnd_end_time.minute,
                    second=0,
                    microsecond=0
                )
        
        if scheduled_time:
            notification = Notification.objects.create(
                user=recipient,
                title=title,
                message=message,
                notification_type=notification_type,
                link=link,
                channel=channel,
                priority=priority,
                scheduled_time=scheduled_time
            )
            return notification
    elif is_dnd_time and priority in ['high', 'urgent'] and is_working_hours:
        # For urgent notifications outside working hours, check if user allows them
        if priority == 'urgent' or user_prefs.push_notifications:
            # Send as urgent notification bypassing DND
            pass
        else:
            notification_allowed = False

    # Create system notification if allowed
    notification = None
    if notification_allowed or channel == 'in_app':
        from .models import Notification
        notification = Notification.objects.create(
            user=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link,
            channel=channel,
            priority=priority
        )

    # Send email if requested and user allows it
    if send_email and recipient.email and user_prefs.email_notifications:
        try:
            from .tasks import send_email_notification_task
            send_email_notification_task.delay(
                recipient_email=recipient.email,
                subject=title,
                message=message,
                recipient_name=recipient.get_full_name(),
                recipient_user_id=recipient.id
            )
        except Exception as e:
            print(f"Email sending failed: {e}")

    # Send SMS if requested and user allows it
    if send_sms and user_prefs.sms_notifications:
        try:
            phone_number = getattr(recipient, 'phone_number', None) or \
                          getattr(recipient.profile, 'work_phone', None) or \
                          getattr(recipient.profile, 'phone_number', None) if hasattr(recipient, 'profile') else None
            if phone_number:
                from .tasks import send_sms_notification_task
                send_sms_notification_task.delay(
                    recipient_phone=phone_number,
                    message=message,
                    recipient_user_id=recipient.id
                )
        except Exception as e:
            print(f"SMS sending failed: {e}")

    # Send push notification if requested and user allows it
    if send_push and user_prefs.push_notifications:
        try:
            from .tasks import send_push_notification_task
            send_push_notification_task.delay(
                user_id=recipient.id,
                title=title,
                message=message,
                data={'link': link} if link else {}
            )
        except Exception as e:
            print(f"Push notification sending failed: {e}")

    return notification


def send_notification_by_smart_routing(recipient, title, message, notification_type='info', link='', priority='normal'):
    """
    Smart notification routing based on user preferences and context.
    
    This function intelligently selects the best notification channel
    based on user preferences, priority, and context.
    
    Args:
        recipient: User to receive the notification
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        link: Optional link
        priority: Priority level ('low', 'normal', 'high', 'urgent')
    
    Returns:
        Notification object
    """
    from .models import UserNotificationPreference
    from django.utils import timezone
    
    user_prefs, created = UserNotificationPreference.objects.get_or_create(user=recipient)
    
    # Determine best channels based on priority and preferences
    channels = []
    
    # For urgent notifications, always try all enabled channels
    if priority in ['high', 'urgent']:
        if user_prefs.push_notifications:
            channels.append('push')
        if user_prefs.email_notifications and recipient.email:
            channels.append('email')
        if user_prefs.sms_notifications:
            phone_number = getattr(recipient, 'phone_number', None) or \
                          getattr(recipient.profile, 'work_phone', None) if hasattr(recipient, 'profile') else None
            if phone_number:
                channels.append('sms')
        if user_prefs.email_notifications:  # also send in-app for important
            channels.append('in_app')
    else:
        # For normal notifications, use user's preferred primary channel
        if notification_type == 'assignment':
            if user_prefs.push_assignment or user_prefs.email_assignment:
                if user_prefs.push_notifications:
                    channels.append('push')
                elif user_prefs.email_notifications and recipient.email:
                    channels.append('email')
            else:
                channels.append('in_app')
        elif notification_type == 'reminder':
            if user_prefs.push_reminder or user_prefs.email_reminder:
                if user_prefs.push_notifications:
                    channels.append('push')
                elif user_prefs.email_notifications and recipient.email:
                    channels.append('email')
            else:
                channels.append('in_app')
        elif notification_type == 'announcement':
            if user_prefs.push_announcement:
                channels.append('push')
            elif user_prefs.email_notifications and recipient.email:
                channels.append('email')
            else:
                channels.append('in_app')
        else:
            # Default to user's preference
            if user_prefs.push_notifications:
                channels.append('push')
            elif user_prefs.email_notifications and recipient.email:
                channels.append('email')
            else:
                channels.append('in_app')
    
    # Send notification through all selected channels
    notification = None
    for channel in channels:
        send_email = channel == 'email'
        send_sms = channel == 'sms'
        send_push = channel == 'push'
        
        notification = send_notification(
            recipient=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link,
            send_email=send_email,
            send_sms=send_sms,
            send_push=send_push,
            channel=channel,
            priority=priority
        )
    
    return notification


def send_simple_email(recipient_email, subject, message, recipient_name='', recipient_user=None):
    """
    Send a simple email using default template.

    Args:
        recipient_email: Recipient email address
        subject: Email subject
        message: Email message body
        recipient_name: Recipient's full name
        recipient_user: User object (optional, for logging)
    """
    # Create email log
    email_log = None
    if recipient_user:
        email_log = EmailLog.objects.create(
            recipient=recipient_user,
            recipient_email=recipient_email,
            subject=f'Q360 - {subject}',
            status='pending'
        )

    try:
        # Prepare context
        context = {
            'recipient_name': recipient_name,
            'message': message,
            'year': 2024,
        }

        # Render HTML content
        html_message = render_to_string('notifications/simple_email.html', context)
        plain_message = strip_tags(html_message)

        # Send email
        send_mail(
            subject=f'Q360 - {subject}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )

        # Update log status
        if email_log:
            email_log.status = 'sent'
            email_log.sent_at = timezone.now()
            email_log.save()

    except Exception as e:
        # Update log with error
        if email_log:
            email_log.status = 'failed'
            email_log.error_message = str(e)
            email_log.save()
        raise


def send_email_via_template(recipient_email, template_name, context_data, recipient_user=None, subject_override=None):
    """
    Send an email using a predefined template.

    Args:
        recipient_email: Recipient email address
        template_name: Name of the email template
        context_data: Dictionary of context variables
        recipient_user: User object (optional, for logging)
        subject_override: Optional subject to override template's subject
    """
    email_log = None
    try:
        from .models import EmailTemplate
        template = EmailTemplate.objects.get(name=template_name, is_active=True)

        # Replace template variables
        subject = subject_override or template.subject
        html_content = template.html_content
        text_content = template.text_content

        for key, value in context_data.items():
            placeholder = '{{ ' + key + ' }}'
            subject = subject.replace(placeholder, str(value))
            html_content = html_content.replace(placeholder, str(value))
            text_content = text_content.replace(placeholder, str(value))

        # Create email log
        if recipient_user:
            email_log = EmailLog.objects.create(
                template=template,
                recipient=recipient_user,
                recipient_email=recipient_email,
                subject=subject,
                status='pending'
            )

        # Send email
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_content,
            fail_silently=False,
        )

        # Update log status
        if email_log:
            email_log.status = 'sent'
            email_log.sent_at = timezone.now()
            email_log.save()

    except EmailTemplate.DoesNotExist:
        print(f"Email template '{template_name}' not found")
        if email_log:
            email_log.status = 'failed'
            email_log.error_message = f"Template '{template_name}' not found"
            email_log.save()
    except Exception as e:
        print(f"Email sending failed: {e}")
        if email_log:
            email_log.status = 'failed'
            email_log.error_message = str(e)
            email_log.save()


def send_template_email(recipient_email, template_name, context, recipient_user=None):
    """
    Send an email using a predefined template.

    Args:
        recipient_email: Recipient email address
        template_name: Name of the email template
        context: Dictionary of context variables
        recipient_user: User object (optional, for logging)
    """
    email_log = None
    try:
        from .models import EmailTemplate
        template = EmailTemplate.objects.get(name=template_name, is_active=True)

        # Replace template variables
        subject = template.subject
        html_content = template.html_content

        for key, value in context.items():
            placeholder = '{{ ' + key + ' }}'
            subject = subject.replace(placeholder, str(value))
            html_content = html_content.replace(placeholder, str(value))

        # Get plain text version
        if template.text_content:
            text_content = template.text_content
            for key, value in context.items():
                placeholder = '{{ ' + key + ' }}'
                text_content = text_content.replace(placeholder, str(value))
        else:
            text_content = strip_tags(html_content)

        # Create email log
        if recipient_user:
            email_log = EmailLog.objects.create(
                template=template,
                recipient=recipient_user,
                recipient_email=recipient_email,
                subject=subject,
                status='pending'
            )

        # Send email
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_content,
            fail_silently=False,
        )

        # Update log status
        if email_log:
            email_log.status = 'sent'
            email_log.sent_at = timezone.now()
            email_log.save()

    except EmailTemplate.DoesNotExist:
        print(f"Email template '{template_name}' not found")
        if email_log:
            email_log.status = 'failed'
            email_log.error_message = f"Template '{template_name}' not found"
            email_log.save()
    except Exception as e:
        print(f"Email sending failed: {e}")
        if email_log:
            email_log.status = 'failed'
            email_log.error_message = str(e)
            email_log.save()


def send_scheduled_email(recipient_email, subject, message, send_time, recipient_user=None):
    """
    Schedule an email to be sent at a specific time.

    Args:
        recipient_email: Recipient email address
        subject: Email subject
        message: Email message
        send_time: DateTime object for when to send the email
        recipient_user: User object (optional, for logging)
    """
    from datetime import datetime
    from .tasks import send_scheduled_email_task
    
    # Calculate delay in seconds
    now = timezone.now()
    delay = (send_time - now).total_seconds()
    
    if delay > 0:
        # Schedule the email
        send_scheduled_email_task.apply_async(
            args=[recipient_email, subject, message, recipient_user.id if recipient_user else None],
            eta=send_time
        )
    else:
        # If the time is in the past, send immediately
        send_simple_email(recipient_email, subject, message, recipient_user=recipient_user)


def send_bulk_emails(recipients, subject, message, template_name=None, context=None):
    """
    Send bulk emails to multiple recipients.

    Args:
        recipients: List of email addresses or User queryset
        subject: Email subject
        message: Email message
        template_name: Optional template name to use
        context: Context data for template
    """
    from .models import BulkNotification
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Convert to email list
    email_list = []
    if recipients and hasattr(recipients, 'model') and recipients.model == User:
        # This is a User queryset
        email_list = [user.email for user in recipients if user.email]
    elif isinstance(recipients, list) and recipients:
        if isinstance(recipients[0], User):
            # List of User objects
            email_list = [user.email for user in recipients if user.email]
        else:
            # List of email addresses
            email_list = recipients
    
    # Create bulk notification record
    bulk_notif = BulkNotification.objects.create(
        title=subject,
        message=message,
        recipients_count=len(email_list),
        filter_criteria={'type': 'email'},
        channels=['email'],
        initiated_by=getattr(recipients, 'initiated_by', None) if hasattr(recipients, 'initiated_by') else None
    )
    
    sent_count = 0
    failed_count = 0
    
    for email in email_list:
        try:
            if template_name:
                send_template_email(email, template_name, context or {})
            else:
                send_simple_email(email, subject, message)
            sent_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Failed to send email to {email}: {e}")
    
    # Update bulk notification record
    bulk_notif.status = 'completed'
    bulk_notif.sent_count = sent_count
    bulk_notif.failed_count = failed_count
    bulk_notif.completed_at = timezone.now()
    bulk_notif.save()
    
    return {
        'total': len(email_list),
        'sent': sent_count,
        'failed': failed_count
    }


def send_bulk_notification(recipients, title, message, notification_type='info', link='', send_email=True, send_sms=False, send_push=False):
    """
    Send notification to multiple users.

    Args:
        recipients: QuerySet or list of User objects
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        link: Optional link
        send_email: Whether to send email notifications
        send_sms: Whether to send SMS notifications
        send_push: Whether to send push notifications

    Returns:
        List of created notifications
    """
    notifications = []
    for recipient in recipients:
        notification = send_notification(
            recipient=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link,
            send_email=send_email and not send_sms and not send_push,  # For bulk, just send to DB unless other channels are specified
            send_sms=send_sms,
            send_push=send_push
        )
        notifications.append(notification)

    return notifications


def send_bulk_notification_smart(recipients, title, message, notification_type='info', priority='normal'):
    """
    Send bulk notifications using smart routing based on each user's preferences.

    Args:
        recipients: QuerySet or list of User objects
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        priority: Priority level

    Returns:
        Count of notifications sent
    """
    sent_count = 0
    for recipient in recipients:
        send_notification_by_smart_routing(
            recipient=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority
        )
        sent_count += 1
    
    return sent_count


def mark_as_read(notification_id, user):
    """
    Mark a notification as read.

    Args:
        notification_id: ID of the notification
        user: User object

    Returns:
        Boolean indicating success
    """
    try:
        from django.utils import timezone
        notification = Notification.objects.get(id=notification_id, user=user)
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return True
    except Notification.DoesNotExist:
        return False


def mark_all_as_read(user):
    """
    Mark all notifications as read for a user.

    Args:
        user: User object

    Returns:
        Number of notifications marked as read
    """
    from django.utils import timezone
    count = Notification.objects.filter(
        user=user,
        is_read=False
    ).update(
        is_read=True,
        read_at=timezone.now()
    )
    return count


def get_unread_count(user):
    """
    Get count of unread notifications for a user.

    Args:
        user: User object

    Returns:
        Integer count of unread notifications
    """
    return Notification.objects.filter(user=user, is_read=False).count()


def delete_old_notifications(days=30):
    """
    Delete read notifications older than specified days.

    Args:
        days: Number of days (default 30)

    Returns:
        Number of notifications deleted
    """
    from django.utils import timezone
    from datetime import timedelta

    cutoff_date = timezone.now() - timedelta(days=days)
    count, _ = Notification.objects.filter(
        is_read=True,
        read_at__lt=cutoff_date
    ).delete()

    return count
