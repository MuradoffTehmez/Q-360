from django.contrib import admin
from .models import Notification, EmailTemplate, EmailLog


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'subject']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['recipient_email', 'subject', 'status', 'sent_at', 'opened_at', 'created_at']
    list_filter = ['status', 'created_at', 'sent_at']
    search_fields = ['recipient_email', 'subject']
    readonly_fields = ['created_at', 'sent_at', 'opened_at', 'clicked_at']
