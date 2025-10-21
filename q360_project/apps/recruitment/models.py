"""
Models for Recruitment & ATS (Applicant Tracking System).
Handles job postings, applications, candidate pipeline, and hiring workflow.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from apps.departments.models import Department


class JobPosting(models.Model):
    """
    Job vacancy postings.
    """

    STATUS_CHOICES = [
        ('draft', 'Qaralama'),
        ('open', 'Açıq'),
        ('closed', 'Bağlı'),
        ('on_hold', 'Gözləmədə'),
        ('cancelled', 'Ləğv Edilmiş'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Tam Ştatlı'),
        ('part_time', 'Qismən Ştatlı'),
        ('contract', 'Müqavilə'),
        ('temporary', 'Müvəqqəti'),
        ('internship', 'Təcrübə'),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Başlanğıc'),
        ('junior', 'Junior'),
        ('mid', 'Orta'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
        ('manager', 'Menecer'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name=_('Vəzifə Adı')
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Vakansiya Kodu')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='job_postings',
        verbose_name=_('Şöbə')
    )
    description = models.TextField(
        verbose_name=_('Təsvir')
    )
    responsibilities = models.TextField(
        verbose_name=_('Vəzifə Öhdəlikləri')
    )
    requirements = models.TextField(
        verbose_name=_('Tələblər')
    )
    qualifications = models.TextField(
        blank=True,
        verbose_name=_('İstisnalı Kvalifikasiyalar')
    )

    # Employment details
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='full_time',
        verbose_name=_('İşə Qəbul Növü')
    )
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default='mid',
        verbose_name=_('Təcrübə Səviyyəsi')
    )
    number_of_positions = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_('Vəzifə Sayı')
    )

    # Salary information
    salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Minimum Maaş')
    )
    salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Maksimum Maaş')
    )
    salary_currency = models.CharField(
        max_length=3,
        default='AZN',
        verbose_name=_('Valyuta')
    )
    show_salary = models.BooleanField(
        default=False,
        verbose_name=_('Maaşı Göstər')
    )

    # Location
    location = models.CharField(
        max_length=200,
        verbose_name=_('İş Yeri')
    )
    remote_allowed = models.BooleanField(
        default=False,
        verbose_name=_('Uzaqdan İş İmkanı')
    )

    # Timeline
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('Status')
    )
    posted_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Elan Tarixi')
    )
    closing_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Bağlanma Tarixi')
    )

    # Hiring team
    hiring_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_job_postings',
        verbose_name=_('İşə Qəbul Meneceri')
    )
    recruiters = models.ManyToManyField(
        User,
        blank=True,
        related_name='recruited_job_postings',
        verbose_name=_('İşə Qəbul Komandası')
    )

    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_job_postings',
        verbose_name=_('Yaradan')
    )
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
        verbose_name = _('Vakansiya')
        verbose_name_plural = _('Vakansiyalar')
        ordering = ['-posted_date', '-created_at']
        indexes = [
            models.Index(fields=['status', 'posted_date']),
            models.Index(fields=['department']),
            models.Index(fields=['employment_type']),
        ]

    def __str__(self):
        return f"{self.code} - {self.title}"

    @property
    def is_open(self):
        """Check if job posting is open for applications."""
        from datetime import date
        return (
            self.status == 'open' and
            (self.closing_date is None or self.closing_date >= date.today())
        )

    @property
    def application_count(self):
        """Get total number of applications."""
        return self.applications.count()

    @property
    def active_application_count(self):
        """Get number of active applications (not rejected/withdrawn)."""
        return self.applications.exclude(
            status__in=['rejected', 'withdrawn']
        ).count()


class Application(models.Model):
    """
    Job applications from candidates.
    """

    STATUS_CHOICES = [
        ('received', 'Alındı'),
        ('screening', 'Sınaq'),
        ('interview', 'Müsahibə'),
        ('assessment', 'Qiymətləndirmə'),
        ('offer', 'Təklif'),
        ('hired', 'İşə Qəbul Edildi'),
        ('rejected', 'Rədd Edildi'),
        ('withdrawn', 'Geri Çəkildi'),
    ]

    SOURCE_CHOICES = [
        ('website', 'Veb Sayt'),
        ('linkedin', 'LinkedIn'),
        ('job_board', 'İş Elanları Saytı'),
        ('referral', 'İstinad'),
        ('direct', 'Birbaşa'),
        ('agency', 'Agentlik'),
        ('other', 'Digər'),
    ]

    job_posting = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('Vakansiya')
    )

    # Candidate information
    first_name = models.CharField(
        max_length=100,
        verbose_name=_('Ad')
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_('Soyad')
    )
    email = models.EmailField(
        verbose_name=_('E-poçt')
    )
    phone = models.CharField(
        max_length=20,
        verbose_name=_('Telefon')
    )

    # Documents
    resume = models.FileField(
        upload_to='resumes/%Y/%m/',
        verbose_name=_('CV/Rezume')
    )
    cover_letter = models.TextField(
        blank=True,
        verbose_name=_('Müraciət Məktubu')
    )
    portfolio_url = models.URLField(
        blank=True,
        verbose_name=_('Portfolio/LinkedIn URL')
    )

    # Application details
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='received',
        verbose_name=_('Status')
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='website',
        verbose_name=_('Mənbə')
    )
    referrer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals',
        verbose_name=_('İstinad Edən')
    )

    # Experience and salary
    current_position = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Hazırki Vəzifə')
    )
    years_of_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name=_('Təcrübə İli')
    )
    expected_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Gözlənilən Maaş')
    )
    notice_period_days = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Bildiriş Müddəti (Gün)')
    )

    # Evaluation
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Reytinq (1-5)')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )

    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_applications',
        verbose_name=_('Təyin Edilən')
    )

    # Metadata
    applied_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Müraciət Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Müraciət')
        verbose_name_plural = _('Müraciətlər')
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['job_posting', 'status']),
            models.Index(fields=['email']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_posting.title}"

    @property
    def full_name(self):
        """Get candidate's full name."""
        return f"{self.first_name} {self.last_name}"


