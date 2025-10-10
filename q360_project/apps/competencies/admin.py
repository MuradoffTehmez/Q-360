"""
Admin configuration for competencies app.
"""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Competency, ProficiencyLevel, PositionCompetency, UserSkill


@admin.register(Competency)
class CompetencyAdmin(SimpleHistoryAdmin):
    """Admin for Competency model."""

    list_display = ['name', 'is_active', 'get_position_count', 'get_user_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']

    fieldsets = (
        ('Əsas Məlumat', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_position_count(self, obj):
        """Vəzifə sayını qaytarır."""
        return obj.position_competencies.count()
    get_position_count.short_description = 'Vəzifə Sayı'

    def get_user_count(self, obj):
        """İstifadəçi sayını qaytarır."""
        return obj.user_skills.filter(is_approved=True).count()
    get_user_count.short_description = 'İstifadəçi Sayı'


@admin.register(ProficiencyLevel)
class ProficiencyLevelAdmin(admin.ModelAdmin):
    """Admin for ProficiencyLevel model."""

    list_display = ['display_name', 'name', 'score_min', 'score_max', 'created_at']
    list_filter = ['name', 'created_at']
    search_fields = ['display_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['score_min']


@admin.register(PositionCompetency)
class PositionCompetencyAdmin(SimpleHistoryAdmin):
    """Admin for PositionCompetency model."""

    list_display = ['position', 'competency', 'weight', 'required_level', 'is_mandatory', 'created_at']
    list_filter = ['is_mandatory', 'created_at', 'position__organization']
    search_fields = ['position__title', 'competency__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-weight']

    fieldsets = (
        ('Əsas Məlumat', {
            'fields': ('position', 'competency', 'weight', 'required_level', 'is_mandatory')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserSkill)
class UserSkillAdmin(SimpleHistoryAdmin):
    """Admin for UserSkill model."""

    list_display = [
        'user',
        'competency',
        'level',
        'current_score',
        'approval_status',
        'is_approved',
        'created_at'
    ]
    list_filter = ['approval_status', 'is_approved', 'level', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'competency__name']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Əsas Məlumat', {
            'fields': ('user', 'competency', 'level', 'current_score', 'self_assessment_score')
        }),
        ('Təsdiq', {
            'fields': ('is_approved', 'approval_status', 'approved_by', 'approved_at')
        }),
        ('Qeydlər', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['approve_skills', 'reject_skills']

    def approve_skills(self, request, queryset):
        """Toplu təsdiq əməliyyatı."""
        count = 0
        for skill in queryset:
            skill.approve(request.user)
            count += 1
        self.message_user(request, f'{count} bacarıq təsdiqləndi.')
    approve_skills.short_description = 'Seçilmiş bacarıqları təsdiq et'

    def reject_skills(self, request, queryset):
        """Toplu rədd əməliyyatı."""
        count = 0
        for skill in queryset:
            skill.reject(request.user)
            count += 1
        self.message_user(request, f'{count} bacarıq rədd edildi.')
    reject_skills.short_description = 'Seçilmiş bacarıqları rədd et'
