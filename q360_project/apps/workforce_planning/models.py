"""
Workforce Planning models for talent matrix, succession planning, and gap analysis.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import User
from apps.departments.models import Position


class TalentMatrix(models.Model):
    """
    9-Box Talent Matrix: Performance vs Potential
    """
    PERFORMANCE_CHOICES = [
        ('low', 'Aşağı Performans'),
        ('medium', 'Orta Performans'),
        ('high', 'Yüksək Performans'),
    ]

    POTENTIAL_CHOICES = [
        ('low', 'Aşağı Potensial'),
        ('medium', 'Orta Potensial'),
        ('high', 'Yüksək Potensial'),
    ]

    BOX_CATEGORY_CHOICES = [
        ('box1', '1. Qutu - Zəif Nəticə'),  # Low Performance, Low Potential
        ('box2', '2. Qutu - İnkişaf Ehtiyacı'),  # Low Performance, Medium Potential
        ('box3', '3. Qutu - Yüksək Potensial'),  # Low Performance, High Potential
        ('box4', '4. Qutu - Əsas Kadr'),  # Medium Performance, Low Potential
        ('box5', '5. Qutu - Güclü İfaçı'),  # Medium Performance, Medium Potential
        ('box6', '6. Qutu - Gələcək Lider'),  # Medium Performance, High Potential
        ('box7', '7. Qutu - İstedad'),  # High Performance, Low Potential
        ('box8', '8. Qutu - Yüksək İfaçı'),  # High Performance, Medium Potential
        ('box9', '9. Qutu - Üstün İstedad'),  # High Performance, High Potential
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='talent_assessments')
    performance_level = models.CharField(max_length=10, choices=PERFORMANCE_CHOICES, verbose_name='Performans Səviyyəsi')
    potential_level = models.CharField(max_length=10, choices=POTENTIAL_CHOICES, verbose_name='Potensial Səviyyəsi')
    box_category = models.CharField(max_length=10, choices=BOX_CATEGORY_CHOICES, verbose_name='9-Qutu Kateqoriyası')

    performance_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Performans Balı'
    )
    potential_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Potensial Balı'
    )

    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='talent_assessments_made', verbose_name='Qiymətləndirən')
    assessment_date = models.DateField(verbose_name='Qiymətləndirmə Tarixi')
    assessment_period = models.CharField(max_length=50, verbose_name='Qiymətləndirmə Dövrü', help_text='Məsələn: 2024 Q1')

    notes = models.TextField(blank=True, verbose_name='Qeydlər')
    development_actions = models.TextField(blank=True, verbose_name='İnkişaf Tədbirləri')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'İstedad Matrisi Qiymətləndirməsi'
        verbose_name_plural = 'İstedad Matrisi Qiymətləndirmələri'
        ordering = ['-assessment_date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-assessment_date']),
            models.Index(fields=['box_category']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_box_category_display()} ({self.assessment_period})"

    def save(self, *args, **kwargs):
        # Auto-calculate box category based on performance and potential
        perf_map = {'low': 1, 'medium': 2, 'high': 3}
        pot_map = {'low': 1, 'medium': 2, 'high': 3}

        perf_num = perf_map.get(self.performance_level, 2)
        pot_num = pot_map.get(self.potential_level, 2)

        box_num = (perf_num - 1) * 3 + pot_num
        self.box_category = f'box{box_num}'

        super().save(*args, **kwargs)


class CriticalRole(models.Model):
    """
    Critical roles within the organization that require succession planning.
    """
    CRITICALITY_CHOICES = [
        ('low', 'Aşağı'),
        ('medium', 'Orta'),
        ('high', 'Yüksək'),
        ('critical', 'Kritik'),
    ]

    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='critical_role_designations')
    current_holder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='held_critical_roles', verbose_name='Hal-hazırkı Tutucusu')

    criticality_level = models.CharField(max_length=10, choices=CRITICALITY_CHOICES, default='medium', verbose_name='Kritiklik Səviyyəsi')
    business_impact = models.TextField(verbose_name='Biznesə Təsiri')

    required_competencies = models.ManyToManyField('competencies.Competency', blank=True, verbose_name='Tələb olunan Kompetensiyalar')
    required_experience_years = models.IntegerField(default=0, verbose_name='Tələb olunan Təcrübə (İl)')

    succession_readiness = models.CharField(
        max_length=20,
        choices=[
            ('no_successor', 'Varis Yoxdur'),
            ('needs_development', 'İnkişaf Tələb olunur'),
            ('ready_1_2_years', '1-2 İl sonra Hazır'),
            ('ready_now', 'İndi Hazır'),
        ],
        default='no_successor',
        verbose_name='Varislik Hazırlığı'
    )

    is_active = models.BooleanField(default=True, verbose_name='Aktivdir')
    designated_date = models.DateField(auto_now_add=True, verbose_name='Təyin Tarixi')

    notes = models.TextField(blank=True, verbose_name='Qeydlər')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Kritik Rol'
        verbose_name_plural = 'Kritik Rollar'
        ordering = ['-criticality_level', 'position__title']

    def __str__(self):
        return f"{self.position.title} ({self.get_criticality_level_display()})"


class SuccessionCandidate(models.Model):
    """
    Candidates identified for succession planning for critical roles.
    """
    READINESS_CHOICES = [
        ('not_ready', 'Hazır Deyil'),
        ('needs_development', 'İnkişaf Tələb olunur'),
        ('ready_1_2_years', '1-2 İl sonra Hazır'),
        ('ready_6_12_months', '6-12 Ay sonra Hazır'),
        ('ready_now', 'İndi Hazır'),
    ]

    critical_role = models.ForeignKey(CriticalRole, on_delete=models.CASCADE, related_name='succession_candidates', verbose_name='Kritik Rol')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='succession_candidacies', verbose_name='Namizəd')

    readiness_level = models.CharField(max_length=20, choices=READINESS_CHOICES, default='needs_development', verbose_name='Hazırlıq Səviyyəsi')
    readiness_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        verbose_name='Hazırlıq Balı'
    )

    strengths = models.TextField(blank=True, verbose_name='Güclü Tərəflər')
    development_needs = models.TextField(blank=True, verbose_name='İnkişaf Ehtiyacları')
    development_plan = models.TextField(blank=True, verbose_name='İnkişaf Planı')

    nominated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='succession_nominations', verbose_name='Təqdim Edən')
    nomination_date = models.DateField(auto_now_add=True, verbose_name='Təqdim Tarixi')

    is_active = models.BooleanField(default=True, verbose_name='Aktivdir')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Varislik Namizədi'
        verbose_name_plural = 'Varislik Namizədləri'
        ordering = ['-readiness_score', 'candidate__last_name']
        unique_together = ['critical_role', 'candidate']

    def __str__(self):
        return f"{self.candidate.get_full_name()} → {self.critical_role.position.title}"


class CompetencyGap(models.Model):
    """
    Gap analysis between current competency levels and target/required levels.
    """
    GAP_STATUS_CHOICES = [
        ('no_gap', 'Boşluq Yoxdur'),
        ('minor_gap', 'Kiçik Boşluq'),
        ('moderate_gap', 'Orta Boşluq'),
        ('major_gap', 'Böyük Boşluq'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competency_gaps', verbose_name='İstifadəçi')
    competency = models.ForeignKey('competencies.Competency', on_delete=models.CASCADE, related_name='identified_gaps', verbose_name='Kompetensiya')

    current_level = models.ForeignKey(
        'competencies.ProficiencyLevel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_level_gaps',
        verbose_name='Cari Səviyyə'
    )
    target_level = models.ForeignKey(
        'competencies.ProficiencyLevel',
        on_delete=models.CASCADE,
        related_name='target_level_gaps',
        verbose_name='Hədəf Səviyyə'
    )

    current_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        verbose_name='Cari Bal'
    )
    target_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Hədəf Bal'
    )
    gap_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Boşluq Balı',
        help_text='Hədəf bal - Cari bal'
    )

    gap_status = models.CharField(max_length=20, choices=GAP_STATUS_CHOICES, default='moderate_gap', verbose_name='Boşluq Statusu')

    target_position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Hədəf Vəzifə',
        help_text='Bu boşluq hansı vəzifə üçün müəyyən edilib'
    )

    recommended_actions = models.TextField(blank=True, verbose_name='Tövsiyə olunan Tədbirlər')
    recommended_trainings = models.ManyToManyField('training.TrainingResource', blank=True, verbose_name='Tövsiyə olunan Təlimlər')

    priority = models.CharField(
        max_length=10,
        choices=[
            ('low', 'Aşağı'),
            ('medium', 'Orta'),
            ('high', 'Yüksək'),
            ('urgent', 'Təcili'),
        ],
        default='medium',
        verbose_name='Prioritet'
    )

    identified_date = models.DateField(auto_now_add=True, verbose_name='Müəyyən edilmə Tarixi')
    target_close_date = models.DateField(null=True, blank=True, verbose_name='Hədəf Bağlanma Tarixi')

    is_closed = models.BooleanField(default=False, verbose_name='Bağlandı')
    closed_date = models.DateField(null=True, blank=True, verbose_name='Bağlanma Tarixi')
    closure_notes = models.TextField(blank=True, verbose_name='Bağlanma Qeydləri')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Kompetensiya Boşluğu'
        verbose_name_plural = 'Kompetensiya Boşluqları'
        ordering = ['-priority', '-gap_score', 'user__last_name']
        indexes = [
            models.Index(fields=['user', '-gap_score']),
            models.Index(fields=['priority', '-identified_date']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.competency.name} (Boşluq: {self.gap_score})"

    def save(self, *args, **kwargs):
        # Auto-calculate gap score
        self.gap_score = self.target_score - self.current_score

        # Auto-determine gap status
        if self.gap_score <= 0:
            self.gap_status = 'no_gap'
        elif self.gap_score <= 20:
            self.gap_status = 'minor_gap'
        elif self.gap_score <= 40:
            self.gap_status = 'moderate_gap'
        else:
            self.gap_status = 'major_gap'

        super().save(*args, **kwargs)
