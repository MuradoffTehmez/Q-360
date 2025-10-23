"""
Signals for audit app.
Automatically updates search vectors and broadcasts real-time alerts.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import AuditLog
from .search import update_audit_search_vector
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AuditLog)
def update_search_vector_on_save(sender, instance, created, **kwargs):
    """
    Automatically update search vector when audit log is saved.
    """
    if created:
        try:
            update_audit_search_vector(instance)
            logger.debug(f"Search vector updated for audit log {instance.pk}")
        except Exception as e:
            logger.error(f"Error updating search vector for audit log {instance.pk}: {e}")


@receiver(post_save, sender=AuditLog)
def broadcast_high_threat_alert(sender, instance, created, **kwargs):
    """
    Broadcast high-threat events to WebSocket clients.
    """
    if not created:
        return

    # Only broadcast high threats
    if instance.threat_score < 60:
        return

    channel_layer = get_channel_layer()

    if not channel_layer:
        return

    # Prepare alert data
    alert_data = {
        'id': instance.id,
        'user': instance.user.username if instance.user else 'N/A',
        'action': instance.action,
        'threat_level': instance.threat_level,
        'threat_score': instance.threat_score,
        'ip_address': instance.ip_address,
        'timestamp': instance.created_at.isoformat(),
        'severity': instance.severity
    }

    # Broadcast to threat monitor room
    try:
        async_to_sync(channel_layer.group_send)(
            'threat_monitor',
            {
                'type': 'threat_alert',
                'data': alert_data
            }
        )
        logger.info(f"Broadcast threat alert for log {instance.id}")
    except Exception as e:
        logger.error(f"Error broadcasting threat alert: {e}")


@receiver(post_save, sender=AuditLog)
def broadcast_new_audit_log(sender, instance, created, **kwargs):
    """
    Broadcast all new audit logs to admin dashboard.
    """
    if not created:
        return

    channel_layer = get_channel_layer()

    if not channel_layer:
        return

    # Prepare log data
    log_data = {
        'id': instance.id,
        'user': instance.user.username if instance.user else 'N/A',
        'action': instance.action,
        'model_name': instance.model_name,
        'severity': instance.severity,
        'threat_level': instance.threat_level,
        'threat_score': instance.threat_score,
        'timestamp': instance.created_at.isoformat()
    }

    # Broadcast to audit logs room
    try:
        async_to_sync(channel_layer.group_send)(
            'audit_logs',
            {
                'type': 'new_audit_log',
                'data': log_data
            }
        )
    except Exception as e:
        logger.error(f"Error broadcasting audit log: {e}")
