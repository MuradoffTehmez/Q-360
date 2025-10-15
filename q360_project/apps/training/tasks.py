"""
Celery tasks for training app.
"""
from celery import shared_task
from django.utils import timezone
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


@shared_task(name='training.assign_training_for_development_goal')
def assign_training_for_development_goal(goal_id):
    """
    Yeni DevelopmentGoal yaradılanda, əgər məqsəd kompetensiya ilə əlaqəlidirsə,
    uyğun TrainingResource tövsiyə edən Celery Task.

    Args:
        goal_id: DevelopmentGoal ID

    Returns:
        dict: Təyin olunan təlimlərin məlumatları
    """
    try:
        from apps.development_plans.models import DevelopmentGoal
        from apps.training.models import TrainingResource, UserTraining
        from apps.competencies.models import Competency

        # Get the development goal
        try:
            goal = DevelopmentGoal.objects.select_related('user').get(id=goal_id)
        except DevelopmentGoal.DoesNotExist:
            logger.error(f"DevelopmentGoal with id {goal_id} does not exist.")
            return {
                'success': False,
                'error': 'Development goal not found',
                'goal_id': goal_id
            }

        # Extract competencies from goal title or description
        # This is a simple keyword-based matching approach
        # You may want to enhance this with more sophisticated NLP or tagging

        goal_text = f"{goal.title} {goal.description} {goal.category}".lower()

        # Find competencies that match keywords in the goal
        competencies = Competency.objects.filter(
            Q(name__icontains=goal.category) |
            Q(description__icontains=goal.category),
            is_active=True
        )

        if not competencies.exists():
            # Try to find by parsing title/description for common keywords
            # This is a basic approach - enhance as needed
            logger.info(f"No direct competency match found for goal {goal_id}")
            return {
                'success': True,
                'message': 'No matching competencies found',
                'goal_id': goal_id,
                'assigned_trainings': []
            }

        # Find training resources related to these competencies
        training_resources = TrainingResource.objects.filter(
            required_competencies__in=competencies,
            is_active=True
        ).distinct()[:5]  # Limit to top 5 recommendations

        assigned_trainings = []

        for resource in training_resources:
            # Check if user is not already assigned to this training
            # IMPORTANT: Allow re-assignment if previous training was completed
            existing_training = UserTraining.objects.filter(
                user=goal.user,
                resource=resource
            ).exclude(
                status='completed'  # Allow re-recommendation after completion
            ).first()

            if existing_training:
                logger.info(
                    f"User {goal.user.username} already assigned to training {resource.title} "
                    f"with status {existing_training.status}"
                )
                continue

            # Create UserTraining assignment
            user_training = UserTraining.objects.create(
                user=goal.user,
                resource=resource,
                assignment_type='system_recommended',
                related_goal=goal,
                start_date=timezone.now().date(),
                due_date=goal.target_date,
                status='pending'
            )

            assigned_trainings.append({
                'training_id': resource.id,
                'training_title': resource.title,
                'user_training_id': user_training.id
            })

            logger.info(
                f"Assigned training '{resource.title}' to user {goal.user.username} "
                f"for goal '{goal.title}'"
            )

        return {
            'success': True,
            'goal_id': goal_id,
            'goal_title': goal.title,
            'user': goal.user.username,
            'assigned_trainings': assigned_trainings,
            'total_assigned': len(assigned_trainings)
        }

    except Exception as e:
        logger.exception(f"Error in assign_training_for_development_goal task: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'goal_id': goal_id
        }


