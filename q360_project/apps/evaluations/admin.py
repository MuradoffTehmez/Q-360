"""
Admin configuration for evaluations app.
"""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    EvaluationCampaign, QuestionCategory, Question, CampaignQuestion,
    EvaluationAssignment, Response, EvaluationResult
)


@admin.register(EvaluationCampaign)
class EvaluationCampaignAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'start_date', 'end_date', 'status', 'created_by']
    list_filter = ['status', 'start_date']
    search_fields = ['title', 'description']
    filter_horizontal = ['target_departments', 'target_users']


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Question)
class QuestionAdmin(SimpleHistoryAdmin):
    list_display = ['text', 'category', 'question_type', 'max_score', 'is_active']
    list_filter = ['category', 'question_type', 'is_active']
    search_fields = ['text']


@admin.register(CampaignQuestion)
class CampaignQuestionAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'question', 'order']
    list_filter = ['campaign']


@admin.register(EvaluationAssignment)
class EvaluationAssignmentAdmin(SimpleHistoryAdmin):
    list_display = ['campaign', 'evaluator', 'evaluatee', 'relationship', 'status']
    list_filter = ['campaign', 'relationship', 'status']
    search_fields = ['evaluator__username', 'evaluatee__username']


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'question', 'score']
    list_filter = ['assignment__campaign']


@admin.register(EvaluationResult)
class EvaluationResultAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'evaluatee', 'overall_score', 'is_finalized']
    list_filter = ['campaign', 'is_finalized']
    search_fields = ['evaluatee__username']