class Interview(models.Model):
    """
    Interview scheduling and tracking.
    """

    TYPE_CHOICES = [
        ('phone', 'Telefon'),
        ('video', 'Video'),
        ('onsite', 'Yerində'),
        ('technical', 'Texniki'),
        ('hr', 'HR'),
        ('final', 'Final'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Planlaşdırılıb'),
        ('completed', 'Tamamlanıb'),
        ('cancelled', 'Ləğv Edilib'),
        ('rescheduled', 'Yenidən Planlaşdırılıb'),
        ('no_show', 'Gəlmədi'),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='interviews',
        verbose_name=_('Müraciət')
    )
    interview_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name=_('Müsahibə Növü')
    )
    scheduled_date = models.DateTimeField(
        verbose_name=_('Planlaşdırılmış Tarix')
    )
    duration_minutes = models.IntegerField(
        default=60,
        verbose_name=_('Müddət (Dəqiqə)')
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Yer')
    )
    meeting_link = models.URLField(
        blank=True,
        verbose_name=_('Görüş Linki')
    )

    # Interviewers
    interviewers = models.ManyToManyField(
        User,
        related_name='conducted_interviews',
        verbose_name=_('Müsahibə Alanlar')
    )

    # Status and feedback
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name=_('Status')
    )
    feedback = models.TextField(
        blank=True,
        verbose_name=_('Rəy')
    )
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Reytinq (1-5)')
    )
    recommendation = models.CharField(
        max_length=20,
        choices=[
            ('strong_yes', 'Güclü Bəli'),
            ('yes', 'Bəli'),
            ('maybe', 'Bəlkə'),
            ('no', 'Xeyr'),
            ('strong_no', 'Güclü Xeyr'),
        ],
        blank=True,
        verbose_name=_('Tövsiyə')
    )

    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_interviews',
        verbose_name=_('Yaradan')
    )
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
        verbose_name = _('Müsahibə')
        verbose_name_plural = _('Müsahibələr')
        ordering = ['-scheduled_date']
        indexes = [
            models.Index(fields=['application', 'status']),
            models.Index(fields=['scheduled_date']),
        ]

    def __str__(self):
        return f"{self.application.full_name} - {self.get_interview_type_display()} ({self.scheduled_date})"


class Offer(models.Model):
    """
    Job offers to candidates.
    """

    STATUS_CHOICES = [
        ('draft', 'Qaralama'),
        ('sent', 'Göndərildi'),
        ('accepted', 'Qəbul Edildi'),
        ('rejected', 'Rədd Edildi'),
        ('negotiating', 'Müzakirə Edilir'),
        ('expired', 'Müddəti Keçib'),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='offers',
        verbose_name=_('Müraciət')
    )

    # Offer details
    position_title = models.CharField(
        max_length=200,
        verbose_name=_('Vəzifə Adı')
    )
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Maaş')
    )
    currency = models.CharField(
        max_length=3,
        default='AZN',
        verbose_name=_('Valyuta')
    )
    bonus_potential = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Bonus Potensialı')
    )
    benefits = models.TextField(
        blank=True,
        verbose_name=_('Müavinətlər')
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Başlanğıc Tarixi')
    )

    # Offer status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('Status')
    )
    sent_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Göndərilmə Tarixi')
    )
    expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Son Qəbul Tarixi')
    )
    response_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Cavab Tarixi')
    )

    # Documents
    offer_letter = models.FileField(
        upload_to='offer_letters/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_('Təklif Məktubu')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )

    # Approval
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_offers',
        verbose_name=_('Təsdiqləyən')
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Təsdiq Tarixi')
    )

    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_offers',
        verbose_name=_('Yaradan')
    )
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
        verbose_name = _('Təklif')
        verbose_name_plural = _('Təkliflər')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['application', 'status']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.application.full_name} - {self.position_title} - {self.salary} {self.currency}"

    @property
    def is_expired(self):
        """Check if offer has expired."""
        from datetime import date
        if self.expiry_date and self.status in ['sent', 'negotiating']:
            return date.today() > self.expiry_date
        return False


