from django.contrib import admin
from .models import TalentMatrix, CriticalRole, SuccessionCandidate, CompetencyGap


@admin.register(TalentMatrix)
class TalentMatrixAdmin(admin.ModelAdmin):
    list_display = ['user', 'box_category', 'performance_score', 'potential_score', 'assessment_period', 'assessment_date']
    list_filter = ['box_category', 'performance_level', 'potential_level', 'assessment_date']
    search_fields = ['user__first_name', 'user__last_name', 'assessment_period']
    date_hierarchy = 'assessment_date'
    readonly_fields = ['box_category', 'created_at', 'updated_at']


@admin.register(CriticalRole)
class CriticalRoleAdmin(admin.ModelAdmin):
    list_display = ['position', 'current_holder', 'criticality_level', 'succession_readiness', 'is_active']
    list_filter = ['criticality_level', 'succession_readiness', 'is_active']
    search_fields = ['position__title', 'current_holder__first_name', 'current_holder__last_name']
    filter_horizontal = ['required_competencies']


@admin.register(SuccessionCandidate)
class SuccessionCandidateAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'critical_role', 'readiness_level', 'readiness_score', 'nomination_date', 'is_active']
    list_filter = ['readiness_level', 'is_active', 'nomination_date']
    search_fields = ['candidate__first_name', 'candidate__last_name', 'critical_role__position__title']
    readonly_fields = ['nomination_date', 'created_at', 'updated_at']


@admin.register(CompetencyGap)
class CompetencyGapAdmin(admin.ModelAdmin):
    list_display = ['user', 'competency', 'gap_score', 'gap_status', 'priority', 'is_closed']
    list_filter = ['gap_status', 'priority', 'is_closed', 'identified_date']
    search_fields = ['user__first_name', 'user__last_name', 'competency__name']
    readonly_fields = ['gap_score', 'gap_status', 'identified_date', 'created_at', 'updated_at']
    filter_horizontal = ['recommended_trainings']
    date_hierarchy = 'identified_date'
