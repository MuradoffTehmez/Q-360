"""
Signal handlers for evaluations app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EvaluationAssignment, EvaluationResult


@receiver(post_save, sender=EvaluationAssignment)
def update_result_on_completion(sender, instance, **kwargs):
    """Update evaluation result when assignment is completed."""
    if instance.status == 'completed':
        result, created = EvaluationResult.objects.get_or_create(
            campaign=instance.campaign,
            evaluatee=instance.evaluatee
        )
        result.calculate_scores()