class OnboardingTask(models.Model):
    """
    Onboarding tasks for new hires.
    """

    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('in_progress', 'Davam Edir'),
        ('completed', 'Tamamlanıb'),
        ('skipped', 'Ötürülüb'),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='onboarding_tasks',
        verbose_name=_('Müraciət')
    )
    new_hire = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='onboarding_tasks',
        verbose_name=_('Yeni İşçi')
    )

    # Task details
    title = models.CharField(
        max_length=200,
        verbose_name=_('Tapşırıq')
    )
    description = models.TextField(
        verbose_name=_('Təsvir')
    )
    category = models.CharField(
        max_length=100,
        choices=[
            ('documentation', 'Sənədləşdirmə'),
            ('equipment', 'Avadanlıq'),
            ('access', 'Giriş'),
            ('training', 'Təlim'),
            ('orientation', 'Orientasiya'),
            ('other', 'Digər'),
        ],
        default='documentation',
        verbose_name=_('Kateqoriya')
    )

    # Status and assignment
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_onboarding_tasks',
        verbose_name=_('Təyin Edilən')
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
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
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
        verbose_name = _('İşəbaşlama Tapşırığı')
        verbose_name_plural = _('İşəbaşlama Tapşırıqları')
        ordering = ['due_date', '-created_at']
        indexes = [
            models.Index(fields=['application', 'status']),
            models.Index(fields=['new_hire', 'status']),
            models.Index(fields=['assigned_to', 'status']),
        ]

    def __str__(self):
        return f"{self.application.full_name} - {self.title}"


class CandidateExperience(models.Model):
    """
    Tracks candidate experience throughout the recruitment process.
    Collects feedback at each touchpoint for process improvement.
    """

    TOUCHPOINT_CHOICES = [
        ('application', 'Müraciət'),
        ('screening', 'İlkin Sınaq'),
        ('interview', 'Müsahibə'),
        ('assessment', 'Qiymətləndirmə'),
        ('offer', 'Təklif'),
        ('onboarding', 'İşə Başlama'),
        ('rejection', 'Rədd'),
    ]

    SATISFACTION_CHOICES = [
        (1, 'Çox Narazı'),
        (2, 'Narazı'),
        (3, 'Neytral'),
        (4, 'Razı'),
        (5, 'Çox Razı'),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='experience_feedback',
        verbose_name=_('Müraciət')
    )
    touchpoint = models.CharField(
        max_length=20,
        choices=TOUCHPOINT_CHOICES,
        verbose_name=_('Təmas Nöqtəsi')
    )
    feedback_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Rəy Tarixi')
    )

    # Satisfaction ratings
    overall_satisfaction = models.IntegerField(
        choices=SATISFACTION_CHOICES,
        verbose_name=_('Ümumi Məmnuniyyət')
    )
    communication_rating = models.IntegerField(
        null=True,
        blank=True,
        choices=SATISFACTION_CHOICES,
        verbose_name=_('Kommunikasiya Qiyməti')
    )
    process_clarity_rating = models.IntegerField(
        null=True,
        blank=True,
        choices=SATISFACTION_CHOICES,
        verbose_name=_('Proses Aydınlığı')
    )
    timeliness_rating = models.IntegerField(
        null=True,
        blank=True,
        choices=SATISFACTION_CHOICES,
        verbose_name=_('Vaxtında Olma')
    )
    professionalism_rating = models.IntegerField(
        null=True,
        blank=True,
        choices=SATISFACTION_CHOICES,
        verbose_name=_('Peşəkarlıq')
    )

    # Qualitative feedback
    positive_aspects = models.TextField(
        blank=True,
        verbose_name=_('Pozitiv Aspektlər')
    )
    improvement_areas = models.TextField(
        blank=True,
        verbose_name=_('Təkmilləşdirmə Sahələri')
    )
    additional_comments = models.TextField(
        blank=True,
        verbose_name=_('Əlavə Şərhlər')
    )

    # Recommend to others
    would_recommend = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('Başqalarına Tövsiyə Edər')
    )
    nps_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_('NPS Balı'),
        help_text=_('0-10: Bu şirkətdə işləməyi dostlarınıza nə dərəcədə tövsiyə edərsiniz?')
    )

    # Survey metadata
    survey_completed = models.BooleanField(
        default=False,
        verbose_name=_('Sorğu Tamamlandı')
    )
    survey_sent_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Sorğu Göndərilmə Tarixi')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Namizəd Təcrübəsi')
        verbose_name_plural = _('Namizəd Təcrübələri')
        ordering = ['-feedback_date']
        indexes = [
            models.Index(fields=['application', 'touchpoint']),
            models.Index(fields=['touchpoint', 'overall_satisfaction']),
        ]

    def __str__(self):
        return f"{self.application.full_name} - {self.get_touchpoint_display()} ({self.overall_satisfaction}/5)"

    def calculate_average_rating(self):
        """Calculate average rating across all dimensions."""
        ratings = [
            self.overall_satisfaction,
            self.communication_rating,
            self.process_clarity_rating,
            self.timeliness_rating,
            self.professionalism_rating
        ]
        valid_ratings = [r for r in ratings if r is not None]

        if valid_ratings:
            return sum(valid_ratings) / len(valid_ratings)
        return 0


