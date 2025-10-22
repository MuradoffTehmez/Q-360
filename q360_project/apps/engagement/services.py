"""
Engagement Services - AI Sentiment Analysis və Digər Xidmətlər
"""
from typing import Dict, Any
import re


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    AI ilə sentiment analizi

    Bu funksiya mətni analiz edərək sentiment (emosional ton) təyin edir.
    Hazırda sadə keyword-based yanaşma istifadə edilir.
    Gələcəkdə transformers kitabxanası ilə daha güclü AI modellər əlavə edilə bilər.

    Args:
        text (str): Analiz ediləcək mətn

    Returns:
        Dict[str, Any]: {
            'score': float (-1.0 to 1.0),
            'label': str (very_positive, positive, neutral, negative, very_negative),
            'confidence': float (0.0 to 1.0)
        }
    """
    if not text:
        return {
            'score': 0.0,
            'label': 'neutral',
            'confidence': 0.0
        }

    # Normalize text
    text_lower = text.lower()

    # Define sentiment keywords
    positive_keywords = [
        'excellent', 'great', 'good', 'amazing', 'wonderful', 'fantastic',
        'love', 'like', 'enjoy', 'happy', 'satisfied', 'perfect',
        'best', 'awesome', 'brilliant', 'outstanding', 'superb',
        'gözəl', 'əla', 'mükəmməl', 'xoş', 'sevincliyəm', 'razıyam',
        'çox yaxşı', 'super', 'əcəmi', 'əladır'
    ]

    negative_keywords = [
        'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst',
        'hate', 'dislike', 'disappointed', 'unhappy', 'unsatisfied',
        'never', 'problem', 'issue', 'concern', 'complaint',
        'pis', 'çox pis', 'dəhşətli', 'narazıyam', 'bəyənmədim',
        'problem', 'şikayət', 'narahat', 'kədərliyəm'
    ]

    # Count sentiment words
    positive_count = sum(1 for word in positive_keywords if word in text_lower)
    negative_count = sum(1 for word in negative_keywords if word in text_lower)

    # Calculate sentiment score
    total_sentiment_words = positive_count + negative_count

    if total_sentiment_words == 0:
        score = 0.0
        label = 'neutral'
        confidence = 0.5
    else:
        score = (positive_count - negative_count) / (total_sentiment_words + 1)
        confidence = min(total_sentiment_words / 10, 1.0)  # Max confidence at 10 sentiment words

        if score >= 0.5:
            label = 'very_positive'
        elif score >= 0.1:
            label = 'positive'
        elif score <= -0.5:
            label = 'very_negative'
        elif score <= -0.1:
            label = 'negative'
        else:
            label = 'neutral'

    return {
        'score': round(score, 2),
        'label': label,
        'confidence': round(confidence, 2)
    }


def analyze_sentiment_with_ai(text: str) -> Dict[str, Any]:
    """
    Transformers kitabxanası ilə AI sentiment analysis
    (Opsional - lazım olduqda aktiv edin)

    Requirements:
        pip install transformers torch

    """
    try:
        from transformers import pipeline

        # Initialize sentiment analysis pipeline
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )

        result = sentiment_pipeline(text[:512])[0]  # Limit to 512 chars

        # Convert label to our format
        label_mapping = {
            '1 star': 'very_negative',
            '2 stars': 'negative',
            '3 stars': 'neutral',
            '4 stars': 'positive',
            '5 stars': 'very_positive'
        }

        label = label_mapping.get(result['label'], 'neutral')

        # Convert score to -1 to 1 range
        stars = int(result['label'].split()[0])
        score = (stars - 3) / 2  # Maps 1-5 to -1 to 1

        return {
            'score': round(score, 2),
            'label': label,
            'confidence': round(result['score'], 2)
        }

    except ImportError:
        # Fallback to keyword-based analysis if transformers not installed
        return analyze_sentiment(text)

    except Exception as e:
        print(f"Error in AI sentiment analysis: {e}")
        return analyze_sentiment(text)


def extract_keywords(text: str, max_keywords: int = 10) -> list:
    """
    Mətndən açar sözləri çıxarır

    Args:
        text (str): Mətn
        max_keywords (int): Maksimum açar söz sayı

    Returns:
        list: Açar sözlər siyahısı
    """
    # Remove punctuation and convert to lowercase
    text_clean = re.sub(r'[^\w\s]', '', text.lower())

    # Common stop words (expand this list)
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'should', 'could', 'may', 'might', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your',
        've', 'bir', 'və', 'ki', 'bu', 'o', 'mən', 'sən', 'biz', 'siz'
    }

    # Split into words and filter
    words = text_clean.split()
    keywords = [word for word in words if word not in stop_words and len(word) > 2]

    # Count frequency
    from collections import Counter
    word_counts = Counter(keywords)

    # Return top keywords
    return [word for word, count in word_counts.most_common(max_keywords)]


def detect_emotions(text: str) -> Dict[str, float]:
    """
    Mətndə emosiyaları aşkar edir

    Returns:
        Dict[str, float]: Emosiyalar və onların intensivliyi (0-1)
    """
    emotions = {
        'joy': 0.0,
        'sadness': 0.0,
        'anger': 0.0,
        'fear': 0.0,
        'surprise': 0.0,
        'trust': 0.0
    }

    text_lower = text.lower()

    # Joy indicators
    joy_words = ['happy', 'joy', 'excited', 'glad', 'pleased', 'sevinc', 'xoşbəxtlik', 'şad']
    emotions['joy'] = sum(0.2 for word in joy_words if word in text_lower)

    # Sadness indicators
    sadness_words = ['sad', 'unhappy', 'disappointed', 'depressed', 'kədər', 'narahat', 'üzgün']
    emotions['sadness'] = sum(0.2 for word in sadness_words if word in text_lower)

    # Anger indicators
    anger_words = ['angry', 'mad', 'furious', 'annoyed', 'qəzəb', 'hirslənmək', 'əsəbi']
    emotions['anger'] = sum(0.2 for word in anger_words if word in text_lower)

    # Fear indicators
    fear_words = ['afraid', 'scared', 'worried', 'anxious', 'qorxu', 'narahatçılıq']
    emotions['fear'] = sum(0.2 for word in fear_words if word in text_lower)

    # Surprise indicators
    surprise_words = ['surprised', 'shocked', 'amazed', 'astonished', 'təəccüb', 'heyrət']
    emotions['surprise'] = sum(0.2 for word in surprise_words if word in text_lower)

    # Trust indicators
    trust_words = ['trust', 'believe', 'confident', 'sure', 'etibar', 'inanıram', 'əminəm']
    emotions['trust'] = sum(0.2 for word in trust_words if word in text_lower)

    # Normalize to 0-1 range
    for emotion in emotions:
        emotions[emotion] = min(emotions[emotion], 1.0)

    return emotions


def calculate_nps(score: int) -> str:
    """
    NPS (Net Promoter Score) kateqoriyasını təyin edir

    Args:
        score (int): 0-10 arası bal

    Returns:
        str: 'promoter', 'passive', or 'detractor'
    """
    if score >= 9:
        return 'promoter'
    elif score >= 7:
        return 'passive'
    else:
        return 'detractor'


def get_engagement_level(score: int) -> str:
    """
    Engagement səviyyəsini təyin edir

    Args:
        score (int): 0-100 arası bal

    Returns:
        str: Engagement səviyyəsi
    """
    if score >= 80:
        return 'Highly Engaged'
    elif score >= 60:
        return 'Engaged'
    elif score >= 40:
        return 'Moderately Engaged'
    elif score >= 20:
        return 'Disengaged'
    else:
        return 'Highly Disengaged'


def calculate_team_engagement(department_id: int) -> Dict[str, Any]:
    """
    Komanda üçün ümumi engagement hesablayır

    Args:
        department_id (int): Şöbə ID

    Returns:
        Dict[str, Any]: Komanda engagement statistikaları
    """
    from .models import EngagementScore
    from django.db.models import Avg, Count
    from django.utils import timezone
    from datetime import timedelta

    thirty_days_ago = timezone.now() - timedelta(days=30)

    scores = EngagementScore.objects.filter(
        department_id=department_id,
        calculated_at__gte=thirty_days_ago
    )

    stats = scores.aggregate(
        avg_score=Avg('score_value'),
        total_responses=Count('id')
    )

    # NPS breakdown
    nps_scores = scores.filter(score_type='nps')
    promoters = nps_scores.filter(is_promoter=True).count()
    passives = nps_scores.filter(is_passive=True).count()
    detractors = nps_scores.filter(is_detractor=True).count()
    total_nps = promoters + passives + detractors

    if total_nps > 0:
        nps = ((promoters - detractors) / total_nps) * 100
    else:
        nps = 0

    return {
        'average_score': round(stats['avg_score'] or 0, 2),
        'total_responses': stats['total_responses'],
        'nps': round(nps, 2),
        'promoters_count': promoters,
        'passives_count': passives,
        'detractors_count': detractors,
        'engagement_level': get_engagement_level(stats['avg_score'] or 0)
    }
