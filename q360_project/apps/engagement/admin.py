from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    PulseSurvey, SurveyQuestion, SurveyResponse,
    EngagementScore, Recognition, AnonymousFeedback,
    SentimentAnalysis, GamificationBadge, UserBadge,
    UserPoints, PointsTransaction
)


class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion
    extra = 1
    fields = ['question_text', 'question_type', 'order', 'is_required']


@admin.register(PulseSurvey)
class PulseSurveyAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'survey_type', 'status', 'start_date', 'end_date', 'is_anonymous', 'created_by']
    list_filter = ['survey_type', 'status', 'is_anonymous', 'is_mandatory', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['target_departments', 'target_users']
    inlines = [SurveyQuestionInline]
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'survey_type', 'status')
        }),
        ('Settings', {
            'fields': ('is_anonymous', 'is_mandatory', 'start_date', 'end_date')
        }),
        ('Targeting', {
            'fields': ('target_departments', 'target_users')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ['survey', 'question_text', 'question_type', 'order', 'is_required']
    list_filter = ['question_type', 'is_required', 'survey']
    search_fields = ['question_text']


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['survey', 'user', 'question', 'rating_value', 'submitted_at']
    list_filter = ['survey', 'submitted_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['submitted_at']


@admin.register(EngagementScore)
class EngagementScoreAdmin(SimpleHistoryAdmin):
    list_display = ['user', 'score_type', 'score_value', 'period_start', 'period_end', 'calculated_at']
    list_filter = ['score_type', 'is_promoter', 'is_passive', 'is_detractor', 'calculated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['calculated_at']


@admin.register(Recognition)
class RecognitionAdmin(SimpleHistoryAdmin):
    list_display = ['given_by', 'given_to', 'recognition_type', 'title', 'is_public', 'points', 'likes_count', 'created_at']
    list_filter = ['recognition_type', 'is_public', 'created_at']
    search_fields = ['given_by__username', 'given_to__username', 'title', 'message']
    filter_horizontal = ['liked_by']
    readonly_fields = ['created_at', 'likes_count']


@admin.register(AnonymousFeedback)
class AnonymousFeedbackAdmin(SimpleHistoryAdmin):
    list_display = ['anonymous_id', 'category', 'subject', 'status', 'priority', 'submitted_at', 'sentiment_label']
    list_filter = ['category', 'status', 'priority', 'sentiment_label', 'submitted_at']
    search_fields = ['subject', 'message', 'anonymous_id']
    readonly_fields = ['anonymous_id', 'submitted_at', 'updated_at', 'sentiment_score', 'sentiment_label']

    fieldsets = (
        ('Feedback Information', {
            'fields': ('anonymous_id', 'category', 'subject', 'message', 'department')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Response', {
            'fields': ('response', 'responded_by', 'responded_at')
        }),
        ('Sentiment Analysis', {
            'fields': ('sentiment_score', 'sentiment_label'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ['source_type', 'source_id', 'sentiment', 'sentiment_score', 'confidence', 'analyzed_at']
    list_filter = ['source_type', 'sentiment', 'analyzed_at']
    search_fields = ['text_content']
    readonly_fields = ['analyzed_at']


@admin.register(GamificationBadge)
class GamificationBadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'icon', 'points_value', 'is_active', 'is_rare', 'created_at']
    list_filter = ['category', 'is_active', 'is_rare']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at', 'awarded_by', 'is_displayed']
    list_filter = ['is_displayed', 'earned_at', 'badge']
    search_fields = ['user__username', 'badge__name']
    readonly_fields = ['earned_at']


@admin.register(UserPoints)
class UserPointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points', 'current_level', 'rank', 'last_updated']
    list_filter = ['current_level', 'last_updated']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_updated']

    fieldsets = (
        ('User', {
            'fields': ('user', 'total_points', 'current_level', 'rank')
        }),
        ('Points Breakdown', {
            'fields': ('performance_points', 'collaboration_points', 'innovation_points', 'learning_points')
        }),
        ('Metadata', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        })
    )


@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'points', 'reason', 'created_by', 'created_at']
    list_filter = ['transaction_type', 'source_type', 'created_at']
    search_fields = ['user__username', 'reason', 'description']
    readonly_fields = ['created_at']
