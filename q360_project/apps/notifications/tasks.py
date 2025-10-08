"""Celery tasks for notifications."""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


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
