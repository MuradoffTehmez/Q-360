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


@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin, SimpleHistoryAdmin):
    """Admin interface for Department model with MPTT support."""

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


@admin.register(Position)
class PositionAdmin(SimpleHistoryAdmin):
    """Admin interface for Position model."""

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
