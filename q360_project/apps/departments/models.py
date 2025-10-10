"""
Models for departments app - Organizational structure management.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from mptt.models import MPTTModel, TreeForeignKey


class Organization(models.Model):
    """
    Represents a government organization (ministry, agency, etc.).
    Top-level entity in the organizational hierarchy.
    """

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Təşkilat Adı')
    )
    short_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Qısa Ad')
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Təşkilat Kodu')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )

    # Contact information
    address = models.TextField(
        blank=True,
        verbose_name=_('Ünvan')
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Telefon')
    )
    email = models.EmailField(
        blank=True,
        verbose_name=_('E-poçt')
    )
    website = models.URLField(
        blank=True,
        verbose_name=_('Veb Sayt')
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )
    established_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Təsis Tarixi')
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
        verbose_name = _('Təşkilat')
        verbose_name_plural = _('Təşkilatlar')
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.short_name if self.short_name else self.name

    def get_total_employees(self):
        """Get total number of employees in this organization."""
        return self.departments.aggregate(
            total=models.Count('users')
        )['total'] or 0


class Department(MPTTModel):
    """
    Represents a department within an organization.
    Uses MPTT (Modified Preorder Tree Traversal) for hierarchical structure.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='departments',
        verbose_name=_('Təşkilat')
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Üst Şöbə')
    )

    # Department information
    name = models.CharField(
        max_length=200,
        verbose_name=_('Şöbə Adı')
    )
    code = models.CharField(
        max_length=20,
        verbose_name=_('Şöbə Kodu')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )

    # Contact information
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Telefon')
    )
    email = models.EmailField(
        blank=True,
        verbose_name=_('E-poçt')
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Yerləşmə')
    )

    # Head of department
    head = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments',
        verbose_name=_('Şöbə Rəhbəri')
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
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

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Şöbə')
        verbose_name_plural = _('Şöbələr')
        unique_together = [['organization', 'code']]
        ordering = ['tree_id', 'lft']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.organization.short_name} - {self.name}"

    def get_full_path(self):
        """Get full hierarchical path of the department."""
        ancestors = self.get_ancestors(include_self=True)
        return ' > '.join([dept.name for dept in ancestors])

    def get_employee_count(self):
        """Get number of employees in this department."""
        return self.users.filter(is_active=True).count()

    def get_all_employees(self):
        """Get all employees including sub-departments."""
        from apps.accounts.models import User
        department_ids = self.get_descendants(include_self=True).values_list('id', flat=True)
        return User.objects.filter(department_id__in=department_ids, is_active=True)


class Position(models.Model):
    """
    Represents a job position within the organization.
    Defines roles and responsibilities.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name=_('Təşkilat')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='positions',
        verbose_name=_('Şöbə')
    )

    # Position information
    title = models.CharField(
        max_length=200,
        verbose_name=_('Vəzifə Adı')
    )
    code = models.CharField(
        max_length=20,
        verbose_name=_('Vəzifə Kodu')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )
    responsibilities = models.TextField(
        blank=True,
        verbose_name=_('Vəzifə Öhdəlikləri')
    )

    # Position hierarchy
    level = models.IntegerField(
        default=1,
        verbose_name=_('Səviyyə'),
        help_text=_('1=Rəhbərlik, 2=Orta menecment, 3=Əməkdaş')
    )
    reports_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinate_positions',
        verbose_name=_('Hesabat Verir')
    )

    # Requirements
    required_education = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Tələb Olunan Təhsil')
    )
    required_experience = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Tələb Olunan Təcrübə')
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
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

    # history = HistoricalRecords()
    
    history = HistoricalRecords(
        excluded_fields=[
            'lft', 
            'rght', 
            'tree_id', 
            'level'
        ]
    ) 


    class Meta:
        verbose_name = _('Vəzifə')
        verbose_name_plural = _('Vəzifələr')
        unique_together = [['organization', 'code']]
        ordering = ['level', 'title']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['level']),
        ]

    def __str__(self):
        return f"{self.title} ({self.code})"
