"""
Signal handlers for evaluations app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EvaluationAssignment, EvaluationResult, Response


@receiver(post_save, sender=EvaluationAssignment)
def update_result_on_completion(sender, instance, **kwargs):
    """Update evaluation result when assignment is completed."""
    if instance.status == 'completed':
        result, created = EvaluationResult.objects.get_or_create(
            campaign=instance.campaign,
            evaluatee=instance.evaluatee
        )
        result.calculate_scores()


@receiver(post_save, sender=Response)
def trigger_sentiment_analysis(sender, instance, created, **kwargs):
    """
    Trigger asynchronous sentiment analysis when a Response is created or updated.

    Args:
        sender: The Response model class
        instance: The Response instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments

    Note:
        - Uses Celery task to analyze sentiment asynchronously
        - Only triggers if there's text to analyze (text_answer or comment)
        - Avoids infinite loops by checking if sentiment was just updated
        - Disabled if Celery/Redis is not available (development mode)
    """
    # Check if there's any text to analyze
    has_text = bool(instance.text_answer or instance.comment)

    # Only trigger analysis if there's text
    if has_text:
        try:
            # Import task here to avoid circular imports
            from .tasks import analyze_sentiment_task
            # Trigger the Celery task asynchronously
            analyze_sentiment_task.delay(instance.pk)
        except Exception as e:
            # If Celery/Redis is not available, perform sync analysis
            from apps.sentiment_analysis.services import analyze_text
            from django.db import transaction

            text_to_analyze = instance.text_answer.strip() if instance.text_answer else ""
            if not text_to_analyze and instance.comment:
                text_to_analyze = instance.comment.strip()

            if text_to_analyze:
                score, category = analyze_text(text_to_analyze)
                with transaction.atomic():
                    instance.sentiment_score = score
                    instance.sentiment_category = category
                    instance.save(update_fields=['sentiment_score', 'sentiment_category', 'updated_at'])
