"""Celery tasks for notifications."""
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from .models import (
    EmailNotification,
    EmailLog,
    SMSNotification,
    SMSLog,
    PushNotification,
    PushDevice,
)
from .sms_utils import send_sms_notification
from .push_utils import send_push_notification as dispatch_push


def _reschedule_later(task, record, eta):
    """Reschedule a task for future delivery respecting existing ETA."""
    task.apply_async((record.pk,), eta=eta)


@shared_task(bind=True)
def deliver_email_notification(self, email_notification_id):
    """Send an email notification using Django's email backend."""
    try:
        record = EmailNotification.objects.select_related('recipient', 'template').get(pk=email_notification_id)
    except EmailNotification.DoesNotExist:
        return

    if record.status == 'sent':
        return

    if record.scheduled_for and record.scheduled_for > timezone.now():
        _reschedule_later(self, record, record.scheduled_for)
        return

    record.mark_sending(task_id=getattr(self.request, 'id', None))

    try:
        send_mail(
            subject=record.subject,
            message=record.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[record.recipient_email],
            fail_silently=False,
        )
    except Exception as exc:  # pragma: no cover - backend specific errors depend on environment
        record.mark_failed(str(exc))
        raise

    record.mark_sent()

    if record.recipient:
        EmailLog.objects.create(
            template=record.template,
            recipient=record.recipient,
            recipient_email=record.recipient_email,
            subject=record.subject,
            status='sent',
            sent_at=record.sent_at,
        )


@shared_task(bind=True)
def deliver_sms_notification(self, sms_notification_id):
    """Send an SMS notification using configured providers."""
    try:
        record = SMSNotification.objects.select_related('provider', 'recipient').get(pk=sms_notification_id)
    except SMSNotification.DoesNotExist:
        return

    if record.status == 'sent':
        return

    if record.scheduled_for and record.scheduled_for > timezone.now():
        _reschedule_later(self, record, record.scheduled_for)
        return

    record.mark_sending(task_id=getattr(self.request, 'id', None))

    provider_name = record.provider.name if record.provider else None
    success = send_sms_notification(
        recipient_phone=record.recipient_phone,
        message=record.message,
        provider_name=provider_name,
        user=record.recipient,
    )

    if success:
        record.mark_sent()
    else:
        record.mark_failed(_('SMS göndərilmədi'))

    if record.recipient and record.provider:
        SMSLog.objects.create(
            recipient=record.recipient,
            recipient_phone=record.recipient_phone,
            message=record.message,
            provider=record.provider,
            status='sent' if success else 'failed',
            sent_at=timezone.now() if success else None,
            error_message='' if success else _('SMS göndərmə xətası'),
        )


@shared_task(bind=True)
def deliver_push_notification(self, push_notification_id):
    """Send a push notification via configured push gateway (e.g. FCM/WebPush)."""
    try:
        record = PushNotification.objects.select_related('user', 'device').get(pk=push_notification_id)
    except PushNotification.DoesNotExist:
        return

    if record.status == 'sent':
        return

    if record.scheduled_for and record.scheduled_for > timezone.now():
        _reschedule_later(self, record, record.scheduled_for)
        return

    record.mark_sending(task_id=getattr(self.request, 'id', None))

    success = dispatch_push(
        user=record.user,
        title=record.title,
        message=record.message,
        data=record.data,
        priority=record.priority,
        notification_record=record,
        device=record.device,
    )

    if not success and not record.error_message:
        record.mark_failed(_('Push bildirişi göndərilmədi'))


@shared_task
def send_email_notification(subject, message, recipient_list):
    """Legacy helper to send email immediately."""
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )


@shared_task
def send_campaign_start_notification(campaign_id):
    """Send notification when a campaign starts (placeholder)."""
    from apps.evaluations.models import EvaluationCampaign

    EvaluationCampaign.objects.get(id=campaign_id)
    # TODO: implement campaign notifications
    return


@shared_task
def send_email_notification_task(
    recipient_email,
    subject,
    message,
    recipient_name='',
    recipient_user_id=None,
    template_id=None,
    scheduled_for=None,
    priority='normal',
):
    """Backward compatible wrapper to queue an email notification."""
    recipient_user = None
    if recipient_user_id:
        recipient_user = User.objects.filter(id=recipient_user_id).first()

    record = EmailNotification.objects.create(
        recipient=recipient_user,
        recipient_email=recipient_email,
        subject=subject,
        body=message,
        template_id=template_id,
        scheduled_for=scheduled_for,
        priority=priority,
        metadata={'recipient_name': recipient_name} if recipient_name else {},
    )
    deliver_email_notification.delay(record.id)
    return record.id


@shared_task
def send_scheduled_email_task(recipient_email, subject, message, recipient_user_id=None, scheduled_for=None):
    """Queue an email notification for scheduled delivery."""
    return send_email_notification_task(
        recipient_email=recipient_email,
        subject=subject,
        message=message,
        recipient_user_id=recipient_user_id,
        scheduled_for=scheduled_for,
    )


@shared_task
def send_sms_notification_task(
    recipient_phone,
    message,
    recipient_user_id=None,
    provider_name=None,
    scheduled_for=None,
    priority='normal',
):
    """Backward compatible wrapper to queue SMS notification."""
    from .models import SMSProvider

    recipient_user = None
    if recipient_user_id:
        recipient_user = User.objects.filter(id=recipient_user_id).first()

    provider = None
    if provider_name:
        provider = SMSProvider.objects.filter(name=provider_name).first()

    record = SMSNotification.objects.create(
        recipient=recipient_user,
        recipient_phone=recipient_phone,
        message=message,
        provider=provider,
        scheduled_for=scheduled_for,
        metadata={'priority': priority},
    )
    deliver_sms_notification.delay(record.id)
    return record.id


@shared_task
def send_push_notification_task(user_id, title, message, data=None, device_id=None, priority='normal'):
    """Queue a push notification for a user."""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return

    device = None
    if device_id:
        device = PushDevice.objects.filter(id=device_id, user=user).first()

    record = PushNotification.objects.create(
        user=user,
        device=device,
        title=title,
        message=message,
        data=data or {},
        priority=priority,
    )
    deliver_push_notification.delay(record.id)
    return record.id
