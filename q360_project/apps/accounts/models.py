"""
Models for accounts app - User management, roles, and permissions.
"""
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Role(models.Model):
    """
    Role model for defining user roles in the system.
    Supports hierarchical role-based access control.
    """

    ROLE_CHOICES = [
        ('superadmin', 'Super Administrator'),
        ('admin', 'Administrator'),
        ('manager', 'Menecer'),
        ('employee', 'İşçi'),
    ]

    name = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        unique=True,
        verbose_name=_('Rol Adı')
    )
    display_name = models.CharField(
        max_length=100,
        verbose_name=_('Göstəriləcək Ad')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_roles',
        verbose_name=_('İcazələr')
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
        verbose_name = _('Rol')
        verbose_name_plural = _('Rollar')
        ordering = ['name']

    def __str__(self):
        return self.display_name


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes role-based access control and organizational hierarchy.
    """

    ROLE_CHOICES = [
        ('superadmin', 'Super Administrator'),
        ('admin', 'Administrator'),
        ('manager', 'Menecer'),
        ('employee', 'İşçi'),
    ]

    # Role and organizational information
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee',
        verbose_name=_('Rol')
    )
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name=_('Şöbə')
    )
    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Vəzifə')
    )

    # Personal information
    middle_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Ata adı')
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Telefon')
    )
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_('İşçi ID')
    )

    # Profile information
    profile_picture = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True,
        verbose_name=_('Profil Şəkli')
    )
    bio = models.TextField(
        blank=True,
        verbose_name=_('Haqqında')
    )

    # Supervisor hierarchy
    supervisor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        verbose_name=_('Rəhbər')
    )

    # Activity tracking
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Qoşulma Tarixi')
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Son Giriş')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('İstifadəçi')
        verbose_name_plural = _('İstifadəçilər')
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['role']),
            models.Index(fields=['department']),
        ]

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username

    def get_full_name(self):
        """Return the user's full name including middle name."""
        parts = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(filter(None, parts))

    def is_superadmin(self):
        """Check if user is a superadmin."""
        return self.role == 'superadmin'

    def is_admin(self):
        """Check if user is an admin."""
        return self.role in ['superadmin', 'admin']

    def is_manager(self):
        """Check if user is a manager."""
        return self.role in ['superadmin', 'admin', 'manager']

    def get_subordinates(self):
        """Get all subordinates of this user."""
        return User.objects.filter(supervisor=self)

    def can_evaluate(self, other_user):
        """
        Check if this user can evaluate another user.
        Rules:
        - Superadmin can evaluate anyone
        - Manager can evaluate subordinates
        - Employees can evaluate peers and supervisor (in peer/upward evaluation)
        """
        if self.is_superadmin():
            return True
        if self.is_manager() and other_user.supervisor == self:
            return True
        if other_user.department == self.department:
            return True
        return False


class Profile(models.Model):
    """
    Extended profile information for users.
    Stores additional metadata not in the core User model.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('İstifadəçi')
    )

    # Professional information
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Doğum Tarixi')
    )
    hire_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('İşə Qəbul Tarixi')
    )
    education_level = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Təhsil Səviyyəsi')
    )
    specialization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('İxtisas')
    )

    # Contact information
    work_email = models.EmailField(
        blank=True,
        verbose_name=_('İş E-poçtu')
    )
    work_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('İş Telefonu')
    )
    address = models.TextField(
        blank=True,
        verbose_name=_('Ünvan')
    )

    # System preferences
    language_preference = models.CharField(
        max_length=10,
        default='az',
        choices=[('az', 'Azərbaycan'), ('en', 'English'), ('ru', 'Русский')],
        verbose_name=_('Dil Seçimi')
    )
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_('E-poçt Bildirişləri')
    )
    sms_notifications = models.BooleanField(
        default=False,
        verbose_name=_('SMS Bildirişləri')
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
        verbose_name = _('Profil')
        verbose_name_plural = _('Profillər')

    def __str__(self):
        return f"{self.user.get_full_name()} - Profil"

    @property
    def years_of_service(self):
        """Calculate years of service."""
        if self.hire_date:
            from datetime import date
            today = date.today()
            years = today.year - self.hire_date.year
            if today.month < self.hire_date.month or \
               (today.month == self.hire_date.month and today.day < self.hire_date.day):
                years -= 1
            return years
        return 0
