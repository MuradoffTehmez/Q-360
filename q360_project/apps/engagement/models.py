from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

User = get_user_model()


class PulseSurvey(models.Model):
    """Qısa və tez-tez aparılan sorğular üçün model"""

    SURVEY_TYPE_CHOICES = [
        ('weekly', _('Weekly Check-in')),
        ('monthly', _('Monthly Pulse')),
        ('quarterly', _('Quarterly Review')),
        ('event', _('Event Feedback')),
        ('custom', _('Custom Survey')),
    ]

    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('active', _('Active')),
        ('closed', _('Closed')),
        ('archived', _('Archived')),
    ]

    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    survey_type = models.CharField(_('Survey Type'), max_length=20, choices=SURVEY_TYPE_CHOICES, default='custom')
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='draft')

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_surveys')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    start_date = models.DateTimeField(_('Start Date'))
    end_date = models.DateTimeField(_('End Date'))

    is_anonymous = models.BooleanField(_('Anonymous Survey'), default=False)
    is_mandatory = models.BooleanField(_('Mandatory'), default=False)

    target_departments = models.ManyToManyField('departments.Department', blank=True, related_name='pulse_surveys')
    target_users = models.ManyToManyField(User, blank=True, related_name='targeted_surveys')

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Pulse Survey')
        verbose_name_plural = _('Pulse Surveys')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def response_count(self):
        return self.responses.count()

    @property
    def completion_rate(self):
        if self.target_users.count() > 0:
            return (self.response_count / self.target_users.count()) * 100
        return 0


