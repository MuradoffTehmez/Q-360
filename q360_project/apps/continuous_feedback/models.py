"""
Continuous Feedback models for quick feedback, feedback bank, and public recognition.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import User


class QuickFeedback(models.Model):
    """
    Quick feedback that users can send to each other anytime.
    Supports both recognition (thanks) and improvement suggestions.
    Enhanced with multi-source 360-degree feedback capabilities.
    """
    FEEDBACK_TYPE_CHOICES = [
        ('recognition', 'Təşəkkür / Recognition'),
        ('improvement', 'Təklif / Improvement'),
        ('general', 'Ümumi'),
        ('behavioral', 'Davranış'),
        ('skill', 'Bacarıq'),
        ('leadership', 'Liderlik'),
    ]

    VISIBILITY_CHOICES = [
        ('private', 'Şəxsi'),
        ('public', 'İctimai'),
        ('team', 'Komanda'),
    ]

    # 360-degree feedback source types
    SOURCE_RELATIONSHIP_CHOICES = [
        ('self', 'Özünüdəyərləndirmə'),
        ('manager', 'Menecer'),
        ('peer', 'Həmkar'),
        ('direct_report', 'Tabeli'),
        ('cross_functional', 'Kross-funksional'),
        ('customer', 'Müştəri'),
        ('external', 'Xarici'),
    ]

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_feedbacks',
        verbose_name='Göndərən'
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_feedbacks',
        verbose_name='Alan'
    )

    feedback_type = models.CharField(
        max_length=20,
        choices=FEEDBACK_TYPE_CHOICES,
        verbose_name='Rəy Tipi'
    )
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='private',
        verbose_name='Görünürlük'
    )

    # 360-degree feedback enhancement
    source_relationship = models.CharField(
        max_length=20,
        choices=SOURCE_RELATIONSHIP_CHOICES,
        default='peer',
        verbose_name='Mənbə Əlaqəsi',
        help_text='360-dərəcə feedback üçün göndərənin alıcı ilə əlaqəsi'
    )

    # Multi-source feedback collection
    is_part_of_360 = models.BooleanField(
        default=False,
        verbose_name='360° Feedback Parçası',
        help_text='Bu feedback 360-dərəcə qiymətləndirmənin bir hissəsidir'
    )
    feedback_campaign = models.ForeignKey(
        'evaluations.EvaluationCampaign',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='continuous_feedbacks',
        verbose_name='Qiymətləndirmə Kampaniyası'
    )

    title = models.CharField(max_length=200, verbose_name='Başlıq')
    message = models.TextField(verbose_name='Mesaj')

    # Optional: Related to a specific competency or skill
    related_competency = models.ForeignKey(
        'competencies.Competency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_feedbacks',
        verbose_name='Əlaqəli Kompetensiya'
    )

    # Optional: Related to a specific project or task
    context = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Kontekst',
        help_text='Məsələn: Layihə adı, tapşırıq və ya hadisə'
    )

    # Ratings (optional, for structured feedback)
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Qiymət (1-5)',
        help_text='1=Çox zəif, 5=Əla'
    )

    is_anonymous = models.BooleanField(
        default=False,
        verbose_name='Anonim',
        help_text='Alan şəxs göndərəni görməyəcək'
    )

    # Anonymous feedback processing
    anonymous_hash = models.CharField(
        max_length=64,
        blank=True,
        verbose_name='Anonim Hash',
        help_text='Anonim feedbackin təkrarlanmasını yoxlamaq üçün hash'
    )

    # Response and acknowledgment
    is_read = models.BooleanField(default=False, verbose_name='Oxundu')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='Oxunma Vaxtı')

    recipient_response = models.TextField(blank=True, verbose_name='Alanın Cavabı')
    responded_at = models.DateTimeField(null=True, blank=True, verbose_name='Cavab Verilmə Vaxtı')

    # Tracking
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma Vaxtı')
    updated_at = models.DateTimeField(auto_now=True)

    # Flag for inappropriate content
    is_flagged = models.BooleanField(default=False, verbose_name='Bildirildi')
    flagged_reason = models.TextField(blank=True, verbose_name='Bildirmə Səbəbi')

    class Meta:
        verbose_name = 'Tez Rəy'
        verbose_name_plural = 'Tez Rəylər'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['sender', '-created_at']),
            models.Index(fields=['feedback_type', 'visibility']),
        ]

    def __str__(self):
        sender_name = "Anonim" if self.is_anonymous else self.sender.get_full_name()
        return f"{sender_name} → {self.recipient.get_full_name()}: {self.title}"

    def save(self, *args, **kwargs):
        """Override save to handle anonymous feedback hashing."""
        if self.is_anonymous and not self.anonymous_hash:
            import hashlib
            from django.utils import timezone
            # Create hash from sender, recipient, timestamp
            hash_string = f"{self.sender_id}:{self.recipient_id}:{timezone.now().isoformat()}"
            self.anonymous_hash = hashlib.sha256(hash_string.encode()).hexdigest()
        super().save(*args, **kwargs)

    def get_sender_display(self):
        """Get sender name respecting anonymity settings."""
        if self.is_anonymous:
            return "Anonim"
        return self.sender.get_full_name()

    def get_feedback_sources_summary(self):
        """Get summary of 360-degree feedback sources for recipient."""
        if not self.is_part_of_360:
            return None

        from django.db.models import Count
        sources = QuickFeedback.objects.filter(
            recipient=self.recipient,
            is_part_of_360=True,
            feedback_campaign=self.feedback_campaign
        ).values('source_relationship').annotate(
            count=Count('id')
        )
        return dict(sources.values_list('source_relationship', 'count'))


class FeedbackBank(models.Model):
    """
    Aggregated feedback repository for each user.
    Stores all collected feedback while maintaining anonymity where needed.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='feedback_bank',
        verbose_name='İstifadəçi'
    )

    total_feedbacks_received = models.IntegerField(default=0, verbose_name='Alınan Ümumi Rəylər')
    total_recognitions = models.IntegerField(default=0, verbose_name='Alınan Təşəkkürlər')
    total_improvements = models.IntegerField(default=0, verbose_name='Alınan Təkliflər')

    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='Orta Qiymət'
    )

    # Top competencies mentioned in feedback
    top_strengths = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Ən Çox Qeyd Edilən Güclü Tərəflər',
        help_text='Rəylərdə ən çox qeyd edilən kompetensiyalar'
    )

    top_improvement_areas = models.JSONField(
        default=list,
        blank=True,
        verbose_name='İnkişaf Sahələri',
        help_text='Təkmilləşdirmə üçün ən çox qeyd edilən sahələr'
    )

    # Sentiment analysis (optional, for future ML integration)
    positive_sentiment_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Müsbət Sentiment Balı'
    )

    last_feedback_date = models.DateTimeField(null=True, blank=True, verbose_name='Son Rəy Tarixi')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='Son Yenilənmə')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Rəy Bankı'
        verbose_name_plural = 'Rəy Bankları'

    def __str__(self):
        return f"Rəy Bankı: {self.user.get_full_name()} ({self.total_feedbacks_received} rəy)"

    def update_stats(self):
        """Update feedback bank statistics."""
        feedbacks = self.user.received_feedbacks.all()

        self.total_feedbacks_received = feedbacks.count()
        self.total_recognitions = feedbacks.filter(feedback_type='recognition').count()
        self.total_improvements = feedbacks.filter(feedback_type='improvement').count()

        # Calculate average rating
        rated_feedbacks = feedbacks.filter(rating__isnull=False)
        if rated_feedbacks.exists():
            total_rating = sum(f.rating for f in rated_feedbacks)
            self.average_rating = total_rating / rated_feedbacks.count()

        # Update last feedback date
        latest_feedback = feedbacks.order_by('-created_at').first()
        if latest_feedback:
            self.last_feedback_date = latest_feedback.created_at

        self.save()


