from django.contrib import admin
from .models import QuickFeedback, FeedbackBank, PublicRecognition, RecognitionLike, RecognitionComment, FeedbackTag


@admin.register(QuickFeedback)
class QuickFeedbackAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'feedback_type', 'visibility', 'title', 'is_read', 'created_at']
    list_filter = ['feedback_type', 'visibility', 'is_read', 'is_anonymous', 'is_flagged', 'created_at']
    search_fields = ['sender__first_name', 'sender__last_name', 'recipient__first_name', 'recipient__last_name', 'title', 'message']
    readonly_fields = ['created_at', 'updated_at', 'read_at', 'responded_at']
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'


@admin.register(FeedbackBank)
class FeedbackBankAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_feedbacks_received', 'total_recognitions', 'total_improvements', 'average_rating', 'last_feedback_date']
    list_filter = ['last_feedback_date']
    search_fields = ['user__first_name', 'user__last_name']
    readonly_fields = ['total_feedbacks_received', 'total_recognitions', 'total_improvements', 'average_rating', 'last_feedback_date', 'last_updated', 'created_at']


@admin.register(PublicRecognition)
class PublicRecognitionAdmin(admin.ModelAdmin):
    list_display = ['feedback', 'likes_count', 'comments_count', 'views_count', 'is_featured', 'published_at']
    list_filter = ['is_featured', 'published_at']
    search_fields = ['feedback__title', 'feedback__message']
    readonly_fields = ['likes_count', 'comments_count', 'views_count', 'published_at']
    date_hierarchy = 'published_at'


@admin.register(RecognitionLike)
class RecognitionLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'recognition', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__first_name', 'user__last_name']
    readonly_fields = ['created_at']


@admin.register(RecognitionComment)
class RecognitionCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'recognition', 'comment', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__first_name', 'user__last_name', 'comment']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FeedbackTag)
class FeedbackTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'usage_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['usage_count', 'created_at']