class SurveyQuestion(models.Model):
    """Sorğu sualları"""

    QUESTION_TYPE_CHOICES = [
        ('rating', _('Rating (1-5)')),
        ('nps', _('NPS (0-10)')),
        ('text', _('Open Text')),
        ('yes_no', _('Yes/No')),
        ('multiple_choice', _('Multiple Choice')),
        ('emoji', _('Emoji Rating')),
    ]

    survey = models.ForeignKey(PulseSurvey, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField(_('Question Text'))
    question_type = models.CharField(_('Question Type'), max_length=20, choices=QUESTION_TYPE_CHOICES)
    order = models.IntegerField(_('Order'), default=0)
    is_required = models.BooleanField(_('Required'), default=True)

    # Multiple choice options (JSON format)
    options = models.JSONField(_('Options'), blank=True, null=True)

    class Meta:
        verbose_name = _('Survey Question')
        verbose_name_plural = _('Survey Questions')
        ordering = ['survey', 'order']

    def __str__(self):
        return f"{self.survey.title} - {self.question_text[:50]}"


class SurveyResponse(models.Model):
    """Sorğu cavabları"""

    survey = models.ForeignKey(PulseSurvey, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='survey_responses')

    # Response data
    rating_value = models.IntegerField(_('Rating Value'), null=True, blank=True)
    text_value = models.TextField(_('Text Value'), blank=True)
    boolean_value = models.BooleanField(_('Boolean Value'), null=True, blank=True)

    submitted_at = models.DateTimeField(_('Submitted At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Survey Response')
        verbose_name_plural = _('Survey Responses')
        unique_together = ['survey', 'question', 'user']

    def __str__(self):
        return f"{self.survey.title} - Response"


class EngagementScore(models.Model):
    """NPS və ümumi engagement skoru üçün model"""

    SCORE_TYPE_CHOICES = [
        ('nps', _('Net Promoter Score')),
        ('esat', _('Employee Satisfaction')),
        ('engagement', _('Overall Engagement')),
        ('wellbeing', _('Well-being Score')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='engagement_scores')
    score_type = models.CharField(_('Score Type'), max_length=20, choices=SCORE_TYPE_CHOICES)
    score_value = models.IntegerField(_('Score Value'), validators=[MinValueValidator(0), MaxValueValidator(100)])

    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)

    calculated_at = models.DateTimeField(_('Calculated At'), auto_now_add=True)
    period_start = models.DateField(_('Period Start'))
    period_end = models.DateField(_('Period End'))

    # NPS breakdown
    is_promoter = models.BooleanField(_('Promoter'), default=False)  # 9-10
    is_passive = models.BooleanField(_('Passive'), default=False)    # 7-8
    is_detractor = models.BooleanField(_('Detractor'), default=False)  # 0-6

    notes = models.TextField(_('Notes'), blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Engagement Score')
        verbose_name_plural = _('Engagement Scores')
        ordering = ['-calculated_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.score_type}: {self.score_value}"


class Recognition(models.Model):
    """Təşəkkür və mükafatlar üçün model"""

    RECOGNITION_TYPE_CHOICES = [
        ('thanks', _('Thank You')),
        ('kudos', _('Kudos')),
        ('award', _('Award')),
        ('milestone', _('Milestone')),
        ('achievement', _('Achievement')),
    ]

    given_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_recognitions')
    given_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_recognitions')

    recognition_type = models.CharField(_('Type'), max_length=20, choices=RECOGNITION_TYPE_CHOICES)
    title = models.CharField(_('Title'), max_length=200)
    message = models.TextField(_('Message'))

    is_public = models.BooleanField(_('Public'), default=True)

    badge = models.ForeignKey('GamificationBadge', on_delete=models.SET_NULL, null=True, blank=True)
    points = models.IntegerField(_('Points'), default=10)

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    # Reactions
    likes_count = models.IntegerField(_('Likes'), default=0)
    liked_by = models.ManyToManyField(User, blank=True, related_name='liked_recognitions')

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Recognition')
        verbose_name_plural = _('Recognitions')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.given_by.get_full_name()} → {self.given_to.get_full_name()}: {self.title}"


class AnonymousFeedback(models.Model):
    """Anonim təkliflər və şikayətlər üçün model"""

    CATEGORY_CHOICES = [
        ('suggestion', _('Suggestion')),
        ('complaint', _('Complaint')),
        ('concern', _('Concern')),
        ('praise', _('Praise')),
        ('question', _('Question')),
        ('other', _('Other')),
    ]

    STATUS_CHOICES = [
        ('new', _('New')),
        ('reviewing', _('Under Review')),
        ('in_progress', _('In Progress')),
        ('resolved', _('Resolved')),
        ('closed', _('Closed')),
    ]

    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]

    # Anonymous identifier
    anonymous_id = models.CharField(_('Anonymous ID'), max_length=50, unique=True)

    category = models.CharField(_('Category'), max_length=20, choices=CATEGORY_CHOICES)
    subject = models.CharField(_('Subject'), max_length=200)
    message = models.TextField(_('Message'))

    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(_('Priority'), max_length=20, choices=PRIORITY_CHOICES, default='medium')

    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)

    submitted_at = models.DateTimeField(_('Submitted At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    # Admin response
    response = models.TextField(_('Response'), blank=True)
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_responses')
    responded_at = models.DateTimeField(_('Responded At'), null=True, blank=True)

    # Sentiment analysis
    sentiment_score = models.FloatField(_('Sentiment Score'), null=True, blank=True)
    sentiment_label = models.CharField(_('Sentiment'), max_length=20, blank=True)  # positive, negative, neutral

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Anonymous Feedback')
        verbose_name_plural = _('Anonymous Feedbacks')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.category} - {self.subject}"


class SentimentAnalysis(models.Model):
    """Emosional analiz üçün model"""

    SOURCE_TYPE_CHOICES = [
        ('survey', _('Survey Response')),
        ('feedback', _('Anonymous Feedback')),
        ('recognition', _('Recognition')),
        ('comment', _('Comment')),
    ]

    SENTIMENT_CHOICES = [
        ('very_positive', _('Very Positive')),
        ('positive', _('Positive')),
        ('neutral', _('Neutral')),
        ('negative', _('Negative')),
        ('very_negative', _('Very Negative')),
    ]

    source_type = models.CharField(_('Source Type'), max_length=20, choices=SOURCE_TYPE_CHOICES)
    source_id = models.IntegerField(_('Source ID'))

    text_content = models.TextField(_('Text Content'))

    sentiment = models.CharField(_('Sentiment'), max_length=20, choices=SENTIMENT_CHOICES)
    sentiment_score = models.FloatField(_('Sentiment Score'), validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)])
    confidence = models.FloatField(_('Confidence'), validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    # Emotion detection
    emotions = models.JSONField(_('Emotions'), blank=True, null=True)  # {'joy': 0.8, 'sadness': 0.1, etc.}

    # Keywords and topics
    keywords = models.JSONField(_('Keywords'), blank=True, null=True)
    topics = models.JSONField(_('Topics'), blank=True, null=True)

    analyzed_at = models.DateTimeField(_('Analyzed At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Sentiment Analysis')
        verbose_name_plural = _('Sentiment Analyses')
        ordering = ['-analyzed_at']

    def __str__(self):
        return f"{self.source_type} - {self.sentiment}"


class GamificationBadge(models.Model):
    """Badge və xal sistemi üçün model"""

    BADGE_CATEGORY_CHOICES = [
        ('performance', _('Performance')),
        ('collaboration', _('Collaboration')),
        ('innovation', _('Innovation')),
        ('leadership', _('Leadership')),
        ('learning', _('Learning & Development')),
        ('milestone', _('Milestone')),
        ('special', _('Special Achievement')),
    ]

    name = models.CharField(_('Badge Name'), max_length=100)
    description = models.TextField(_('Description'))
    category = models.CharField(_('Category'), max_length=20, choices=BADGE_CATEGORY_CHOICES)

    icon = models.CharField(_('Icon'), max_length=50, default='🏆')  # Emoji or icon class
    color = models.CharField(_('Color'), max_length=20, default='#FFD700')

    points_value = models.IntegerField(_('Points Value'), default=50)

    # Criteria for earning
    criteria = models.JSONField(_('Earning Criteria'), blank=True, null=True)

    is_active = models.BooleanField(_('Active'), default=True)
    is_rare = models.BooleanField(_('Rare Badge'), default=False)

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Gamification Badge')
        verbose_name_plural = _('Gamification Badges')
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserBadge(models.Model):
    """İstifadəçilərə verilmiş badge-lər"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(GamificationBadge, on_delete=models.CASCADE, related_name='awarded_to')

    earned_at = models.DateTimeField(_('Earned At'), auto_now_add=True)
    awarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='awarded_badges')

    reason = models.TextField(_('Reason'), blank=True)

    is_displayed = models.BooleanField(_('Display on Profile'), default=True)

    class Meta:
        verbose_name = _('User Badge')
        verbose_name_plural = _('User Badges')
        unique_together = ['user', 'badge', 'earned_at']
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.badge.name}"


class UserPoints(models.Model):
    """İstifadəçi xal sistemi"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='points_profile')

    total_points = models.IntegerField(_('Total Points'), default=0)
    current_level = models.IntegerField(_('Current Level'), default=1)

    # Points breakdown
    performance_points = models.IntegerField(_('Performance Points'), default=0)
    collaboration_points = models.IntegerField(_('Collaboration Points'), default=0)
    innovation_points = models.IntegerField(_('Innovation Points'), default=0)
    learning_points = models.IntegerField(_('Learning Points'), default=0)

    rank = models.IntegerField(_('Rank'), default=0)  # Overall rank in company

    last_updated = models.DateTimeField(_('Last Updated'), auto_now=True)

    class Meta:
        verbose_name = _('User Points')
        verbose_name_plural = _('User Points')
        ordering = ['-total_points']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.total_points} points (Level {self.current_level})"

    def add_points(self, points, category='performance'):
        """Xal əlavə et"""
        self.total_points += points

        if category == 'performance':
            self.performance_points += points
        elif category == 'collaboration':
            self.collaboration_points += points
        elif category == 'innovation':
            self.innovation_points += points
        elif category == 'learning':
            self.learning_points += points

        # Calculate new level
        self.current_level = (self.total_points // 1000) + 1

        self.save()


class PointsTransaction(models.Model):
    """Xal əməliyyatları tarixçəsi"""

    TRANSACTION_TYPE_CHOICES = [
        ('earned', _('Earned')),
        ('awarded', _('Awarded')),
        ('deducted', _('Deducted')),
        ('bonus', _('Bonus')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points_transactions')
    transaction_type = models.CharField(_('Type'), max_length=20, choices=TRANSACTION_TYPE_CHOICES)

    points = models.IntegerField(_('Points'))
    reason = models.CharField(_('Reason'), max_length=200)
    description = models.TextField(_('Description'), blank=True)

    # Reference to source
    source_type = models.CharField(_('Source Type'), max_length=50, blank=True)
    source_id = models.IntegerField(_('Source ID'), null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_transactions')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Points Transaction')
        verbose_name_plural = _('Points Transactions')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.transaction_type}: {self.points} points"
