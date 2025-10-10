"""Admin configuration for support app."""
from django.contrib import admin
from django.utils.html import format_html
from .models import SupportTicket, TicketComment


class TicketCommentInline(admin.TabularInline):
    """Inline admin for ticket comments."""
    model = TicketComment
    extra = 1
    fields = ['comment', 'created_by', 'is_internal', 'created_at']
    readonly_fields = ['created_at']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    """Admin for support tickets."""

    list_display = ['title', 'status_badge', 'priority_badge', 'created_by', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']
    inlines = [TicketCommentInline]

    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('title', 'description', 'status', 'priority')
        }),
        ('Təyin', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Tarixlər', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        """Display colored status badge."""
        colors = {
            'open': '#17a2b8',
            'in_progress': '#ffc107',
            'resolved': '#28a745',
            'closed': '#6c757d'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def priority_badge(self, obj):
        """Display colored priority badge."""
        colors = {
            'low': '#28a745',
            'medium': '#ffc107',
            'high': '#fd7e14',
            'urgent': '#dc3545'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.priority, '#6c757d'),
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Prioritet'


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    """Admin for ticket comments."""

    list_display = ['ticket', 'comment_preview', 'created_by', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['comment', 'ticket__title']
    readonly_fields = ['created_at']

    def comment_preview(self, obj):
        """Display comment preview."""
        preview = obj.comment[:60] + '...' if len(obj.comment) > 60 else obj.comment
        return preview
    comment_preview.short_description = 'Şərh'
