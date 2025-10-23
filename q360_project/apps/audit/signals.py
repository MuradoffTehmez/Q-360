"""
Signals for audit app.
Automatically updates search vectors when audit logs are created.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
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
