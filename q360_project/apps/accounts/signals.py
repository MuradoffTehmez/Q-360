"""
Signal handlers for accounts app.
"""
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import logging

from .models import User, Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile instance when a new User is created.
    """
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the Profile instance when User is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(user_login_failed)
def log_login_failure(sender, credentials, request, **kwargs):
    """
    Django-nun standart user_login_failed siqnalını dinləyir və
    uğursuz giriş cəhdlərini AuditLog modelində qeyd edir.

    Signal: user_login_failed (Django built-in)
    Action: Creates AuditLog entry with action='login_failure'
    """
    try:
        from apps.audit.models import AuditLog

        # Get user if exists
        username = credentials.get('username')
        user = None

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # User not found - this is also a login failure
                pass

        # Get IP address and user agent from request
        ip_address = None
        user_agent = ''

        if request:
            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')

            # Get user agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Create audit log entry
        AuditLog.objects.create(
            user=user,  # Can be None if user doesn't exist
            action='login_failure',
            model_name='User',
            object_id=str(user.id) if user else username,
            changes={
                'attempted_username': username,
                'timestamp': timezone.now().isoformat(),
                'reason': 'Invalid credentials'
            },
            ip_address=ip_address,
            user_agent=user_agent
        )

        logger.warning(
            f"Login failure for username: {username} from IP: {ip_address}"
        )

    except Exception as e:
        logger.exception(
            f"Failed to log login failure for {credentials.get('username')}: {str(e)}"
        )


@receiver(user_login_failed)
def check_brute_force_attempts(sender, credentials, request, **kwargs):
    """
    Brute force hücumlarını yoxlayır.
    Eyni IP-dən çox sayda uğursuz giriş cəhdi olduqda xəbərdarlıq yaradır.

    Signal: user_login_failed
    Action: Checks for multiple failures from same IP
    """
    try:
        from apps.audit.models import AuditLog

        if not request:
            return

        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        if not ip_address:
            return

        # Check failures in last 15 minutes
        fifteen_minutes_ago = timezone.now() - timedelta(minutes=15)

        recent_failures = AuditLog.objects.filter(
            action='login_failure',
            ip_address=ip_address,
            created_at__gte=fifteen_minutes_ago
        ).count()

        # If more than 5 failures in 15 minutes, log warning
        if recent_failures >= 5:
            logger.error(
                f"SECURITY WARNING: Possible brute force attack from IP {ip_address}. "
                f"{recent_failures} failed login attempts in last 15 minutes."
            )

            # You can also send notification to admins here
            try:
                from apps.notifications.models import Notification

                # Notify superadmins
                superadmins = User.objects.filter(role='superadmin', is_active=True)

                for admin in superadmins:
                    Notification.objects.create(
                        user=admin,
                        title="Təhlükəsizlik Xəbərdarlığı",
                        message=(
                            f"Mümkün brute force hücumu aşkar edildi. "
                            f"IP ünvanı: {ip_address}. "
                            f"Son 15 dəqiqədə {recent_failures} uğursuz giriş cəhdi."
                        ),
                        notification_type='security',
                        is_read=False
                    )

            except Exception as notif_error:
                logger.exception(f"Failed to send brute force notification: {str(notif_error)}")

    except Exception as e:
        logger.exception(f"Error in brute force check: {str(e)}")
