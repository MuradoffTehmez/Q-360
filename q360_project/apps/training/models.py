"""
Models for training app - Təlim və İnkişaf Planlaması.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class TrainingResource(models.Model):
    """
    Təlim Kataloqu - Təşkilat üçün mövcud təlim resursları.
    Development plans ilə əlaqələndirilir və kompetensiyaları inkişaf etdirir.
    """

    TRAINING_TYPE_CHOICES = [
        ('course', 'Kurs'),
        ('certification', 'Sertifikasiya'),
        ('mentoring', 'Mentorluq'),
        ('workshop', 'Seminar'),
        ('conference', 'Konfrans'),
        ('webinar', 'Vebinar'),
        ('self_study', 'Öz-özünə Təhsil'),
    ]

    DELIVERY_METHOD_CHOICES = [
        ('online', 'Onlayn'),
        ('offline', 'Oflayn'),
        ('hybrid', 'Hibrid'),
    ]

    DIFFICULTY_LEVEL_CHOICES = [
        ('beginner', 'Başlanğıc'),
        ('intermediate', 'Orta'),
        ('advanced', 'Təkmil'),
        ('expert', 'Ekspert'),
    ]

    # Basic information
    title = models.CharField(
        max_length=300,
        verbose_name=_('Təlim Adı')
    )
    description = models.TextField(
        verbose_name=_('Təsvir')
    )
    type = models.CharField(
        max_length=20,
        choices=TRAINING_TYPE_CHOICES,
        default='course',
        verbose_name=_('Təlim Növü')
    )

    # Delivery details
    is_online = models.BooleanField(
        default=True,
        verbose_name=_('Onlayn')
    )
    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_METHOD_CHOICES,
        default='online',
        verbose_name=_('Çatdırılma Metodu')
    )
    link = models.URLField(
        blank=True,
        verbose_name=_('Link'),
        help_text=_('Onlayn təlim linki və ya əlavə məlumat')
    )

    # Content details
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVEL_CHOICES,
        default='intermediate',
        verbose_name=_('Çətinlik Səviyyəsi')
    )
    duration_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Müddət (saat)'),
        help_text=_('Təlimin təxmini müddəti saat olaraq')
    )
    language = models.CharField(
        max_length=50,
        default='Azərbaycan',
        verbose_name=_('Dil')
    )

    # Competency mapping
    required_competencies = models.ManyToManyField(
        'competencies.Competency',
        blank=True,
        related_name='training_resources',
        verbose_name=_('Əlaqəli Kompetensiyalar'),
        help_text=_('Bu təlimin inkişaf etdirdiyi kompetensiyalar')
    )

    # Provider information
    provider = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Təlim Təminatçısı')
    )
    instructor = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Təlimatçı/Mütəxəssis')
    )

    # Cost and capacity
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Qiymət'),
        help_text=_('Təlimin dəyəri (manat)')
    )
    max_participants = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Maksimum İştirakçı')
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )
    is_mandatory = models.BooleanField(
        default=False,
        verbose_name=_('Məcburi'),
        help_text=_('Müəyyən vəzifələr üçün məcburi təlim')
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

    # Simple History
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Təlim Resursu')
        verbose_name_plural = _('Təlim Resursları')
        ordering = ['title']
        indexes = [
            models.Index(fields=['type', 'is_active']),
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['is_mandatory']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

    def get_assigned_users_count(self):
        """Təlimə təyin olunmuş istifadəçi sayını qaytarır."""
        return self.user_trainings.filter(
            user__is_active=True
        ).count()

    def get_completion_rate(self):
        """Təlimi tamamlayan istifadəçi faizini hesablayır."""
        total = self.user_trainings.count()
        if total == 0:
            return 0

        completed = self.user_trainings.filter(status='completed').count()
        return round((completed / total) * 100, 2)

    def get_related_competencies(self):
        """Əlaqəli kompetensiyaları qaytarır."""
        return self.required_competencies.filter(is_active=True)


class UserTraining(models.Model):
    """
    İstifadəçi Təlimi - Təyin olunmuş və ya seçilmiş təlimlər.
    İstifadəçilərin təlim proqresini izləyir.
    """

    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('in_progress', 'Davam Edir'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'Ləğv Edildi'),
        ('failed', 'Uğursuz'),
    ]

    ASSIGNMENT_TYPE_CHOICES = [
        ('self_enrolled', 'Özü Qeydiyyatdan Keçdi'),
        ('manager_assigned', 'Menecer Tərəfindən Təyin Edildi'),
        ('system_recommended', 'Sistem Tövsiyəsi'),
        ('mandatory', 'Məcburi'),
    ]

    # Relations
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='user_trainings',
        verbose_name=_('İstifadəçi')
    )
    resource = models.ForeignKey(
        TrainingResource,
        on_delete=models.CASCADE,
        related_name='user_trainings',
        verbose_name=_('Təlim Resursu')
    )
    assigned_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_trainings',
        verbose_name=_('Təyin Edən')
    )

    # Assignment details
    assignment_type = models.CharField(
        max_length=30,
        choices=ASSIGNMENT_TYPE_CHOICES,
        default='self_enrolled',
        verbose_name=_('Təyin Növü')
    )
    related_goal = models.ForeignKey(
        'development_plans.DevelopmentGoal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_trainings',
        verbose_name=_('Əlaqəli İnkişaf Məqsədi')
    )

    # Dates
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Başlama Tarixi')
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Son Tarix')
    )
    completed_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Tamamlanma Tarixi')
    )

    # Status and progress
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    progress_percentage = models.IntegerField(
        default=0,
        verbose_name=_('Proqres (%)'),
        help_text=_('0-100 arası')
    )

    # Feedback and results
    completion_note = models.TextField(
        blank=True,
        verbose_name=_('Tamamlanma Qeydi')
    )
    user_feedback = models.TextField(
        blank=True,
        verbose_name=_('İstifadəçi Rəyi')
    )
    rating = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Reytinq'),
        help_text=_('1-5 ulduz arası qiymətləndirmə')
    )
    certificate_url = models.URLField(
        blank=True,
        verbose_name=_('Sertifikat Linki')
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

    # Simple History
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('İstifadəçi Təlimi')
        verbose_name_plural = _('İstifadəçi Təlimləri')
        unique_together = [['user', 'resource']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['resource', 'status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['assignment_type']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.resource.title} ({self.get_status_display()})"

    def mark_completed(self, completion_note=''):
        """Təlimi tamamlanmış kimi qeyd et."""
        from django.utils import timezone
        self.status = 'completed'
        self.progress_percentage = 100
        self.completed_date = timezone.now().date()
        self.completion_note = completion_note
        self.save()

    def mark_in_progress(self):
        """Təlimi davam edir kimi qeyd et."""
        from django.utils import timezone
        if self.status == 'pending':
            self.status = 'in_progress'
            if not self.start_date:
                self.start_date = timezone.now().date()
            self.save()

    def update_progress(self, percentage):
        """Proqresi yenilə."""
        if 0 <= percentage <= 100:
            self.progress_percentage = percentage
            if percentage == 100:
                self.mark_completed()
            elif percentage > 0 and self.status == 'pending':
                self.mark_in_progress()
            self.save()

    def is_overdue(self):
        """Təlimin vaxtı keçibmi?"""
        from django.utils import timezone
        if self.due_date and self.status not in ['completed', 'cancelled']:
            return timezone.now().date() > self.due_date
        return False

    def get_days_until_due(self):
        """Son tarixə qalan gün sayı."""
        from django.utils import timezone
        if self.due_date and self.status not in ['completed', 'cancelled']:
            delta = self.due_date - timezone.now().date()
            return delta.days
        return None
