from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.evaluations.models import Response


class SentimentFeedback(models.Model):
    """
    Model for storing sentiment analysis feedback.
    """
    SENTIMENT_CHOICES = [
        ('positive', _('Positive')),
        ('neutral', _('Neutral')),
        ('negative', _('Negative')),
    ]
    
    feedback_text = models.TextField(verbose_name=_("Feedback Text"))
    sentiment_label = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, verbose_name=_("Sentiment Label"))
    sentiment_score = models.FloatField(verbose_name=_("Sentiment Score"))
    confidence = models.FloatField(verbose_name=_("Confidence Score"))
    
    # Related objects
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sentiment_feedback', verbose_name=_("User"))
    evaluation_response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='sentiment_analysis', verbose_name=_("Evaluation Response"), null=True, blank=True)
    
    # Resolution tracking
    is_resolved = models.BooleanField(default=False, verbose_name=_("Is Resolved"))
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='resolved_feedback', verbose_name=_("Resolved By"), null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Resolved At"))
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        verbose_name = _("Sentiment Feedback")
        verbose_name_plural = _("Sentiment Feedback")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.sentiment_label} ({self.created_at.date()})"
    
    
class SentimentAnalysisSettings(models.Model):
    """
    Model for storing sentiment analysis settings.
    """
    # Analysis configuration
    enable_sentiment_analysis = models.BooleanField(default=True, verbose_name=_("Enable Sentiment Analysis"))
    min_confidence_threshold = models.FloatField(default=0.7, verbose_name=_("Minimum Confidence Threshold"))
    
    # Alert settings
    enable_negative_alerts = models.BooleanField(default=True, verbose_name=_("Enable Negative Sentiment Alerts"))
    negative_sentiment_threshold = models.FloatField(default=0.3, verbose_name=_("Negative Sentiment Threshold"))
    
    # Integration settings
    enable_slack_integration = models.BooleanField(default=False, verbose_name=_("Enable Slack Integration"))
    slack_webhook_url = models.URLField(blank=True, null=True, verbose_name=_("Slack Webhook URL"))
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        verbose_name = _("Sentiment Analysis Settings")
        verbose_name_plural = _("Sentiment Analysis Settings")
    
    def __str__(self):
        return _("Sentiment Analysis Settings")