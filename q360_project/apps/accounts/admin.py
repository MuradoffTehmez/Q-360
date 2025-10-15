"""
Professional admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from simple_history.admin import SimpleHistoryAdmin

from .models import User, Profile, Role


@admin.register(Role)
class RoleAdmin(SimpleHistoryAdmin):
    """Professional admin interface for Role model."""

    list_display = ['name', 'display_name', 'users_count', 'created_at']
    search_fields = ['name', 'display_name']
    list_filter = ['name', 'created_at']
    filter_horizontal = ['permissions']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Rol Məlumatları'), {
            'fields': ('name', 'display_name')
        }),
        (_('İcazələr'), {
            'fields': ('permissions',)
        }),
        (_('Tarixlər'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def users_count(self, obj):
        """Display users count with this role."""
        # Role is stored as CharField in User model, not ForeignKey
        from apps.accounts.models import User
        count = User.objects.filter(role=obj.name).count()
        return format_html(
            '<span style="background: #007bff; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px;">{}</span>',
            count
        )
    users_count.short_description = 'İstifadəçi Sayı'


class ProfileInline(admin.StackedInline):
    """Inline admin for Profile model."""

    model = Profile
    can_delete = False
    verbose_name = 'Profil'
    verbose_name_plural = 'Profil'
    fk_name = 'user'
    fields = [
        'date_of_birth', 'hire_date', 'education_level', 'specialization',
        'work_email', 'work_phone', 'address', 'language_preference',
        'email_notifications', 'sms_notifications'
    ]

    def get_or_create_profile(self, obj):
        """Ensure profile exists before inline form is rendered."""
        if obj.pk and not hasattr(obj, 'profile'):
            Profile.objects.get_or_create(user=obj)

    def get_formset(self, request, obj=None, **kwargs):
        """Override to ensure profile exists."""
        if obj:
            self.get_or_create_profile(obj)
        return super().get_formset(request, obj, **kwargs)


@admin.register(User)
class UserAdmin(BaseUserAdmin, SimpleHistoryAdmin):
    """Professional admin interface for User model."""

    inlines = [ProfileInline]
    list_display = [
        'username', 'full_name_with_badge', 'email', 'role_badge',
        'department_link', 'position', 'status_badge', 'date_joined'
    ]
    list_filter = ['role', 'is_active', 'is_staff', 'department', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'employee_id']
    autocomplete_fields = []  # Required for Profile autocomplete
    ordering = ['last_name', 'first_name']
    readonly_fields = ['date_joined', 'last_login', 'user_statistics']

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Şəxsi Məlumatlar'), {
            'fields': ('first_name', 'middle_name', 'last_name', 'email', 'phone_number')
        }),
        (_('Təşkilati Məlumatlar'), {
            'fields': ('role', 'department', 'position', 'employee_id', 'supervisor')
        }),
        (_('Profil'), {
            'fields': ('profile_picture', 'bio')
        }),
        (_('İcazələr'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Statistika'), {
            'fields': ('user_statistics',),
            'classes': ('collapse',)
        }),
        (_('Tarixlər'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_users', 'deactivate_users', 'reset_passwords']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'email',
                'first_name', 'middle_name', 'last_name',
                'role', 'department', 'position', 'employee_id'
            ),
        }),
    )

    def activate_users(self, request, queryset):
        """Bulk activate selected users."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} istifadəçi aktivləşdirildi.',
            level='SUCCESS'
        )
    activate_users.short_description = 'Seçilmiş istifadəçiləri aktiv et'

    def deactivate_users(self, request, queryset):
        """Bulk deactivate selected users."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} istifadəçi deaktiv edildi.',
            level='WARNING'
        )
    deactivate_users.short_description = 'Seçilmiş istifadəçiləri deaktiv et'

    def reset_passwords(self, request, queryset):
        """Bulk reset passwords for selected users."""
        from django.contrib.auth.hashers import make_password
        import secrets
        import string
        
        # Generate a temporary password for each user
        for user in queryset:
            # Create a random temporary password
            temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            user.password = make_password(temp_password)
            user.save()
            
            # Here you would normally send the password via email
            # For now, we'll just log it in the admin message
            self.message_user(
                request,
                f'İstifadəçilər üçün şifrələr sıfırlandı. Hər istifadəçiyə yeni şifrə e-poçt vasitəsilə göndərilməlidir.',
                level='INFO'
            )
    reset_passwords.short_description = 'Seçilmiş istifadəçilərin şifrələrini sıfırla'

    def full_name_with_badge(self, obj):
        """Display full name with superuser badge."""
        name = obj.get_full_name()
        if obj.is_superuser:
            return format_html(
                '{} <span style="background: #dc3545; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; margin-left: 5px;">ADMIN</span>',
                name
            )
        return name
    full_name_with_badge.short_description = 'Ad Soyad'

    def role_badge(self, obj):
        """Display role with colored badge."""
        if not obj.role:
            return '-'
        colors = {
            'superadmin': '#dc3545',
            'admin': '#dc3545',
            'manager': '#ffc107',
            'employee': '#28a745'
        }
        # role is CharField, get display name from choices
        role_display = dict(obj.ROLE_CHOICES).get(obj.role, obj.role)
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold; font-size: 11px;">{}</span>',
            colors.get(obj.role, '#6c757d'),
            role_display
        )
    role_badge.short_description = 'Rol'

    def department_link(self, obj):
        """Display department with link."""
        if not obj.department:
            return '-'
        url = reverse('admin:departments_department_change', args=[obj.department.pk])
        return format_html('<a href="{}">{}</a>', url, obj.department.name)
    department_link.short_description = 'Departament'

    def status_badge(self, obj):
        """Display status badge."""
        if obj.is_active:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">● Aktiv</span>'
            )
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">● Deaktiv</span>'
        )
    status_badge.short_description = 'Status'

    def user_statistics(self, obj):
        """Display user statistics."""
        from apps.evaluations.models import EvaluationAssignment, EvaluationResult

        completed_evaluations = EvaluationAssignment.objects.filter(
            evaluator=obj,
            status='completed'
        ).count()

        pending_evaluations = EvaluationAssignment.objects.filter(
            evaluator=obj,
            status__in=['pending', 'in_progress']
        ).count()

        results = EvaluationResult.objects.filter(evaluatee=obj).order_by('-calculated_at')
        latest_score = results.first().overall_score if results.exists() and results.first().overall_score else None

        subordinates_count = obj.get_subordinates().count() if hasattr(obj, 'get_subordinates') else 0

        stats_html = f"""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
            <h3 style="margin-top: 0;">İstifadəçi Statistikası</h3>
            <table style="width: 100%;">
                <tr>
                    <td><strong>Tamamlanmış Qiymətləndirmələr:</strong></td>
                    <td style="color: #28a745; font-weight: bold;">{completed_evaluations}</td>
                </tr>
                <tr>
                    <td><strong>Gözləyən Qiymətləndirmələr:</strong></td>
                    <td style="color: #ffc107; font-weight: bold;">{pending_evaluations}</td>
                </tr>
                <tr>
                    <td><strong>Son Qiymətləndirmə Nəticəsi:</strong></td>
                    <td style="color: #007bff; font-weight: bold;">{f'{latest_score:.2f}/5' if latest_score else 'N/A'}</td>
                </tr>
                <tr>
                    <td><strong>Tabelik Sayı:</strong></td>
                    <td style="font-weight: bold;">{subordinates_count}</td>
                </tr>
            </table>
        </div>
        """
        return format_html(stats_html)
    user_statistics.short_description = 'Statistika'


@admin.register(Profile)
class ProfileAdmin(SimpleHistoryAdmin):
    """Professional admin interface for Profile model."""

    list_display = [
        'user_link', 'hire_date', 'education_badge',
        'work_email', 'years_display'
    ]
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'work_email']
    list_filter = ['education_level', 'language_preference', 'hire_date']
    readonly_fields = ['created_at', 'updated_at', 'years_of_service']
    raw_id_fields = ['user']  # Changed from autocomplete_fields

    fieldsets = (
        (_('İstifadəçi'), {
            'fields': ('user',)
        }),
        (_('Peşəkar Məlumatlar'), {
            'fields': ('hire_date', 'education_level', 'specialization', 'years_of_service')
        }),
        (_('Əlaqə Məlumatları'), {
            'fields': ('work_email', 'work_phone', 'address')
        }),
        (_('Şəxsi Məlumatlar'), {
            'fields': ('date_of_birth',)
        }),
        (_('Sistem Tənzimləmələri'), {
            'fields': ('language_preference', 'email_notifications', 'sms_notifications')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_link(self, obj):
        """Display user with link."""
        url = reverse('admin:accounts_user_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.get_full_name())
    user_link.short_description = 'İstifadəçi'

    def education_badge(self, obj):
        """Display education level with badge."""
        if not obj.education_level:
            return '-'
        # Simple display without colors since education_level is a CharField
        return format_html(
            '<span style="background: #007bff; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            obj.education_level
        )
    education_badge.short_description = 'Təhsil'

    def years_display(self, obj):
        """Display years of service."""
        years = obj.years_of_service
        if years is None:
            return '-'
        return format_html(
            '<span style="color: #007bff; font-weight: bold;">{} il</span>',
            years
        )
    years_display.short_description = 'İş Təcrübəsi'
