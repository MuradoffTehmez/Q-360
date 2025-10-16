"""
Signals for training app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender='development_plans.DevelopmentGoal')
def trigger_training_assignment(sender, instance, created, **kwargs):
    """
    Yeni DevelopmentGoal yaradılanda, uyğun TrainingResource tövsiyə edən
    Celery Task-ı işə salır.

    Signal: post_save from DevelopmentGoal
    Triggers: assign_training_for_development_goal Celery task
    """
    # Only trigger for new goals that are active
    if created and instance.status in ['active', 'pending_approval']:
        try:
            from apps.training.tasks import assign_training_for_development_goal
            from django.conf import settings

            # Check if Celery is in eager mode (development)
            if getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False):
                # Run synchronously in development
                assign_training_for_development_goal(instance.id)
            else:
                # Trigger Celery task asynchronously in production
                assign_training_for_development_goal.delay(instance.id)

            logger.info(
                f"Triggered training assignment task for DevelopmentGoal {instance.id} "
                f"(User: {instance.user.username})"
            )

        except Exception as e:
            # Log but don't crash if Celery/Redis is unavailable
            logger.warning(
                f"Could not trigger training assignment for goal {instance.id}: {str(e)}. "
                "This is expected in development mode without Redis."
            )


@receiver(post_save, sender='training.UserTraining')
def notify_user_on_training_assignment(sender, instance, created, **kwargs):
    """
    Yeni təlim təyin olunduqda istifadəçiyə bildiriş göndərir.

    Signal: post_save from UserTraining
    Action: Creates notification for the user
    """
    if created:
        try:
            from apps.notifications.models import Notification

            # Create notification for the assigned user
            notification_message = (
                f"Sizə yeni təlim təyin edildi: {instance.resource.title}. "
            )

            if instance.due_date:
                notification_message += f"Son tarix: {instance.due_date}. "

            if instance.assignment_type == 'mandatory':
                notification_message += "Bu təlim məcburidir."
            elif instance.assignment_type == 'manager_assigned':
                notification_message += f"Təyin edən: {instance.assigned_by.get_full_name()}"

            Notification.objects.create(
                user=instance.user,
                title="Yeni Təlim Təyini",
                message=notification_message,
                notification_type='assignment',
                is_read=False
            )

            logger.info(
                f"Created notification for user {instance.user.username} "
                f"for training {instance.resource.title}"
            )

        except Exception as e:
            logger.exception(
                f"Failed to create notification for training assignment {instance.id}: {str(e)}"
            )


@receiver(post_save, sender='training.UserTraining')
def notify_on_training_completion(sender, instance, created, **kwargs):
    """
    Təlim tamamlandıqda istifadəçiyə və menecerə bildiriş göndərir.

    Signal: post_save from UserTraining
    Action: Creates notifications on completion
    """
    if not created and instance.status == 'completed':
        try:
            from apps.notifications.models import Notification

            # Notify the user
            Notification.objects.create(
                user=instance.user,
                title="Təlim Tamamlandı",
                message=f"Təbrik edirik! '{instance.resource.title}' təlimini uğurla tamamladınız.",
                notification_type='success',
                is_read=False
            )

            # Notify the manager/supervisor if exists
            if instance.user.supervisor:
                Notification.objects.create(
                    user=instance.user.supervisor,
                    title="Təlim Tamamlandı",
                    message=(
                        f"{instance.user.get_full_name()} '{instance.resource.title}' "
                        f"təlimini tamamladı."
                    ),
                    notification_type='info',
                    is_read=False
                )

            logger.info(
                f"Created completion notifications for training {instance.id}"
            )

        except Exception as e:
            logger.exception(
                f"Failed to create completion notification for training {instance.id}: {str(e)}"
            )


@receiver(post_save, sender='competencies.UserSkill')
def suggest_training_for_low_skill(sender, instance, created, **kwargs):
    """
    İstifadəçinin bacarıq balı aşağı olduqda avtomatik təlim tövsiyəsi.

    Signal: post_save from UserSkill
    Triggers: Training recommendation when score is low
    """
    # Only check for approved skills with low scores
    if instance.is_approved and instance.current_score:
        # If score is below 60, suggest training
        if instance.current_score < 60:
            try:
                from apps.training.models import TrainingResource, UserTraining
                from django.utils import timezone

                # Find trainings for this competency
                related_trainings = TrainingResource.objects.filter(
                    required_competencies=instance.competency,
                    is_active=True
                ).exclude(
                    # Exclude already assigned trainings
                    user_trainings__user=instance.user
                )[:3]  # Limit to 3 recommendations

                for training in related_trainings:
                    # Create a recommended training assignment
                    UserTraining.objects.create(
                        user=instance.user,
                        resource=training,
                        assignment_type='system_recommended',
                        status='pending',
                        start_date=timezone.now().date()
                    )

                    logger.info(
                        f"Auto-recommended training '{training.title}' to user "
                        f"{instance.user.username} for low skill score in "
                        f"{instance.competency.name}"
                    )

            except Exception as e:
                logger.exception(
                    f"Failed to suggest training for low skill {instance.id}: {str(e)}"
                )
