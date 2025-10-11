from django.contrib import admin
from .models import Notification, EmailTemplate, EmailLog


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    actions = ['mark_as_read', 'mark_as_unread', 'delete_notifications']
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']

    def mark_as_read(self, request, queryset):
        """Bulk mark notifications as read."""
        updated = queryset.update(is_read=True)
        self.message_user(
            request,
            f'{updated} bildiriş oxunmuş kimi qeyd edildi.',
            level='SUCCESS'
        )
    mark_as_read.short_description = 'Seçilmiş bildirişləri oxunmuş kimi qeyd et'

    def mark_as_unread(self, request, queryset):
        """Bulk mark notifications as unread."""
        updated = queryset.update(is_read=False)
        self.message_user(
            request,
            f'{updated} bildiriş oxunmamış kimi qeyd edildi.',
            level='INFO'
        )
    mark_as_unread.short_description = 'Seçilmiş bildirişləri oxunmamış kimi qeyd et'

    def delete_notifications(self, request, queryset):
        """Bulk delete notifications."""
        count = queryset.count()
        queryset.delete()
        self.message_user(
            request,
            f'{count} bildiriş silindi.',
            level='WARNING'
        )
    delete_notifications.short_description = 'Seçilmiş bildirişləri sil'


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    actions = ['activate_templates', 'deactivate_templates']
    list_display = ['name', 'subject', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'subject']

    def activate_templates(self, request, queryset):
        """Bulk activate email templates."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} e-poçt şablonu aktiv edildi.',
            level='SUCCESS'
        )
    activate_templates.short_description = 'Seçilmiş şablonları aktiv et'

    def deactivate_templates(self, request, queryset):
        """Bulk deactivate email templates."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} e-poçt şablonu deaktiv edildi.',
            level='WARNING'
        )
    deactivate_templates.short_description = 'Seçilmiş şablonları deaktiv et'


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['recipient_email', 'subject', 'status', 'sent_at', 'opened_at', 'created_at']
    list_filter = ['status', 'created_at', 'sent_at']
    search_fields = ['recipient_email', 'subject']
    readonly_fields = ['created_at', 'sent_at', 'opened_at', 'clicked_at']