@shared_task(name='training.send_training_due_reminders')
def send_training_due_reminders(days_before=7):
    """
    Təlimlərin son tarixinə yaxınlaşdıqda istifadəçilərə xatırlatma göndərir.

    Args:
        days_before: Neçə gün əvvəl xatırlatma göndərilsin

    Returns:
        dict: Göndərilən xatırlatmaların sayı
    """
    try:
        from apps.training.models import UserTraining
        from apps.notifications.models import Notification
        from datetime import timedelta

        target_date = timezone.now().date() + timedelta(days=days_before)

        # Find trainings due on target date
        upcoming_trainings = UserTraining.objects.filter(
            due_date=target_date,
            status__in=['pending', 'in_progress'],
            user__is_active=True
        ).select_related('user', 'resource')

        notifications_sent = 0

        for training in upcoming_trainings:
            try:
                # Create notification for the user
                Notification.objects.create(
                    user=training.user,
                    title=f"Təlim Xatırlatması: {training.resource.title}",
                    message=f"{training.resource.title} təliminin son tarixi {days_before} gün sonra "
                            f"({training.due_date}) başa çatır. Zəhmət olmasa, təlimi vaxtında tamamlayın.",
                    notification_type='reminder',
                    is_read=False
                )
                notifications_sent += 1

            except Exception as e:
                logger.error(
                    f"Failed to create notification for training {training.id}: {str(e)}"
                )

        return {
            'success': True,
            'notifications_sent': notifications_sent,
            'days_before': days_before,
            'target_date': str(target_date)
        }

    except Exception as e:
        logger.exception(f"Error in send_training_due_reminders task: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@shared_task(name='training.update_overdue_trainings')
def update_overdue_trainings():
    """
    Müddəti keçmiş təlimləri yoxlayır və statuslarını yenilənir.

    Returns:
        dict: Yenilənmiş təlimlərin sayı
    """
    try:
        from apps.training.models import UserTraining

        current_date = timezone.now().date()

        # Find overdue trainings
        overdue_trainings = UserTraining.objects.filter(
            due_date__lt=current_date,
            status__in=['pending', 'in_progress']
        )

        updated_count = 0

        for training in overdue_trainings:
            # You can choose to auto-mark as failed or just send notifications
            # For now, we'll just log and send notification
            logger.warning(
                f"Training {training.id} for user {training.user.username} is overdue"
            )
            updated_count += 1

        return {
            'success': True,
            'overdue_trainings': updated_count,
            'checked_date': str(current_date)
        }

    except Exception as e:
        logger.exception(f"Error in update_overdue_trainings task: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@shared_task(name='training.recommend_trainings_for_user')
def recommend_trainings_for_user(user_id, competency_ids=None, limit=5):
    """
    İstifadəçi üçün kompetensiyalara əsasən təlim tövsiyələri generasiya edir.

    Args:
        user_id: User ID
        competency_ids: List of Competency IDs (optional)
        limit: Maksimum tövsiyə sayı

    Returns:
        dict: Tövsiyə olunan təlimlər
    """
    try:
        from apps.accounts.models import User
        from apps.training.models import TrainingResource, UserTraining
        from apps.competencies.models import Competency, UserSkill

        # Get the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return {
                'success': False,
                'error': 'User not found',
                'user_id': user_id
            }

        # Get competencies to focus on
        if competency_ids:
            competencies = Competency.objects.filter(
                id__in=competency_ids,
                is_active=True
            )
        else:
            # Get user's skills that need improvement
            user_skills = UserSkill.objects.filter(
                user=user,
                is_approved=True
            ).select_related('competency', 'level')

            # Find competencies where user has low scores
            low_score_competencies = [
                skill.competency for skill in user_skills
                if skill.current_score and skill.current_score < 70
            ]

            competencies = Competency.objects.filter(
                id__in=[c.id for c in low_score_competencies]
            )

        if not competencies.exists():
            return {
                'success': True,
                'message': 'No competencies found for recommendations',
                'recommendations': []
            }

        # Find trainings for these competencies
        # IMPORTANT: Exclude trainings that user is currently working on (not completed)
        # Allow recommendations for completed trainings (user may want to retake)
        recommended_trainings = TrainingResource.objects.filter(
            required_competencies__in=competencies,
            is_active=True
        ).exclude(
            # Exclude only non-completed trainings (pending, in_progress, cancelled, failed)
            user_trainings__user=user,
            user_trainings__status__in=['pending', 'in_progress', 'cancelled', 'failed']
        ).distinct()[:limit]

        recommendations = []

        for training in recommended_trainings:
            recommendations.append({
                'training_id': training.id,
                'title': training.title,
                'type': training.type,
                'difficulty_level': training.difficulty_level,
                'duration_hours': str(training.duration_hours) if training.duration_hours else None,
                'competencies': [
                    comp.name for comp in training.required_competencies.all()
                ]
            })

        return {
            'success': True,
            'user_id': user_id,
            'recommendations': recommendations,
            'total_recommendations': len(recommendations)
        }

    except Exception as e:
        logger.exception(f"Error in recommend_trainings_for_user task: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'user_id': user_id
        }
