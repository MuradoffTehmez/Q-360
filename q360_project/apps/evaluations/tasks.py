"""
Celery tasks for evaluations app.
Includes asynchronous sentiment analysis for responses.
"""
import logging
from celery import shared_task
from django.db import transaction

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # 1 minute
    autoretry_for=(Exception,)
)
def analyze_sentiment_task(self, response_id):
    """
    Analyze sentiment for a Response instance asynchronously.

    Args:
        response_id: ID of the Response object to analyze

    Returns:
        dict: Dictionary containing the analysis results
            {
                'success': bool,
                'response_id': int,
                'score': float,
                'category': str,
                'text_length': int
            }
    """
    from apps.evaluations.models import Response
    from apps.sentiment_analysis.services import analyze_text

    try:
        logger.info(f"Starting sentiment analysis for Response ID: {response_id}")

        # Fetch the response instance
        try:
            response = Response.objects.get(pk=response_id)
        except Response.DoesNotExist:
            logger.error(f"Response with ID {response_id} does not exist")
            return {
                'success': False,
                'response_id': response_id,
                'error': 'Response not found'
            }

        # Get the text to analyze (prioritize text_answer, fallback to comment)
        text_to_analyze = response.text_answer.strip() if response.text_answer else ""

        if not text_to_analyze and response.comment:
            text_to_analyze = response.comment.strip()

        # If there's no text, set neutral sentiment
        if not text_to_analyze:
            logger.debug(f"No text found for Response ID {response_id}, setting neutral")
            score, category = 0.0, 'neutral'
        else:
            # Perform sentiment analysis
            score, category = analyze_text(text_to_analyze)

        # Update the response with sentiment data using atomic transaction
        # Use update_fields to avoid triggering the post_save signal again (preventing loops)
        with transaction.atomic():
            response.sentiment_score = score
            response.sentiment_category = category
            response.save(update_fields=['sentiment_score', 'sentiment_category', 'updated_at'])

        logger.info(
            f"Sentiment analysis complete for Response ID {response_id}: "
            f"score={score}, category={category}, text_length={len(text_to_analyze)}"
        )

        return {
            'success': True,
            'response_id': response_id,
            'score': score,
            'category': category,
            'text_length': len(text_to_analyze)
        }

    except Exception as exc:
        logger.error(
            f"Error analyzing sentiment for Response ID {response_id}: {exc}",
            exc_info=True
        )
        # Retry the task
        raise self.retry(exc=exc)
