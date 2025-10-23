"""
Signals for development_plans app.
Handles automatic alignment calculation for goals.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import DevelopmentGoal
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=DevelopmentGoal)
def update_goal_alignment_on_save(sender, instance, **kwargs):
    """
    Automatically calculate alignment percentage when goal is saved
    if parent_goal or strategic_objective changed.
    """
    # Only calculate for existing goals
    if instance.pk:
        try:
            old_instance = DevelopmentGoal.objects.get(pk=instance.pk)

            # Check if relationships changed
            parent_changed = old_instance.parent_goal != instance.parent_goal
            strategic_changed = old_instance.strategic_objective != instance.strategic_objective
            department_changed = old_instance.related_department != instance.related_department

            if parent_changed or strategic_changed or department_changed:
                # Recalculate alignment
                new_alignment = instance.calculate_alignment_percentage()
                instance.alignment_percentage = new_alignment
                logger.info(
                    f"Updated alignment for goal '{instance.title}' (ID: {instance.pk}): "
                    f"{new_alignment}% (parent_changed={parent_changed}, "
                    f"strategic_changed={strategic_changed}, department_changed={department_changed})"
                )
        except DevelopmentGoal.DoesNotExist:
            # New goal, calculate initial alignment
            pass


@receiver(post_save, sender=DevelopmentGoal)
def calculate_initial_alignment(sender, instance, created, **kwargs):
    """
    Calculate initial alignment for newly created goals.
    """
    if created:
        # Calculate alignment after creation
        if instance.parent_goal or instance.strategic_objective:
            new_alignment = instance.calculate_alignment_percentage()

            # Only update if different from default
            if new_alignment != instance.alignment_percentage:
                DevelopmentGoal.objects.filter(pk=instance.pk).update(
                    alignment_percentage=new_alignment
                )
                logger.info(
                    f"Initial alignment calculated for goal '{instance.title}' (ID: {instance.pk}): "
                    f"{new_alignment}%"
                )


@receiver(post_save, sender=DevelopmentGoal)
def update_child_goals_alignment(sender, instance, **kwargs):
    """
    When a parent goal's title/description changes,
    update alignment for all child goals.
    """
    # Skip during creation
    if kwargs.get('created'):
        return

    # Check if title or description changed
    try:
        old_instance = DevelopmentGoal.objects.get(pk=instance.pk)

        title_changed = old_instance.title != instance.title
        desc_changed = old_instance.description != instance.description

        if title_changed or desc_changed:
            # Update alignment for all child goals
            child_goals = instance.child_goals.all()

            if child_goals.exists():
                updated_count = 0
                for child in child_goals:
                    new_alignment = child.calculate_alignment_percentage()
                    if new_alignment != child.alignment_percentage:
                        child.alignment_percentage = new_alignment
                        child.save(update_fields=['alignment_percentage', 'updated_at'])
                        updated_count += 1

                if updated_count > 0:
                    logger.info(
                        f"Updated alignment for {updated_count} child goals after parent goal "
                        f"'{instance.title}' (ID: {instance.pk}) changed"
                    )
    except DevelopmentGoal.DoesNotExist:
        pass
