"""Models for development plans app."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class DevelopmentGoal(models.Model):
    """
    Individual development goals based on evaluation results.
    Enhanced with goal cascading functionality for organizational alignment.
    """

    STATUS_CHOICES = [
        ('draft', 'Qaralama'),
        ('pending_approval', 'Təsdiq Gözləyir'),
        ('active', 'Aktiv'),
        ('completed', 'Tamamlanmış'),
        ('cancelled', 'Ləğv Edilmiş'),
        ('rejected', 'Rədd Edilmiş'),
    ]

    GOAL_LEVEL_CHOICES = [
        ('organizational', 'Təşkilati'),
        ('departmental', 'Departament'),
        ('team', 'Komanda'),
        ('individual', 'Fərdi'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='development_goals')
    title = models.CharField(max_length=200, verbose_name=_('Məqsəd'))
    description = models.TextField(verbose_name=_('Təsvir'))
    category = models.CharField(max_length=100, verbose_name=_('Kateqoriya'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    target_date = models.DateField(verbose_name=_('Hədəf Tarixi'))
    completion_date = models.DateField(null=True, blank=True)

    # Goal Cascading Fields
    goal_level = models.CharField(
        max_length=20,
        choices=GOAL_LEVEL_CHOICES,
        default='individual',
        verbose_name=_('Məqsəd Səviyyəsi'),
        help_text=_('Bu məqsədin təşkilati iyerarxiyada yerləşdiyi səviyyə')
    )
    parent_goal = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_goals',
        verbose_name=_('Valideyn Məqsəd'),
        help_text=_('Bu məqsədin əsaslandığı daha yüksək səviyyəli məqsəd')
    )
    alignment_percentage = models.IntegerField(
        default=100,
        verbose_name=_('Uyğunluq Faizi'),
        help_text=_('Bu məqsədin valideyn məqsədə uyğunluq dərəcəsi (0-100)')
    )
    weight_in_parent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_('Valideyn Məqsəddə Çəki'),
        help_text=_('Bu məqsədin valideyn məqsədin nail olunmasındakı payı (%)')
    )

    # Organizational alignment
    related_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='department_goals',
        verbose_name=_('Əlaqəli Departament')
    )
    strategic_objective = models.ForeignKey(
        'development_plans.StrategicObjective',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='aligned_goals',
        verbose_name=_('Strateji Məqsəd')
    )

    # Progress tracking
    progress_percentage = models.IntegerField(
        default=0,
        verbose_name=_('İrəliləyiş Faizi'),
        help_text=_('Məqsədə nail olma faizi (0-100)')
    )

    # Approval workflow (managed via status field)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_goals')
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_note = models.TextField(blank=True, verbose_name=_('Təsdiq Qeydi'))

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_goals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('İnkişaf Məqsədi')
        verbose_name_plural = _('İnkişaf Məqsədləri')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def submit_for_approval(self):
        """
        Submit goal for approval.
        Can only submit from draft status.
        """
        from django.core.exceptions import ValidationError

        if self.status != 'draft':
            raise ValidationError(
                f'Yalnız qaralama statusunda olan məqsədlər təsdiqə göndərilə bilər. '
                f'Hazırki status: {self.get_status_display()}'
            )

        self.status = 'pending_approval'
        self.save()

    def approve(self, approver, note=''):
        """
        Approve the goal.
        Can only approve from pending_approval status.
        """
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        if self.status != 'pending_approval':
            raise ValidationError(
                f'Yalnız təsdiq gözləyən məqsədlər təsdiq edilə bilər. '
                f'Hazırki status: {self.get_status_display()}'
            )

        self.status = 'active'
        self.approved_by = approver
        self.approved_at = timezone.now()
        self.approval_note = note
        self.save()

    def reject(self, rejector, note=''):
        """
        Reject the goal.
        Can only reject from pending_approval status.
        """
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        if self.status != 'pending_approval':
            raise ValidationError(
                f'Yalnız təsdiq gözləyən məqsədlər rədd edilə bilər. '
                f'Hazırki status: {self.get_status_display()}'
            )

        self.status = 'rejected'
        self.approved_by = rejector
        self.approved_at = timezone.now()
        self.approval_note = note
        self.save()

    def mark_completed(self, completion_note=''):
        """
        Mark goal as completed.
        Can only complete active goals.
        """
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        if self.status != 'active':
            raise ValidationError(
                f'Yalnız aktiv məqsədlər tamamlana bilər. '
                f'Hazırki status: {self.get_status_display()}'
            )

        self.status = 'completed'
        self.completion_date = timezone.now().date()
        self.approval_note = completion_note
        self.save()

    def cancel(self, cancel_note=''):
        """
        Cancel the goal.
        Can cancel from any status except completed.
        """
        from django.core.exceptions import ValidationError

        if self.status == 'completed':
            raise ValidationError('Tamamlanmış məqsədlər ləğv edilə bilməz.')

        self.status = 'cancelled'
        self.approval_note = cancel_note
        self.save()

    def get_goal_hierarchy(self):
        """
        Get complete goal hierarchy (ancestors and descendants).
        Returns dict with ancestors, current goal, and descendants.
        """
        # Get all ancestors
        ancestors = []
        current = self.parent_goal
        while current:
            ancestors.append(current)
            current = current.parent_goal
        ancestors.reverse()  # Top-down order

        # Get all descendants
        descendants = list(self.child_goals.all())

        # Recursively get sub-goals
        def get_all_descendants(goal):
            result = []
            for child in goal.child_goals.all():
                result.append(child)
                result.extend(get_all_descendants(child))
            return result

        all_descendants = get_all_descendants(self)

        return {
            'ancestors': ancestors,
            'current': self,
            'direct_children': descendants,
            'all_descendants': all_descendants,
            'depth': len(ancestors),
            'total_descendants': len(all_descendants)
        }

    def calculate_cascaded_progress(self):
        """
        Calculate progress based on child goals weighted contribution.
        If goal has children, progress is weighted average of child progress.
        """
        children = self.child_goals.filter(status='active')

        if not children.exists():
            return self.progress_percentage

        total_weight = sum(float(child.weight_in_parent) for child in children)

        if total_weight == 0:
            # If no weights assigned, use equal weights
            weighted_progress = sum(child.progress_percentage for child in children) / children.count()
        else:
            # Calculate weighted average
            weighted_progress = sum(
                child.progress_percentage * (float(child.weight_in_parent) / total_weight)
                for child in children
            )

        return round(weighted_progress, 2)

    def update_progress_from_children(self):
        """
        Update this goal's progress based on child goals.
        Useful for automatic progress tracking in cascaded goals.
        """
        new_progress = self.calculate_cascaded_progress()
        self.progress_percentage = int(new_progress)
        self.save()

        # Recursively update parent if exists
        if self.parent_goal:
            self.parent_goal.update_progress_from_children()

    def validate_cascading_integrity(self):
        """
        Validate goal cascading integrity.
        Checks for circular references and weight consistency.
        """
        from django.core.exceptions import ValidationError

        # Check for circular reference
        visited = set()
        current = self.parent_goal
        while current:
            if current.id in visited:
                raise ValidationError('Dövri asılılıq aşkar edildi. Məqsəd öz özünün vali növü ola bilməz.')
            visited.add(current.id)
            current = current.parent_goal

        # Check weight consistency for children
        if self.child_goals.exists():
            total_weight = sum(float(child.weight_in_parent) for child in self.child_goals.all())
            if total_weight > 100:
                raise ValidationError(
                    f'Uşaq məqsədlərin ümumi çəkisi 100%-dən çox ola bilməz. Hazırda: {total_weight}%'
                )

    def get_alignment_chain(self):
        """
        Get alignment chain showing how this goal aligns with organizational objectives.
        """
        chain = []
        current = self

        while current:
            chain.append({
                'goal': current,
                'level': current.goal_level,
                'title': current.title,
                'progress': current.progress_percentage,
                'alignment': current.alignment_percentage
            })
            current = current.parent_goal

        chain.reverse()
        return chain

    def cascade_to_team(self, team_members, weight_per_member=None):
        """
        Cascade this goal to team members as individual goals.

        Args:
            team_members: List of User instances
            weight_per_member: Optional dict mapping user_id to weight percentage
        """
        if not team_members:
            return []

        created_goals = []
        default_weight = 100 / len(team_members)

        for member in team_members:
            weight = weight_per_member.get(member.id, default_weight) if weight_per_member else default_weight

            child_goal = DevelopmentGoal.objects.create(
                user=member,
                title=f"{self.title} - {member.get_full_name()}",
                description=f"Kaskadlaşdırılmış məqsəd: {self.description}",
                category=self.category,
                status='draft',
                target_date=self.target_date,
                goal_level='individual',
                parent_goal=self,
                alignment_percentage=100,
                weight_in_parent=weight,
                related_department=self.related_department,
                strategic_objective=self.strategic_objective,
                created_by=self.user
            )
            created_goals.append(child_goal)

        return created_goals


class ProgressLog(models.Model):
    """Progress tracking for development goals."""

    goal = models.ForeignKey(DevelopmentGoal, on_delete=models.CASCADE, related_name='progress_logs')
    note = models.TextField(verbose_name=_('Qeyd'))
    progress_percentage = models.IntegerField(default=0, verbose_name=_('İrəliləyiş %'))
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_draft = models.BooleanField(default=False, verbose_name=_('Layihə'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('İrəliləyiş Qeydi')
        verbose_name_plural = _('İrəliləyiş Qeydləri')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.goal.title} - {self.progress_percentage}%"


# Import OKR models
from .models_okr import StrategicObjective, KeyResult, KPI, KPIMeasurement
