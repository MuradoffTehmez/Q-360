"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from .models import User, Profile, Role


@admin.register(Role)
class RoleAdmin(SimpleHistoryAdmin):
    """Admin interface for Role model."""

    list_display = ['name', 'display_name', 'created_at']
    search_fields = ['name', 'display_name']
    list_filter = ['name', 'created_at']
    filter_horizontal = ['permissions']


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


@admin.register(User)
class UserAdmin(BaseUserAdmin, SimpleHistoryAdmin):
    """Admin interface for User model."""

    inlines = [ProfileInline]
    list_display = [
        'username', 'get_full_name', 'email', 'role',
        'department', 'position', 'is_active', 'date_joined'
    ]
    list_filter = ['role', 'is_active', 'is_staff', 'department', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'employee_id']
    ordering = ['last_name', 'first_name']
    readonly_fields = ['date_joined', 'last_login']

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
        (_('Tarixlər'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

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

    def get_full_name(self, obj):
        """Display full name."""
        return obj.get_full_name()
    get_full_name.short_description = 'Ad Soyad'


@admin.register(Profile)
class ProfileAdmin(SimpleHistoryAdmin):
    """Admin interface for Profile model."""

    list_display = ['user', 'hire_date', 'education_level', 'work_email']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'work_email']
    list_filter = ['education_level', 'language_preference', 'hire_date']
    readonly_fields = ['created_at', 'updated_at', 'years_of_service']

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
