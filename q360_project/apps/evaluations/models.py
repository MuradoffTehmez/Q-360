"""
Models for evaluations app - 360-degree evaluation system.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from apps.accounts.models import User


class EvaluationCampaign(models.Model):
    """
    Represents a 360-degree evaluation campaign period.
    Defines when and how evaluations are conducted.
    """

    STATUS_CHOICES = [
        ('draft', 'Qaralama'),
        ('active', 'Aktiv'),
        ('completed', 'Tamamlanmış'),
        ('archived', 'Arxivlənmiş'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name=_('Kampaniya Adı')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )

    # Campaign period
    start_date = models.DateField(
        verbose_name=_('Başlama Tarixi')
    )
    end_date = models.DateField(
        verbose_name=_('Bitmə Tarixi')
    )

    # Campaign settings
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('Status')
    )
    is_anonymous = models.BooleanField(
        default=True,
        verbose_name=_('Anonim Qiymətləndirmə'),
        help_text=_('Qiymətləndirənin kimliyini gizlət')
    )
    allow_self_evaluation = models.BooleanField(
        default=True,
        verbose_name=_('Özünüdəyərləndirməyə İcazə Ver')
    )

    # Target audience
    target_departments = models.ManyToManyField(
        'departments.Department',
        blank=True,
        related_name='evaluation_campaigns',
        verbose_name=_('Hədəf Şöbələr')
    )
    target_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='target_campaigns',
        verbose_name=_('Hədəf İstifadəçilər')
    )

    # Created by
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_campaigns',
        verbose_name=_('Yaradan')
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Qiymətləndirmə Kampaniyası')
        verbose_name_plural = _('Qiymətləndirmə Kampaniyaları')
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['end_date']),
        ]

    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"

    def is_active(self):
        """Check if campaign is currently active."""
        from datetime import date
        today = date.today()
        return (
            self.status == 'active' and
            self.start_date <= today <= self.end_date
        )

    def get_completion_rate(self):
        """Calculate completion rate of the campaign."""
        total_assignments = self.assignments.count()
        if total_assignments == 0:
            return 0
        completed = self.assignments.filter(status='completed').count()
        return (completed / total_assignments) * 100


class QuestionCategory(models.Model):
    """
    Categories for organizing evaluation questions.
    E.g., Leadership, Communication, Technical Skills, etc.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Kateqoriya Adı')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Sıra')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Sual Kateqoriyası')
        verbose_name_plural = _('Sual Kateqoriyaları')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Evaluation questions for 360-degree assessment.
    """

    QUESTION_TYPE_CHOICES = [
        ('scale', 'Bal Skalası (1-5)'),
        ('boolean', 'Bəli/Xeyr'),
        ('text', 'Açıq Cavab'),
    ]

    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('Kateqoriya')
    )
    text = models.TextField(
        verbose_name=_('Sual Mətni')
    )
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default='scale',
        verbose_name=_('Sual Növü')
    )
    max_score = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_('Maksimum Bal')
    )
    is_required = models.BooleanField(
        default=True,
        verbose_name=_('Məcburi')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Sıra')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Sual')
        verbose_name_plural = _('Suallar')
        ordering = ['category', 'order']

    def __str__(self):
        return f"{self.category.name}: {self.text[:50]}..."


class CampaignQuestion(models.Model):
    """
    Links questions to specific campaigns.
    Allows different question sets for different campaigns.
    """

    campaign = models.ForeignKey(
        EvaluationCampaign,
        on_delete=models.CASCADE,
        related_name='campaign_questions',
        verbose_name=_('Kampaniya')
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='campaign_uses',
        verbose_name=_('Sual')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Sıra')
    )

    class Meta:
        verbose_name = _('Kampaniya Sualı')
        verbose_name_plural = _('Kampaniya Sualları')
        unique_together = [['campaign', 'question']]
        ordering = ['order']

    def __str__(self):
        return f"{self.campaign.title} - {self.question.text[:30]}"


class EvaluationAssignment(models.Model):
    """
    Represents who evaluates whom in a campaign.
    The core of 360-degree evaluation relationships.
    """

    RELATIONSHIP_CHOICES = [
        ('self', 'Özünüdəyərləndirmə'),
        ('supervisor', 'Rəhbər Tərəfindən'),
        ('peer', 'Həmkar Tərəfindən'),
        ('subordinate', 'Tabelik Tərəfindən'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('in_progress', 'Davam edir'),
        ('completed', 'Tamamlanmış'),
        ('expired', 'Vaxtı Keçmiş'),
    ]

    campaign = models.ForeignKey(
        EvaluationCampaign,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_('Kampaniya')
    )
    evaluator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_evaluations',
        verbose_name=_('Qiymətləndirən')
    )
    evaluatee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_evaluations',
        verbose_name=_('Qiymətləndirilən')
    )
    relationship = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_CHOICES,
        verbose_name=_('Əlaqə Növü')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )

    # Progress tracking
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Başlanma Vaxtı')
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Tamamlanma Vaxtı')
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Qiymətləndirmə Tapşırığı')
        verbose_name_plural = _('Qiymətləndirmə Tapşırıqları')
        unique_together = [['campaign', 'evaluator', 'evaluatee']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['evaluator', 'status']),
            models.Index(fields=['evaluatee', 'campaign']),
        ]

    def __str__(self):
        return f"{self.evaluator.get_full_name()} → {self.evaluatee.get_full_name()}"

    def get_progress(self):
        """Calculate completion progress of this assignment."""
        total_questions = self.campaign.campaign_questions.count()
        if total_questions == 0:
            return 0
        answered = self.responses.count()
        return (answered / total_questions) * 100


class Response(models.Model):
    """
    Individual responses to evaluation questions.
    """

    assignment = models.ForeignKey(
        EvaluationAssignment,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_('Tapşırıq')
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_('Sual')
    )

    # Answer fields
    score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_('Bal')
    )
    boolean_answer = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('Bəli/Xeyr Cavabı')
    )
    text_answer = models.TextField(
        blank=True,
        verbose_name=_('Mətn Cavabı')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Şərh')
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cavab')
        verbose_name_plural = _('Cavablar')
        unique_together = [['assignment', 'question']]
        ordering = ['assignment', 'question__order']

    def __str__(self):
        return f"Response: {self.question.text[:30]}..."


class EvaluationResult(models.Model):
    """
    Aggregated results for an evaluatee in a campaign.
    Stores calculated averages and statistics.
    """

    campaign = models.ForeignKey(
        EvaluationCampaign,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name=_('Kampaniya')
    )
    evaluatee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='evaluation_results',
        verbose_name=_('Qiymətləndirilən')
    )

    # Aggregated scores
    overall_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Ümumi Bal')
    )
    self_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Özünüdəyərləndirmə Balı')
    )
    supervisor_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Rəhbər Balı')
    )
    peer_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Həmkar Balı')
    )
    subordinate_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Tabelik Balı')
    )

    # Statistics
    total_evaluators = models.IntegerField(
        default=0,
        verbose_name=_('Qiymətləndirən Sayı')
    )
    completion_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_('Tamamlanma Faizi')
    )

    # Status
    is_finalized = models.BooleanField(
        default=False,
        verbose_name=_('Yekunlaşdırılmış')
    )
    finalized_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Yekunlaşdırma Vaxtı')
    )

    # Metadata
    calculated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Hesablama Vaxtı')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Qiymətləndirmə Nəticəsi')
        verbose_name_plural = _('Qiymətləndirmə Nəticələri')
        unique_together = [['campaign', 'evaluatee']]
        ordering = ['-calculated_at']

    def __str__(self):
        return f"{self.evaluatee.get_full_name()} - {self.campaign.title}"

    def calculate_scores(self):
        """Calculate and update all scores for this result."""
        from django.db.models import Avg

        assignments = EvaluationAssignment.objects.filter(
            campaign=self.campaign,
            evaluatee=self.evaluatee,
            status='completed'
        )

        self.total_evaluators = assignments.count()

        # Calculate overall score
        all_scores = Response.objects.filter(
            assignment__in=assignments,
            score__isnull=False
        ).aggregate(avg_score=Avg('score'))
        self.overall_score = all_scores['avg_score']

        # Calculate scores by relationship
        for relationship, field in [
            ('self', 'self_score'),
            ('supervisor', 'supervisor_score'),
            ('peer', 'peer_score'),
            ('subordinate', 'subordinate_score'),
        ]:
            rel_assignments = assignments.filter(relationship=relationship)
            if rel_assignments.exists():
                rel_scores = Response.objects.filter(
                    assignment__in=rel_assignments,
                    score__isnull=False
                ).aggregate(avg_score=Avg('score'))
                setattr(self, field, rel_scores['avg_score'])

        # Calculate completion rate
        total_expected = EvaluationAssignment.objects.filter(
            campaign=self.campaign,
            evaluatee=self.evaluatee
        ).count()
        if total_expected > 0:
            self.completion_rate = (self.total_evaluators / total_expected) * 100

        self.save()
