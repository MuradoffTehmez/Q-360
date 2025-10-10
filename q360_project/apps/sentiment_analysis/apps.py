"""App configuration for sentiment_analysis."""
from django.apps import AppConfig


class SentimentAnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sentiment_analysis'
    verbose_name = 'Sentiment Analizi'
