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
            models.Index(fields=['provider']),  # For filtering by provider
            models.Index(fields=['title', 'type']),  # For combined filtering
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
            models.Index(fields=['user', 'resource', 'status']),  # For combined filtering
            models.Index(fields=['progress_percentage']),  # For progress-based queries
            models.Index(fields=['rating']),  # For rating queries
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


class Certification(models.Model):
    """
    Professional certifications and credentials.
    Tracks employee certifications, expiration, and renewals.
    """

    CERTIFICATION_STATUS_CHOICES = [
        ('active', 'Aktiv'),
        ('expired', 'Müddəti Keçib'),
        ('pending_renewal', 'Yeniləmə Gözləyir'),
        ('suspended', 'Dayandırılıb'),
        ('revoked', 'Ləğv Edilib'),
    ]

    RENEWAL_FREQUENCY_CHOICES = [
        ('annual', 'İllik'),
        ('biennial', '2 İllik'),
        ('triennial', '3 İllik'),
        ('lifetime', 'Ömürlük'),
        ('custom', 'Xüsusi'),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='certifications',
        verbose_name=_('İstifadəçi')
    )

    # Certification details
    certification_name = models.CharField(
        max_length=200,
        verbose_name=_('Sertifikat Adı')
    )
    certification_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Sertifikat Kodu'),
        help_text=_('Məsələn: PMP, AWS-SAA, CISSP')
    )
    issuing_organization = models.CharField(
        max_length=200,
        verbose_name=_('Təqdim Edən Təşkilat')
    )
    credential_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Sertifikat ID')
    )

    # Related competency
    related_competency = models.ForeignKey(
        'competencies.Competency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='certifications',
        verbose_name=_('Əlaqəli Kompetensiya')
    )

    # Dates
    issue_date = models.DateField(
        verbose_name=_('Verilmə Tarixi')
    )
    expiration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Bitmə Tarixi')
    )
    last_renewal_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Son Yeniləmə Tarixi')
    )

    # Renewal settings
    renewal_frequency = models.CharField(
        max_length=20,
        choices=RENEWAL_FREQUENCY_CHOICES,
        default='annual',
        verbose_name=_('Yeniləmə Tezliyi')
    )
    renewal_reminder_days = models.IntegerField(
        default=60,
        verbose_name=_('Yeniləmə Xatırlatma Günləri'),
        help_text=_('Bitmə tarixindən neçə gün əvvəl xatırlatma göndərsin')
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=CERTIFICATION_STATUS_CHOICES,
        default='active',
        verbose_name=_('Status')
    )

    # Verification
    verification_url = models.URLField(
        blank=True,
        verbose_name=_('Yoxlama URL'),
        help_text=_('Sertifikatı yoxlamaq üçün link')
    )
    certificate_file = models.FileField(
        upload_to='certifications/%Y/',
        null=True,
        blank=True,
        verbose_name=_('Sertifikat Faylı')
    )

    # Requirements tracking
    requires_continuing_education = models.BooleanField(
        default=False,
        verbose_name=_('Davamlı Təhsil Tələb Edir')
    )
    ce_hours_required = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Tələb olunan CE Saatları'),
        help_text=_('Yeniləmə üçün lazım olan davamlı təhsil saatları')
    )
    ce_hours_completed = models.IntegerField(
        default=0,
        verbose_name=_('Tamamlanmış CE Saatları')
    )

    # Cost tracking
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Xərc')
    )
    company_sponsored = models.BooleanField(
        default=False,
        verbose_name=_('Şirkət Tərəfindən Maliyyələşdirilir')
    )

    # Metadata
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )
    is_required_for_role = models.BooleanField(
        default=False,
        verbose_name=_('Vəzifə üçün Məcburidir')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    # Simple History
    from simple_history.models import HistoricalRecords
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Sertifikat')
        verbose_name_plural = _('Sertifikatlar')
        ordering = ['-issue_date']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['expiration_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.certification_name}"

    def update_status(self):
        """Update certification status based on expiration date."""
        from django.utils import timezone

        if not self.expiration_date:
            return

        today = timezone.now().date()
        days_until_expiry = (self.expiration_date - today).days

        if days_until_expiry < 0:
            self.status = 'expired'
        elif days_until_expiry <= self.renewal_reminder_days:
            self.status = 'pending_renewal'
        else:
            self.status = 'active'

        self.save()

    def is_expired(self):
        """Check if certification is expired."""
        from django.utils import timezone

        if not self.expiration_date:
            return False

        return timezone.now().date() > self.expiration_date

    def days_until_expiry(self):
        """Get days until expiration."""
        from django.utils import timezone

        if not self.expiration_date:
            return None

        delta = self.expiration_date - timezone.now().date()
        return delta.days

    def renew_certification(self, new_expiration_date):
        """
        Renew certification.

        Args:
            new_expiration_date: New expiration date after renewal
        """
        from django.utils import timezone

        self.last_renewal_date = timezone.now().date()
        self.expiration_date = new_expiration_date
        self.status = 'active'
        self.ce_hours_completed = 0  # Reset CE hours
        self.save()

    def add_ce_hours(self, hours, description=''):
        """
        Add continuing education hours.

        Args:
            hours: Number of hours to add
            description: Description of CE activity
        """
        self.ce_hours_completed += hours
        self.save()

        # Create CE log entry
        ContinuingEducationLog.objects.create(
            certification=self,
            hours=hours,
            description=description
        )

    @property
    def ce_progress_percentage(self):
        """Get CE completion percentage."""
        if not self.ce_hours_required or self.ce_hours_required == 0:
            return 0

        percentage = (self.ce_hours_completed / self.ce_hours_required) * 100
        return min(100, round(percentage, 2))


class ContinuingEducationLog(models.Model):
    """
    Log of continuing education activities for certifications.
    """

    certification = models.ForeignKey(
        Certification,
        on_delete=models.CASCADE,
        related_name='ce_logs',
        verbose_name=_('Sertifikat')
    )

    activity_date = models.DateField(
        verbose_name=_('Fəaliyyət Tarixi')
    )
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Saatlar')
    )
    activity_type = models.CharField(
        max_length=100,
        verbose_name=_('Fəaliyyət Növü'),
        help_text=_('Məsələn: Vebinar, Konfrans, Kurs')
    )
    description = models.TextField(
        verbose_name=_('Təsvir')
    )
    provider = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Təmin Edən')
    )

    # Verification
    verification_document = models.FileField(
        upload_to='ce_documents/%Y/',
        null=True,
        blank=True,
        verbose_name=_('Təsdiq Sənədi')
    )
    verified = models.BooleanField(
        default=False,
        verbose_name=_('Təsdiqləndi')
    )
    verified_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_ce_logs',
        verbose_name=_('Təsdiqləyən')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )

    class Meta:
        verbose_name = _('Davamlı Təhsil Qeydi')
        verbose_name_plural = _('Davamlı Təhsil Qeydləri')
        ordering = ['-activity_date']

    def __str__(self):
        return f"{self.certification.certification_name} - {self.hours} hours - {self.activity_date}"
