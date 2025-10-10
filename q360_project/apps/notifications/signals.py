"""
Signals for notifications app.
Handles cache invalidation when notifications are created or updated.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from .models import Notification


@receiver(post_save, sender=Notification)
def invalidate_notification_cache_on_save(sender, instance, created, **kwargs):
    """
    Invalidate user's notification fragment cache when a notification is created or updated.
    This ensures the navbar shows updated notification count immediately.
    """
    # Generate the cache key for the user's notification fragment
    cache_key = make_template_fragment_key('user_notifications', [instance.user.pk])

    # Delete the cache entry
    cache.delete(cache_key)

    # Optionally log the cache invalidation for debugging
    if created:
        print(f"[Cache] Notification cache invalidated for user {instance.user.pk} (new notification)")
    else:
        print(f"[Cache] Notification cache invalidated for user {instance.user.pk} (updated notification)")


@receiver(post_delete, sender=Notification)
def invalidate_notification_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate user's notification fragment cache when a notification is deleted.
    """
    cache_key = make_template_fragment_key('user_notifications', [instance.user.pk])
    cache.delete(cache_key)

    print(f"[Cache] Notification cache invalidated for user {instance.user.pk} (deleted notification)")