class PublicRecognition(models.Model):
    """
    Public recognition feed - showcases appreciation messages for all to see.
    Boosts morale and creates a positive culture.
    """
    feedback = models.OneToOneField(
        QuickFeedback,
        on_delete=models.CASCADE,
        limit_choices_to={'feedback_type': 'recognition', 'visibility': 'public'},
        related_name='public_recognition',
        verbose_name='Rəy'
    )

    # Engagement metrics
    likes_count = models.IntegerField(default=0, verbose_name='Bəyənmə Sayı')
    comments_count = models.IntegerField(default=0, verbose_name='Şərh Sayı')
    views_count = models.IntegerField(default=0, verbose_name='Baxış Sayı')

    # Featured/pinned recognition
    is_featured = models.BooleanField(default=False, verbose_name='Xüsusi Seçilmiş')
    featured_until = models.DateTimeField(null=True, blank=True, verbose_name='Seçilmə Müddəti')

    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Dərc Tarixi')

    class Meta:
        verbose_name = 'İctimai Təqdir'
        verbose_name_plural = 'İctimai Təqdirlər'
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['is_featured', '-published_at']),
        ]

    def __str__(self):
        return f"İctimai Təqdir: {self.feedback.title}"


class RecognitionLike(models.Model):
    """
    Likes on public recognition posts.
    """
    recognition = models.ForeignKey(
        PublicRecognition,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Təqdir'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recognition_likes',
        verbose_name='İstifadəçi'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Təqdir Bəyənməsi'
        verbose_name_plural = 'Təqdir Bəyənmələri'
        unique_together = ['recognition', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} bəyəndi"


class RecognitionComment(models.Model):
    """
    Comments on public recognition posts.
    """
    recognition = models.ForeignKey(
        PublicRecognition,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Təqdir'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recognition_comments',
        verbose_name='İstifadəçi'
    )

    comment = models.TextField(verbose_name='Şərh')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Təqdir Şərhi'
        verbose_name_plural = 'Təqdir Şərhləri'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.get_full_name()}: {self.comment[:50]}"


class FeedbackTag(models.Model):
    """
    Tags for categorizing feedback (e.g., 'teamwork', 'communication', 'leadership').
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='Ad')
    description = models.TextField(blank=True, verbose_name='Təsvir')
    icon = models.CharField(max_length=50, blank=True, verbose_name='İkon', help_text='Font Awesome icon class')

    is_active = models.BooleanField(default=True, verbose_name='Aktivdir')
    usage_count = models.IntegerField(default=0, verbose_name='İstifadə Sayı')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Rəy Etiketi'
        verbose_name_plural = 'Rəy Etiketləri'
        ordering = ['name']

    def __str__(self):
        return self.name


# Add ManyToMany relationship to QuickFeedback
QuickFeedback.add_to_class(
    'tags',
    models.ManyToManyField(
        FeedbackTag,
        blank=True,
        related_name='feedbacks',
        verbose_name='Etiketlər'
    )
)
