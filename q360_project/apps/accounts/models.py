"""
Models for accounts app - User management, roles, and permissions.
"""
from django.contrib.auth.models import (
    AbstractUser,
    Group,
    Permission,
    UserManager as DjangoUserManager,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class _CallableRoleCheck:
    """
    Wrapper so role helper methods can be used both as callables and booleans.
    Allows templates to use ``user.is_admin`` while Python code can still call
    ``user.is_admin()`` without breaking backwards compatibility.
    """

    __slots__ = ("_instance", "_func")

    def __init__(self, instance, func):
        self._instance = instance
        self._func = func

    def __call__(self):
        return self._func(self._instance)

    def __bool__(self):
        return bool(self._func(self._instance))

    __nonzero__ = __bool__  # Python 2 compatibility (harmless in Py3)


class role_check:
    """Descriptor decorator that returns _CallableRoleCheck wrappers."""

    def __init__(self, func):
        self.func = func
        self.__doc__ = getattr(func, "__doc__", "")

    def __get__(self, instance, owner):
        if instance is None:
            return self.func
        return _CallableRoleCheck(instance, self.func)


class Q360UserManager(DjangoUserManager):
    """
    Custom user manager that understands legacy boolean flags like ``is_admin``.
    Normalises these flags into the canonical ``role`` field to avoid TypeError
    during user creation in seeds/tests and keeps role permissions in sync.
    """

    def _extract_role(self, extra_fields):
        """Translate legacy helpers into the canonical role string."""
        # Pop legacy flags so Django's AbstractUser manager doesn't raise.
        is_superadmin = extra_fields.pop("is_superadmin", None)
        is_admin = extra_fields.pop("is_admin", None)
        is_manager = extra_fields.pop("is_manager", None)

        role = extra_fields.get("role")
        if role:
            return role

        if is_superadmin:
            return "superadmin"
        if is_admin:
            return "admin"
        if is_manager:
            return "manager"
        return "employee"

    def create_user(self, username, email=None, password=None, **extra_fields):
        role = self._extract_role(extra_fields)
        extra_fields["role"] = role
        user = super().create_user(username, email=email, password=password, **extra_fields)
        self._apply_role_defaults(user)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # Force superadmin role for canonical behaviour.
        extra_fields["role"] = "superadmin"
        user = super().create_superuser(username, email=email, password=password, **extra_fields)
        self._apply_role_defaults(user)
        return user

    def _apply_role_defaults(self, user):
        """Apply default Django auth flags/permissions for the user's role."""
        from apps.accounts.rbac import RoleManager

        RoleManager.assign_default_permissions(user)


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

    objects = Q360UserManager()

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

    @role_check
    def is_superadmin(self):
        """
        Check if user is a superadmin.
        DEPRECATED: Use RoleManager.is_superadmin(user) instead.
        """
        from apps.accounts.rbac import RoleManager
        return RoleManager.is_superadmin(self)

    @role_check
    def is_admin(self):
        """
        Check if user is an admin or higher.
        DEPRECATED: Use RoleManager.is_admin(user) instead.
        """
        from apps.accounts.rbac import RoleManager
        return RoleManager.is_admin(self)

    @role_check
    def is_manager(self):
        """
        Check if user is a manager or higher.
        DEPRECATED: Use RoleManager.is_manager(user) instead.
        """
        from apps.accounts.rbac import RoleManager
        return RoleManager.is_manager(self)

    def get_subordinates(self):
        """Get all subordinates of this user."""
        return User.objects.filter(supervisor=self)

    def can_evaluate(self, other_user):
        """
        Check if this user can evaluate another user.
        DEPRECATED: Use RoleManager.can_evaluate(evaluator, evaluatee) instead.
        """
        from apps.accounts.rbac import RoleManager
        return RoleManager.can_evaluate(self, other_user)

    def get_permission_checker(self):
        """
        Get a PermissionChecker instance for this user.
        Recommended way to check permissions.

        Example:
            permissions = user.get_permission_checker()
            if permissions.can('can_manage_users'):
                # Do something
        """
        from apps.accounts.rbac import PermissionChecker
        return PermissionChecker(self)


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

    # Personal information
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Doğum Tarixi')
    )
    place_of_birth = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Doğum Yeri')
    )
    nationality = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Vətəndaşlıq')
    )
    national_id = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Şəxsiyyət Vəsiqəsi')
    )
    marital_status = models.CharField(
        max_length=20,
        choices=[
            ('single', 'Subay'),
            ('married', 'Evli'),
            ('divorced', 'Boşanmış'),
            ('widowed', 'Dul')
        ],
        blank=True,
        verbose_name=_('Ailə Vəziyyəti')
    )
    number_of_children = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Uşaq Sayı')
    )

    # Professional information
    hire_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('İşə Qəbul Tarixi')
    )
    probation_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Sınaq Müddəti Bitmə Tarixi')
    )
    contract_type = models.CharField(
        max_length=50,
        choices=[
            ('permanent', 'Daimi'),
            ('temporary', 'Müvəqqəti'),
            ('contract', 'Müqavilə'),
            ('probation', 'Sınaq Müddəti')
        ],
        default='permanent',
        verbose_name=_('Müqavilə Növü')
    )
    contract_start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Müqavilə Başlanğıc Tarixi')
    )
    contract_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Müqavilə Bitmə Tarixi')
    )
    termination_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('İşdən Çıxma Tarixi')
    )
    termination_reason = models.TextField(
        blank=True,
        verbose_name=_('İşdən Çıxma Səbəbi')
    )

    # Education
    education_level = models.CharField(
        max_length=100,
        choices=[
            ('high_school', 'Orta Məktəb'),
            ('vocational', 'Texniki'),
            ('bachelor', 'Bakalavr'),
            ('master', 'Magistr'),
            ('phd', 'PhD/Doktorantura')
        ],
        blank=True,
        verbose_name=_('Təhsil Səviyyəsi')
    )
    specialization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('İxtisas')
    )
    university = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Universitet')
    )
    graduation_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Məzuniyyət İli')
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
    personal_email = models.EmailField(
        blank=True,
        verbose_name=_('Şəxsi E-poçt')
    )
    personal_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Şəxsi Telefon')
    )
    address = models.TextField(
        blank=True,
        verbose_name=_('Ünvan')
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Şəhər')
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Poçt Kodu')
    )

    # Emergency contact
    emergency_contact_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Fövqəladə Əlaqə Adı')
    )
    emergency_contact_relationship = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Qohumluq Əlaqəsi')
    )
    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Fövqəladə Əlaqə Telefonu')
    )

    # Insurance & Benefits
    health_insurance_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Tibbi Sığorta Nömrəsi')
    )
    health_insurance_provider = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Tibbi Sığorta Təminatçısı')
    )
    pension_insurance_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Pensiya Sığortası Nömrəsi')
    )
    tax_id = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Vergi Nömrəsi')
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

# Import extended models
from .models_extended import EmployeeDocument, WorkHistory
