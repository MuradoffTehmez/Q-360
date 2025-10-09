"""
Utility functions for notifications app.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from .models import Notification, EmailTemplate, EmailLog


def send_notification(recipient, title, message, notification_type='info', link='', send_email=True):
    """
    Send a system notification and optionally an email to a user.

    Args:
        recipient: User object to receive the notification
        title: Notification title
        message: Notification message
        notification_type: Type of notification (info, success, warning, error)
        link: Optional link for the notification
        send_email: Whether to send email notification as well

    Returns:
        Notification object
    """
    # Create system notification
    notification = Notification.objects.create(
        user=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        link=link
    )

    # Send email if requested
    if send_email and recipient.email:
        try:
            send_simple_email(
                recipient_email=recipient.email,
                subject=title,
                message=message,
                recipient_name=recipient.get_full_name(),
                recipient_user=recipient
            )
        except Exception as e:
            print(f"Email sending failed: {e}")

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


def send_bulk_notification(recipients, title, message, notification_type='info', link=''):
    """
    Send notification to multiple users.

    Args:
        recipients: QuerySet or list of User objects
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        link: Optional link

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
            send_email=False  # Don't send individual emails in bulk
        )
        notifications.append(notification)

    return notifications


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
