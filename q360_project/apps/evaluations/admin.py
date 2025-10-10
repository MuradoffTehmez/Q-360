"""
Professional admin configuration for evaluations app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Avg
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    EvaluationCampaign, QuestionCategory, Question, CampaignQuestion,
    EvaluationAssignment, Response, EvaluationResult
)


class CampaignQuestionInline(admin.TabularInline):
    """Inline admin for campaign questions."""
    model = CampaignQuestion
    extra = 1
    fields = ['question', 'order']
    autocomplete_fields = ['question']
    ordering = ['order']


@admin.register(EvaluationCampaign)
class EvaluationCampaignAdmin(SimpleHistoryAdmin):
    """Professional admin for evaluation campaigns."""

    list_display = [
        'title', 'colored_status', 'date_range',
        'assignments_count', 'completion_rate', 'created_by', 'actions_column'
    ]
    list_filter = ['status', 'start_date', 'end_date', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['target_departments', 'target_users']
    readonly_fields = ['created_at', 'updated_at', 'campaign_statistics']
    inlines = [CampaignQuestionInline]

    fieldsets = (
        (_('Əsas Məlumatlar'), {
            'fields': ('title', 'description', 'status')
        }),
        (_('Tarixlər'), {
            'fields': ('start_date', 'end_date')
        }),
        (_('Hədəflər'), {
            'fields': ('target_departments', 'target_users'),
            'classes': ('collapse',)
        }),
        (_('Yaradıcı və Statistika'), {
            'fields': ('created_by', 'campaign_statistics', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Save model with current user."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def colored_status(self, obj):
        """Display colored status badge."""
        colors = {
            'draft': '#6c757d',
            'active': '#28a745',
            'completed': '#007bff',
            'cancelled': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'

    def date_range(self, obj):
        """Display date range."""
        return f"{obj.start_date} → {obj.end_date}"
    date_range.short_description = 'Kampaniya Müddəti'

    def assignments_count(self, obj):
        """Count assignments."""
        return obj.assignments.count()
    assignments_count.short_description = 'Tapşırıqlar'

    def completion_rate(self, obj):
        """Calculate completion rate."""
        total = obj.assignments.count()
        if total == 0:
            return "0%"
        completed = obj.assignments.filter(status='completed').count()
        rate = (completed / total) * 100
        color = '#28a745' if rate >= 80 else '#ffc107' if rate >= 50 else '#dc3545'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, rate
        )
    completion_rate.short_description = 'Tamamlanma'

    def actions_column(self, obj):
        """Action buttons."""
        return format_html(
            '<a class="button" href="{}">Bax</a> '
            '<a class="button" href="{}">Dəyiş</a>',
            reverse('admin:evaluations_evaluationcampaign_change', args=[obj.pk]),
            reverse('admin:evaluations_evaluationcampaign_change', args=[obj.pk])
        )
    actions_column.short_description = 'Əməliyyatlar'

    def campaign_statistics(self, obj):
        """Display campaign statistics."""
        total_assignments = obj.assignments.count()
        completed = obj.assignments.filter(status='completed').count()
        pending = obj.assignments.filter(status='pending').count()
        in_progress = obj.assignments.filter(status='in_progress').count()

        stats_html = f"""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
            <h3 style="margin-top: 0;">Kampaniya Statistikası</h3>
            <table style="width: 100%;">
                <tr>
                    <td><strong>Ümumi Tapşırıqlar:</strong></td>
                    <td>{total_assignments}</td>
                </tr>
                <tr>
                    <td><strong>Tamamlanmış:</strong></td>
                    <td style="color: #28a745;">{completed}</td>
                </tr>
                <tr>
                    <td><strong>Davam edən:</strong></td>
                    <td style="color: #ffc107;">{in_progress}</td>
                </tr>
                <tr>
                    <td><strong>Gözləyən:</strong></td>
                    <td style="color: #6c757d;">{pending}</td>
                </tr>
            </table>
        </div>
        """
        return format_html(stats_html)
    campaign_statistics.short_description = 'Statistika'


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    """Admin for question categories."""

    list_display = ['name', 'order', 'questions_count', 'colored_status']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    ordering = ['order']

    fieldsets = (
        (_('Əsas Məlumatlar'), {
            'fields': ('name', 'description', 'order')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )

    def questions_count(self, obj):
        """Count questions in category."""
        count = obj.questions.count()
        return format_html(
            '<span style="background: #007bff; color: white; padding: 2px 8px; border-radius: 10px;">{}</span>',
            count
        )
    questions_count.short_description = 'Suallar'

    def colored_status(self, obj):
        """Display colored status."""
        if obj.is_active:
            return format_html(
                '<span style="color: #28a745;">● Aktiv</span>'
            )
        return format_html(
            '<span style="color: #dc3545;">● Deaktiv</span>'
        )
    colored_status.short_description = 'Status'


@admin.register(Question)
class QuestionAdmin(SimpleHistoryAdmin):
    """Professional admin for questions."""

    list_display = [
        'text_preview', 'category', 'colored_type',
        'max_score', 'colored_status'
    ]
    list_filter = ['category', 'question_type', 'is_active']
    search_fields = ['text']
    autocomplete_fields = ['category']

    fieldsets = (
        (_('Sual Məlumatları'), {
            'fields': ('text', 'category', 'question_type')
        }),
        (_('Qiymətləndirmə'), {
            'fields': ('min_score', 'max_score')
        }),
        (_('Parametrlər'), {
            'fields': ('allow_comments', 'is_required', 'is_active'),
            'classes': ('collapse',)
        }),
    )

    def text_preview(self, obj):
        """Display text preview."""
        preview = obj.text[:80] + '...' if len(obj.text) > 80 else obj.text
        return preview
    text_preview.short_description = 'Sual Mətni'

    def colored_type(self, obj):
        """Display colored question type."""
        colors = {
            'scale': '#007bff',
            'text': '#28a745',
            'multiple_choice': '#ffc107'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.question_type, '#6c757d'),
            obj.get_question_type_display()
        )
    colored_type.short_description = 'Növ'

    def colored_status(self, obj):
        """Display colored status."""
        if obj.is_active:
            return format_html('<span style="color: #28a745;">✓ Aktiv</span>')
        return format_html('<span style="color: #dc3545;">✗ Deaktiv</span>')
    colored_status.short_description = 'Status'


@admin.register(CampaignQuestion)
class CampaignQuestionAdmin(admin.ModelAdmin):
    """Admin for campaign questions."""

    list_display = ['campaign', 'question_preview', 'order', 'question_type']
    list_filter = ['campaign', 'question__category']
    autocomplete_fields = ['campaign', 'question']
    ordering = ['campaign', 'order']

    def question_preview(self, obj):
        """Display question preview."""
        preview = obj.question.text[:60] + '...' if len(obj.question.text) > 60 else obj.question.text
        return preview
    question_preview.short_description = 'Sual'

    def question_type(self, obj):
        """Display question type."""
        return obj.question.get_question_type_display()
    question_type.short_description = 'Növ'


@admin.register(EvaluationAssignment)
class EvaluationAssignmentAdmin(SimpleHistoryAdmin):
    """Professional admin for evaluation assignments."""

    list_display = [
        'campaign', 'evaluator_link', 'evaluatee_link',
        'colored_relationship', 'colored_status', 'progress_bar'
    ]
    list_filter = ['campaign', 'relationship', 'status', 'created_at']
    search_fields = [
        'evaluator__username', 'evaluator__first_name', 'evaluator__last_name',
        'evaluatee__username', 'evaluatee__first_name', 'evaluatee__last_name'
    ]
    readonly_fields = ['created_at', 'updated_at', 'started_at', 'completed_at', 'progress_display']
    autocomplete_fields = ['campaign', 'evaluator', 'evaluatee']

    fieldsets = (
        (_('Kampaniya'), {
            'fields': ('campaign',)
        }),
        (_('İştirakçılar'), {
            'fields': ('evaluator', 'evaluatee', 'relationship')
        }),
        (_('Status'), {
            'fields': ('status', 'progress_display')
        }),
        (_('Tarixlər'), {
            'fields': ('created_at', 'updated_at', 'started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

    def evaluator_link(self, obj):
        """Display evaluator with link."""
        url = reverse('admin:accounts_user_change', args=[obj.evaluator.pk])
        return format_html('<a href="{}">{}</a>', url, obj.evaluator.get_full_name())
    evaluator_link.short_description = 'Qiymətləndirən'

    def evaluatee_link(self, obj):
        """Display evaluatee with link."""
        url = reverse('admin:accounts_user_change', args=[obj.evaluatee.pk])
        return format_html('<a href="{}">{}</a>', url, obj.evaluatee.get_full_name())
    evaluatee_link.short_description = 'Qiymətləndirilən'

    def colored_relationship(self, obj):
        """Display colored relationship."""
        colors = {
            'self': '#6c757d',
            'supervisor': '#dc3545',
            'peer': '#007bff',
            'subordinate': '#28a745'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.relationship, '#6c757d'),
            obj.get_relationship_display()
        )
    colored_relationship.short_description = 'Münasibət'

    def colored_status(self, obj):
        """Display colored status."""
        colors = {
            'pending': '#ffc107',
            'in_progress': '#17a2b8',
            'completed': '#28a745'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'

    def progress_bar(self, obj):
        """Display progress bar."""
        progress = obj.get_progress()
        color = '#28a745' if progress >= 100 else '#007bff' if progress >= 50 else '#ffc107'
        return format_html(
            '<div style="width: 100px; background: #e9ecef; border-radius: 3px; overflow: hidden;">'
            '<div style="width: {}%; background: {}; color: white; text-align: center; padding: 2px; font-size: 10px;">{:.0f}%</div>'
            '</div>',
            progress, color, progress
        )
    progress_bar.short_description = 'Tamamlanma'

    def progress_display(self, obj):
        """Display detailed progress."""
        progress = obj.get_progress()
        total_questions = obj.campaign.questions.count()
        answered = Response.objects.filter(assignment=obj).count()

        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">'
            '<strong>Cavablanmış:</strong> {} / {}<br>'
            '<strong>Faiz:</strong> {:.1f}%'
            '</div>',
            answered, total_questions, progress
        )
    progress_display.short_description = 'İrəliləyiş'


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    """Admin for responses."""

    list_display = [
        'assignment', 'question_preview', 'score_display',
        'sentiment_badge', 'created_at'
    ]
    list_filter = [
        'assignment__campaign', 'question__category',
        'sentiment_category', 'created_at'
    ]
    search_fields = ['text_answer', 'comment']
    readonly_fields = ['created_at', 'updated_at', 'sentiment_score', 'sentiment_category']
    autocomplete_fields = ['assignment', 'question']

    fieldsets = (
        (_('Tapşırıq və Sual'), {
            'fields': ('assignment', 'question')
        }),
        (_('Cavab'), {
            'fields': ('score', 'text_answer', 'comment')
        }),
        (_('Sentiment Analizi'), {
            'fields': ('sentiment_score', 'sentiment_category'),
            'classes': ('collapse',)
        }),
        (_('Tarixlər'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def question_preview(self, obj):
        """Display question preview."""
        preview = obj.question.text[:50] + '...' if len(obj.question.text) > 50 else obj.question.text
        return preview
    question_preview.short_description = 'Sual'

    def score_display(self, obj):
        """Display score with color."""
        if obj.score is None:
            return '-'
        max_score = obj.question.max_score
        percentage = (obj.score / max_score) * 100 if max_score > 0 else 0
        color = '#28a745' if percentage >= 80 else '#ffc107' if percentage >= 50 else '#dc3545'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/{}</span>',
            color, obj.score, max_score
        )
    score_display.short_description = 'Bal'

    def sentiment_badge(self, obj):
        """Display sentiment badge."""
        if not obj.sentiment_category:
            return '-'
        colors = {
            'positive': '#28a745',
            'neutral': '#6c757d',
            'negative': '#dc3545'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.sentiment_category, '#6c757d'),
            obj.sentiment_category.title()
        )
    sentiment_badge.short_description = 'Sentiment'


@admin.register(EvaluationResult)
class EvaluationResultAdmin(admin.ModelAdmin):
    """Professional admin for evaluation results."""

    list_display = [
        'campaign', 'evaluatee_link', 'overall_score_display',
        'breakdown_scores', 'colored_finalized', 'calculated_at'
    ]
    list_filter = ['campaign', 'is_finalized', 'calculated_at']
    search_fields = ['evaluatee__username', 'evaluatee__first_name', 'evaluatee__last_name']
    readonly_fields = [
        'calculated_at', 'overall_score', 'self_score',
        'supervisor_score', 'peer_score', 'subordinate_score',
        'score_breakdown_display'
    ]
    autocomplete_fields = ['campaign', 'evaluatee']

    fieldsets = (
        (_('Kampaniya və İstifadəçi'), {
            'fields': ('campaign', 'evaluatee')
        }),
        (_('Ümumi Nəticə'), {
            'fields': ('overall_score', 'is_finalized')
        }),
        (_('Bal Parçalanması'), {
            'fields': (
                'self_score', 'supervisor_score',
                'peer_score', 'subordinate_score',
                'score_breakdown_display'
            ),
            'classes': ('collapse',)
        }),
        (_('Tarixlər'), {
            'fields': ('calculated_at',),
            'classes': ('collapse',)
        }),
    )

    def evaluatee_link(self, obj):
        """Display evaluatee with link."""
        url = reverse('admin:accounts_user_change', args=[obj.evaluatee.pk])
        return format_html('<a href="{}">{}</a>', url, obj.evaluatee.get_full_name())
    evaluatee_link.short_description = 'İstifadəçi'

    def overall_score_display(self, obj):
        """Display overall score with color."""
        if not obj.overall_score:
            return '-'
        score = float(obj.overall_score)
        color = '#28a745' if score >= 4 else '#ffc107' if score >= 3 else '#dc3545'
        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 16px;">{:.2f}/5</span>',
            color, score
        )
    overall_score_display.short_description = 'Ümumi Bal'

    def breakdown_scores(self, obj):
        """Display score breakdown."""
        scores_html = '<div style="font-size: 11px;">'
        if obj.self_score:
            scores_html += f'<div>Özü: {obj.self_score:.1f}</div>'
        if obj.supervisor_score:
            scores_html += f'<div>Rəhbər: {obj.supervisor_score:.1f}</div>'
        if obj.peer_score:
            scores_html += f'<div>Həmkar: {obj.peer_score:.1f}</div>'
        if obj.subordinate_score:
            scores_html += f'<div>Tabe: {obj.subordinate_score:.1f}</div>'
        scores_html += '</div>'
        return format_html(scores_html)
    breakdown_scores.short_description = 'Parçalanmış Ballar'

    def colored_finalized(self, obj):
        """Display finalized status."""
        if obj.is_finalized:
            return format_html('<span style="color: #28a745;">✓ Finallaşdırıldı</span>')
        return format_html('<span style="color: #ffc107;">⏳ İcmalda</span>')
    colored_finalized.short_description = 'Status'

    def score_breakdown_display(self, obj):
        """Display detailed score breakdown."""
        html = '<div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">'
        html += '<h3 style="margin-top: 0;">Bal Detallı Parçalanması</h3>'
        html += '<table style="width: 100%;">'

        if obj.self_score:
            html += f'<tr><td><strong>Özünüqiymətləndirmə:</strong></td><td style="color: #007bff; font-weight: bold;">{obj.self_score:.2f}</td></tr>'
        if obj.supervisor_score:
            html += f'<tr><td><strong>Rəhbər Qiymətləndirməsi:</strong></td><td style="color: #dc3545; font-weight: bold;">{obj.supervisor_score:.2f}</td></tr>'
        if obj.peer_score:
            html += f'<tr><td><strong>Həmkarlar Qiymətləndirməsi:</strong></td><td style="color: #28a745; font-weight: bold;">{obj.peer_score:.2f}</td></tr>'
        if obj.subordinate_score:
            html += f'<tr><td><strong>Tabelelər Qiymətləndirməsi:</strong></td><td style="color: #ffc107; font-weight: bold;">{obj.subordinate_score:.2f}</td></tr>'

        html += '</table></div>'
        return format_html(html)
    score_breakdown_display.short_description = 'Detallı Ballar'
