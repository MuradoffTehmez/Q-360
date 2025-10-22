"""Admin panel for Wellness module."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    HealthCheckup,
    MentalHealthSurvey,
    FitnessProgram,
    MedicalClaim,
    WellnessChallenge,
    WellnessChallengeParticipation,
    HealthScore,
    StepTracking
)


@admin.register(HealthCheckup)
class HealthCheckupAdmin(SimpleHistoryAdmin):
    list_display = ['employee', 'checkup_type', 'scheduled_date', 'status', 'provider']
    list_filter = ['status', 'checkup_type', 'scheduled_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'provider']
    date_hierarchy = 'scheduled_date'


@admin.register(MentalHealthSurvey)
class MentalHealthSurveyAdmin(SimpleHistoryAdmin):
    list_display = ['employee', 'survey_date', 'stress_level', 'work_life_balance', 'seeking_support']
    list_filter = ['stress_level', 'seeking_support', 'survey_date']
    search_fields = ['employee__first_name', 'employee__last_name']
    date_hierarchy = 'survey_date'


@admin.register(FitnessProgram)
class FitnessProgramAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'program_type', 'start_date', 'end_date', 'status', 'get_participant_count']
    list_filter = ['status', 'program_type', 'start_date']
    search_fields = ['title', 'instructor']
    date_hierarchy = 'start_date'
    filter_horizontal = ['participants']


@admin.register(MedicalClaim)
class MedicalClaimAdmin(SimpleHistoryAdmin):
    list_display = ['employee', 'claim_type', 'claim_date', 'amount_claimed', 'amount_approved', 'status']
    list_filter = ['status', 'claim_type', 'claim_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'provider']
    date_hierarchy = 'claim_date'


@admin.register(WellnessChallenge)
class WellnessChallengeAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'challenge_type', 'start_date', 'end_date', 'status', 'get_participant_count']
    list_filter = ['status', 'challenge_type', 'start_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'start_date'


@admin.register(WellnessChallengeParticipation)
class WellnessChallengeParticipationAdmin(admin.ModelAdmin):
    list_display = ['participant', 'challenge', 'progress', 'completed', 'joined_date']
    list_filter = ['completed', 'joined_date']
    search_fields = ['participant__first_name', 'participant__last_name', 'challenge__title']


@admin.register(HealthScore)
class HealthScoreAdmin(SimpleHistoryAdmin):
    list_display = ['employee', 'score_date', 'overall_score', 'physical_health', 'mental_health', 'bmi']
    list_filter = ['score_date']
    search_fields = ['employee__first_name', 'employee__last_name']
    date_hierarchy = 'score_date'


@admin.register(StepTracking)
class StepTrackingAdmin(admin.ModelAdmin):
    list_display = ['employee', 'tracking_date', 'steps', 'distance_km', 'calories_burned', 'data_source']
    list_filter = ['tracking_date', 'data_source']
    search_fields = ['employee__first_name', 'employee__last_name']
    date_hierarchy = 'tracking_date'
