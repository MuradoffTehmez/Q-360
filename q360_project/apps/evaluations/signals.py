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
    """
    # Import task here to avoid circular imports
    from .tasks import analyze_sentiment_task

    # Check if there's any text to analyze
    has_text = bool(instance.text_answer or instance.comment)

    # Only trigger analysis if there's text
    # The task itself will handle checking for update loops
    if has_text:
        # Trigger the Celery task asynchronously
        analyze_sentiment_task.delay(instance.pk)