class Referral(models.Model):
    """
    Employee referral tracking and management.
    Automates referral program with rewards and analytics.
    """

    STATUS_CHOICES = [
        ('submitted', 'Təqdim Edildi'),
        ('under_review', 'Baxışdadır'),
        ('interview_scheduled', 'Müsahibə Planlaşdırılıb'),
        ('hired', 'İşə Qəbul Edildi'),
        ('not_selected', 'Seçilmədi'),
        ('withdrawn', 'Geri Çəkildi'),
    ]

    REWARD_STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('eligible', 'Uyğundur'),
        ('approved', 'Təsdiqləndi'),
        ('paid', 'Ödənildi'),
        ('not_eligible', 'Uyğun Deyil'),
    ]

    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='referrals_made',
        verbose_name=_('Tövsiyə Edən')
    )
    job_posting = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name='referrals',
        verbose_name=_('Vakansiya')
    )
    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name='referral_info',
        verbose_name=_('Müraciət')
    )

    # Referral details
    relationship = models.CharField(
        max_length=100,
        verbose_name=_('Əlaqə'),
        help_text=_('Namizədlə əlaqə (məs: Keçmiş həmkar, Universitet dostu)')
    )
    referral_notes = models.TextField(
        blank=True,
        verbose_name=_('Tövsiyə Qeydləri')
    )

    # Status tracking
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='submitted',
        verbose_name=_('Status')
    )

    # Reward management
    reward_status = models.CharField(
        max_length=20,
        choices=REWARD_STATUS_CHOICES,
        default='pending',
        verbose_name=_('Mükafat Statusu')
    )
    reward_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Mükafat Məbləği')
    )
    reward_currency = models.CharField(
        max_length=3,
        default='AZN',
        verbose_name=_('Valyuta')
    )
    reward_paid_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Mükafat Ödəniş Tarixi')
    )

    # Timestamps
    submitted_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Təqdim Tarixi')
    )
    hired_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('İşə Qəbul Tarixi')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Tövsiyə')
        verbose_name_plural = _('Tövsiyələr')
        ordering = ['-submitted_date']
        indexes = [
            models.Index(fields=['referrer', 'status']),
            models.Index(fields=['job_posting', 'status']),
            models.Index(fields=['reward_status']),
        ]

    def __str__(self):
        return f"{self.referrer.get_full_name()} → {self.application.full_name}"

    def update_status_from_application(self):
        """Update referral status based on application status."""
        status_mapping = {
            'screening': 'under_review',
            'interview': 'interview_scheduled',
            'hired': 'hired',
            'rejected': 'not_selected',
            'withdrawn': 'withdrawn'
        }

        new_status = status_mapping.get(self.application.status)
        if new_status:
            self.status = new_status

            # Update reward eligibility
            if new_status == 'hired':
                self.reward_status = 'eligible'
                self.hired_date = self.application.updated_at.date()

                # Set default reward amount if configured
                # This could come from a ReferralRewardConfig model
                if not self.reward_amount:
                    self.reward_amount = Decimal('500.00')  # Default amount

            self.save()

    def approve_reward(self, approver):
        """Approve referral reward."""
        if self.reward_status == 'eligible':
            self.reward_status = 'approved'
            self.save()

    def mark_reward_paid(self, payment_date=None):
        """Mark reward as paid."""
        from django.utils import timezone

        if self.reward_status == 'approved':
            self.reward_status = 'paid'
            self.reward_paid_date = payment_date or timezone.now().date()
            self.save()
