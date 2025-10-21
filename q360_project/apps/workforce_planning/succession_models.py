"""
Succession Planning Models.
Handles talent assessment, potential analysis, and succession planning.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from apps.departments.models import Department


class CriticalPosition(models.Model):
    """
    Identifies critical positions that require succession planning.
    """

    CRITICALITY_LEVEL_CHOICES = [
        ('high', 'Yüksək'),
        ('medium', 'Orta'),
        ('low', 'Aşağı'),
    ]

    position_title = models.CharField(
        max_length=200,
        verbose_name=_('Vəzifə Adı')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='critical_positions',
        verbose_name=_('Departament')
    )
    current_incumbent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_position',
        verbose_name=_('Hazırki Vəzifə Sahibi')
    )

    description = models.TextField(
        verbose_name=_('Vəzifə Təsviri')
    )
    key_responsibilities = models.TextField(
        verbose_name=_('Əsas Vəzifələr')
    )
    required_competencies = models.ManyToManyField(
        'competencies.Competency',
        blank=True,
        related_name='critical_positions',
        verbose_name=_('Tələb olunan Kompetensiyalar')
    )

    # Criticality assessment
    criticality_level = models.CharField(
        max_length=20,
        choices=CRITICALITY_LEVEL_CHOICES,
        default='medium',
        verbose_name=_('Kritiklik Səviyyəsi')
    )
    business_impact = models.TextField(
        verbose_name=_('Biznesə Təsir'),
        help_text=_('Bu vəzifənin boş qalmasının biznesə təsiri')
    )
    difficulty_to_fill = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Doldurma Çətinliyi'),
        help_text=_('1=Çox asan, 5=Çox çətin')
    )

    # Retirement/vacancy risk
    estimated_vacancy_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Təxmini Boşalma Tarixi')
    )
    retirement_risk = models.BooleanField(
        default=False,
        verbose_name=_('Təqaüd Riski')
    )

    # Succession readiness
    has_ready_successor = models.BooleanField(
        default=False,
        verbose_name=_('Hazır Varisə Sahib')
    )
    succession_readiness_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_('Varislik Hazırlıq Balı'),
        help_text=_('0-100 arası')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_critical_positions',
        verbose_name=_('Yaradan')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Kritik Vəzifə')
        verbose_name_plural = _('Kritik Vəzifələr')
        ordering = ['-criticality_level', 'position_title']
        indexes = [
            models.Index(fields=['department', 'is_active']),
            models.Index(fields=['criticality_level']),
        ]

    def __str__(self):
        return f"{self.position_title} ({self.department.name})"

    def update_succession_readiness(self):
        """Calculate and update succession readiness score."""
        successors = self.succession_candidates.filter(
            status='ready',
            readiness_level__in=['ready_now', 'ready_1_year']
        )

        if successors.exists():
            self.has_ready_successor = True
            # Calculate average readiness from top candidates
            avg_readiness = sum(s.overall_readiness_score for s in successors[:3]) / min(3, successors.count())
            self.succession_readiness_score = avg_readiness
        else:
            self.has_ready_successor = False
            self.succession_readiness_score = 0

        self.save()


class TalentAssessment(models.Model):
    """
    Comprehensive talent assessment for succession planning.
    Includes performance, potential, and competency evaluations.
    """

    PERFORMANCE_RATING_CHOICES = [
        ('below_expectations', 'Gözləntidən Aşağı'),
        ('meets_expectations', 'Gözləntiləri Qarşılayır'),
        ('exceeds_expectations', 'Gözləntiləri Üstələyir'),
        ('exceptional', 'İstisna Dərəcədə Yüksək'),
    ]

    POTENTIAL_RATING_CHOICES = [
        ('limited', 'Məhdud'),
        ('moderate', 'Orta'),
        ('high', 'Yüksək'),
        ('very_high', 'Çox Yüksək'),
    ]

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='talent_assessments',
        verbose_name=_('İşçi')
    )
    assessment_date = models.DateField(
        verbose_name=_('Qiymətləndirmə Tarixi')
    )
    assessor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='conducted_talent_assessments',
        verbose_name=_('Qiymətləndirən')
    )

    # Performance rating
    performance_rating = models.CharField(
        max_length=30,
        choices=PERFORMANCE_RATING_CHOICES,
        verbose_name=_('Performans Qiyməti')
    )
    performance_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Performans Balı')
    )

    # Potential rating
    potential_rating = models.CharField(
        max_length=20,
        choices=POTENTIAL_RATING_CHOICES,
        verbose_name=_('Potensial Qiyməti')
    )
    potential_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Potensial Balı')
    )

    # 9-Box Grid position (Performance vs Potential)
    nine_box_category = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('9-Box Kateqoriyası'),
        help_text=_('Məsələn: "High Performer, High Potential"')
    )

    # Leadership competencies
    leadership_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Liderlik Balı')
    )
    strategic_thinking_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Strateji Düşüncə Balı')
    )
    decision_making_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Qərar Qəbulu Balı')
    )

    # Development areas
    strengths = models.TextField(
        verbose_name=_('Güclü Tərəflər')
    )
    development_areas = models.TextField(
        verbose_name=_('İnkişaf Sahələri')
    )

    # Mobility and aspiration
    geographic_mobility = models.BooleanField(
        default=False,
        verbose_name=_('Coğrafi Mobillik'),
        help_text=_('Başqa yerə köçməyə hazırdır')
    )
    functional_mobility = models.BooleanField(
        default=False,
        verbose_name=_('Funksional Mobillik'),
        help_text=_('Başqa funksiyaya keçməyə hazırdır')
    )
    career_aspiration = models.TextField(
        blank=True,
        verbose_name=_('Karyera Arzuları')
    )

    # Overall assessment
    overall_assessment = models.TextField(
        verbose_name=_('Ümumi Qiymətləndirmə')
    )
    retention_risk = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Aşağı'),
            ('medium', 'Orta'),
            ('high', 'Yüksək'),
        ],
        default='low',
        verbose_name=_('Saxlama Riski')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Talant Qiymətləndirməsi')
        verbose_name_plural = _('Talant Qiymətləndirmələri')
        ordering = ['-assessment_date']
        indexes = [
            models.Index(fields=['employee', '-assessment_date']),
            models.Index(fields=['performance_rating', 'potential_rating']),
        ]

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.assessment_date}"

    def calculate_nine_box_position(self):
        """Calculate 9-box grid position based on performance and potential."""
        perf_map = {
            'below_expectations': 'Low',
            'meets_expectations': 'Medium',
            'exceeds_expectations': 'High',
            'exceptional': 'High'
        }

        pot_map = {
            'limited': 'Low',
            'moderate': 'Medium',
            'high': 'High',
            'very_high': 'High'
        }

        perf = perf_map.get(self.performance_rating, 'Medium')
        pot = pot_map.get(self.potential_rating, 'Medium')

        self.nine_box_category = f"{perf} Performer, {pot} Potential"
        self.save()


class SuccessionCandidate(models.Model):
    """
    Links employees to critical positions they could succeed into.
    Tracks readiness and development plans.
    """

    READINESS_LEVEL_CHOICES = [
        ('ready_now', 'İndi Hazırdır'),
        ('ready_1_year', '1 İl İçində Hazır'),
        ('ready_2_3_years', '2-3 İl İçində Hazır'),
        ('future_potential', 'Gələcək Potensial'),
    ]

    STATUS_CHOICES = [
        ('identified', 'Müəyyənləşdirildi'),
        ('developing', 'İnkişaf Edir'),
        ('ready', 'Hazırdır'),
        ('promoted', 'Tərtiqə Alındı'),
        ('no_longer_candidate', 'Artıq Namizəd Deyil'),
    ]

    critical_position = models.ForeignKey(
        CriticalPosition,
        on_delete=models.CASCADE,
        related_name='succession_candidates',
        verbose_name=_('Kritik Vəzifə')
    )
    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='succession_opportunities',
        verbose_name=_('Namizəd')
    )

    # Readiness assessment
    readiness_level = models.CharField(
        max_length=20,
        choices=READINESS_LEVEL_CHOICES,
        default='future_potential',
        verbose_name=_('Hazırlıq Səviyyəsi')
    )
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='identified',
        verbose_name=_('Status')
    )

    # Competency gaps
    competency_gap_analysis = models.TextField(
        blank=True,
        verbose_name=_('Kompetensiya Boşluğu Analizi')
    )
    skills_to_develop = models.TextField(
        blank=True,
        verbose_name=_('İnkişaf Etdirilməli Bacarıqlar')
    )

    # Readiness scores
    technical_readiness = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Texniki Hazırlıq (%)')
    )
    leadership_readiness = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Liderlik Hazırlığı (%)')
    )
    overall_readiness_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Ümumi Hazırlıq Balı')
    )

    # Development plan
    development_plan = models.TextField(
        blank=True,
        verbose_name=_('İnkişaf Planı')
    )
    target_ready_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Hədəf Hazırlıq Tarixi')
    )

    # Tracking
    identified_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Müəyyənləşdirmə Tarixi')
    )
    identified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='identified_successors',
        verbose_name=_('Müəyyənləşdirən')
    )

    # Priority
    is_primary_successor = models.BooleanField(
        default=False,
        verbose_name=_('Əsas Varis'),
        help_text=_('Bu namizəd bu vəzifə üçün əsas varisdirmi?')
    )
    priority_rank = models.IntegerField(
        default=0,
        verbose_name=_('Prioritet Sırası')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Varislik Namizədi')
        verbose_name_plural = _('Varislik Namizədləri')
        ordering = ['-is_primary_successor', 'priority_rank', '-overall_readiness_score']
        unique_together = [['critical_position', 'candidate']]
        indexes = [
            models.Index(fields=['critical_position', 'status']),
            models.Index(fields=['candidate', 'status']),
            models.Index(fields=['readiness_level']),
        ]

    def __str__(self):
        return f"{self.candidate.get_full_name()} → {self.critical_position.position_title}"

    def calculate_overall_readiness(self):
        """Calculate overall readiness score from component scores."""
        self.overall_readiness_score = (
            (self.technical_readiness * 0.6) +
            (self.leadership_readiness * 0.4)
        )
        self.save()

    def update_status_based_on_readiness(self):
        """Automatically update status based on readiness score."""
        if self.overall_readiness_score >= 85:
            self.status = 'ready'
            self.readiness_level = 'ready_now'
        elif self.overall_readiness_score >= 70:
            self.readiness_level = 'ready_1_year'
            self.status = 'developing'
        elif self.overall_readiness_score >= 50:
            self.readiness_level = 'ready_2_3_years'
            self.status = 'developing'
        else:
            self.readiness_level = 'future_potential'
            self.status = 'identified'

        self.save()


class SuccessionPlanReview(models.Model):
    """
    Periodic reviews of succession plans.
    Ensures succession plans stay current and effective.
    """

    critical_position = models.ForeignKey(
        CriticalPosition,
        on_delete=models.CASCADE,
        related_name='plan_reviews',
        verbose_name=_('Kritik Vəzifə')
    )
    review_date = models.DateField(
        verbose_name=_('Baxış Tarixi')
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='conducted_succession_reviews',
        verbose_name=_('Baxan')
    )

    # Review findings
    plan_adequacy = models.CharField(
        max_length=20,
        choices=[
            ('adequate', 'Adekvat'),
            ('needs_improvement', 'Təkmilləşdirmə Lazımdır'),
            ('inadequate', 'Qeyri-adekvat'),
        ],
        verbose_name=_('Plan Adekvatları')
    )
    successor_bench_strength = models.IntegerField(
        default=0,
        verbose_name=_('Varis Dəstə Gücü'),
        help_text=_('Hazır varislərin sayı')
    )

    findings = models.TextField(
        verbose_name=_('Tapıntılar')
    )
    recommendations = models.TextField(
        verbose_name=_('Tövsiyələr')
    )
    action_items = models.TextField(
        verbose_name=_('Fəaliyyət Bəndləri')
    )

    # Next review
    next_review_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Növbəti Baxış Tarixi')
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Varislik Planı Baxışı')
        verbose_name_plural = _('Varislik Planı Baxışları')
        ordering = ['-review_date']

    def __str__(self):
        return f"{self.critical_position.position_title} - Baxış {self.review_date}"
