"""
Sentiment analysis services using VADER.
Provides text sentiment analysis for evaluation responses.
"""
import logging
from typing import Tuple

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    logging.warning("vaderSentiment not installed. Sentiment analysis will be disabled.")


logger = logging.getLogger(__name__)


def analyze_text(text: str) -> Tuple[float, str]:
    """
    Analyze sentiment of given text using VADER.

    Args:
        text: The text to analyze

    Returns:
        Tuple of (score, category) where:
        - score: compound sentiment score from -1.0 (most negative) to +1.0 (most positive)
        - category: 'positive', 'negative', or 'neutral'

    Examples:
        >>> analyze_text("This is great!")
        (0.6588, 'positive')

        >>> analyze_text("This is terrible")
        (-0.5423, 'negative')

        >>> analyze_text("This is okay")
        (0.0, 'neutral')
    """
    # Handle empty or very short text
    if not text or len(text.strip()) < 3:
        return (0.0, 'neutral')

    # If VADER is not available, return neutral
    if not VADER_AVAILABLE:
        logger.warning("VADER not available, returning neutral sentiment")
        return (0.0, 'neutral')

    try:
        # Initialize VADER analyzer
        analyzer = SentimentIntensityAnalyzer()

        # Get sentiment scores
        scores = analyzer.polarity_scores(text)
        compound_score = scores['compound']

        # Categorize based on compound score
        # VADER recommends thresholds: >= 0.05 positive, <= -0.05 negative
        if compound_score >= 0.05:
            category = 'positive'
        elif compound_score <= -0.05:
            category = 'negative'
        else:
            category = 'neutral'

        logger.debug(f"Sentiment analysis: score={compound_score:.4f}, category={category}, text_length={len(text)}")

        return (round(compound_score, 4), category)

    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}", exc_info=True)
        return (0.0, 'neutral')


def get_sentiment_label_az(category: str) -> str:
    """
    Get Azerbaijani label for sentiment category.

    Args:
        category: Sentiment category ('positive', 'negative', 'neutral')

    Returns:
        Azerbaijani label for the category
    """
    labels = {
        'positive': 'Pozitiv',
        'negative': 'Neqativ',
        'neutral': 'Neytral'
    }
    return labels.get(category, 'Neytral')


def get_sentiment_color(category: str) -> str:
    """
    Get Bootstrap color class for sentiment category.

    Args:
        category: Sentiment category ('positive', 'negative', 'neutral')

    Returns:
        Bootstrap color class
    """
    colors = {
        'positive': 'success',
        'negative': 'danger',
        'neutral': 'secondary'
    }
    return colors.get(category, 'secondary')
