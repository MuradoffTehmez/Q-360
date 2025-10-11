"""
Admin configuration for departments app.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Organization, Department, Position


@admin.register(Organization)
class OrganizationAdmin(SimpleHistoryAdmin):
    """Admin interface for Organization model."""

    actions = ['activate_organizations', 'deactivate_organizations']
    list_display = ['name', 'short_name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active', 'established_date']
    search_fields = ['name', 'short_name', 'code']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Əsas Məlumatlar'), {
            'fields': ('name', 'short_name', 'code', 'description')
        }),
        (_('Əlaqə Məlumatları'), {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        (_('Status'), {
            'fields': ('is_active', 'established_date')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def activate_organizations(self, request, queryset):
        """Bulk activate organizations."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} təşkilat aktiv edildi.',
            level='SUCCESS'
        )
    activate_organizations.short_description = 'Seçilmiş təşkilatları aktiv et'

    def deactivate_organizations(self, request, queryset):
        """Bulk deactivate organizations."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} təşkilat deaktiv edildi.',
            level='WARNING'
        )
    deactivate_organizations.short_description = 'Seçilmiş təşkilatları deaktiv et'


@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin, SimpleHistoryAdmin):
    """Admin interface for Department model with MPTT support."""

    actions = ['activate_departments', 'deactivate_departments']
    list_display = ['name', 'code', 'organization', 'parent', 'head', 'is_active']
    list_filter = ['organization', 'is_active', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at', 'level', 'lft', 'rght', 'tree_id']
    autocomplete_fields = ['head']

    fieldsets = (
        (_('Əsas Məlumatlar'), {
            'fields': ('organization', 'parent', 'name', 'code', 'description')
        }),
        (_('Əlaqə Məlumatları'), {
            'fields': ('phone', 'email', 'location')
        }),
        (_('Rəhbərlik'), {
            'fields': ('head',)
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
        (_('Ağac Strukturu'), {
            'fields': ('level', 'lft', 'rght', 'tree_id'),
            'classes': ('collapse',)
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    mptt_level_indent = 20

    def activate_departments(self, request, queryset):
        """Bulk activate departments."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} departament aktiv edildi.',
            level='SUCCESS'
        )
    activate_departments.short_description = 'Seçilmiş departamentləri aktiv et'

    def deactivate_departments(self, request, queryset):
        """Bulk deactivate departments."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} departament deaktiv edildi.',
            level='WARNING'
        )
    deactivate_departments.short_description = 'Seçilmiş departamentləri deaktiv et'


@admin.register(Position)
class PositionAdmin(SimpleHistoryAdmin):
    """Admin interface for Position model."""

    actions = ['activate_positions', 'deactivate_positions']
    list_display = ['title', 'code', 'organization', 'department', 'level', 'is_active']
    list_filter = ['organization', 'level', 'is_active', 'created_at']
    search_fields = ['title', 'code']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Əsas Məlumatlar'), {
            'fields': ('organization', 'department', 'title', 'code', 'description')
        }),
        (_('Vəzifə Detalları'), {
            'fields': ('responsibilities', 'level', 'reports_to')
        }),
        (_('Tələblər'), {
            'fields': ('required_education', 'required_experience')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def activate_positions(self, request, queryset):
        """Bulk activate positions."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} vəzifə aktiv edildi.',
            level='SUCCESS'
        )
    activate_positions.short_description = 'Seçilmiş vəzifələri aktiv et'

    def deactivate_positions(self, request, queryset):
        """Bulk deactivate positions."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} vəzifə deaktiv edildi.',
            level='WARNING'
        )
    deactivate_positions.short_description = 'Seçilmiş vəzifələri deaktiv et'
