"""
Serializers for Wellness & Well-Being module API.
"""
from rest_framework import serializers
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


class HealthCheckupSerializer(serializers.ModelSerializer):
    """Serializer for HealthCheckup model."""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    checkup_type_display = serializers.CharField(source='get_checkup_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = HealthCheckup
        fields = '__all__'
        read_only_fields = ['employee', 'created_at', 'updated_at', 'reminder_sent']


class MentalHealthSurveySerializer(serializers.ModelSerializer):
    """Serializer for MentalHealthSurvey model."""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    overall_score = serializers.SerializerMethodField()

    class Meta:
        model = MentalHealthSurvey
        fields = '__all__'
        read_only_fields = ['employee', 'survey_date']

    def get_overall_score(self, obj):
        """Get calculated overall mental health score."""
        return obj.get_overall_score()


class FitnessProgramSerializer(serializers.ModelSerializer):
    """Serializer for FitnessProgram model."""
    participant_count = serializers.SerializerMethodField()
    available_spots = serializers.SerializerMethodField()
    is_full = serializers.SerializerMethodField()
    program_type_display = serializers.CharField(source='get_program_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = FitnessProgram
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_participant_count(self, obj):
        return obj.get_participant_count()

    def get_available_spots(self, obj):
        return obj.get_available_spots()

    def get_is_full(self, obj):
        return obj.is_full()


class MedicalClaimSerializer(serializers.ModelSerializer):
    """Serializer for MedicalClaim model."""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    claim_type_display = serializers.CharField(source='get_claim_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = MedicalClaim
        fields = '__all__'
        read_only_fields = ['employee', 'created_at', 'updated_at', 'reviewed_by', 'reviewed_date']


class WellnessChallengeParticipationSerializer(serializers.ModelSerializer):
    """Serializer for WellnessChallengeParticipation model."""
    participant_name = serializers.CharField(source='participant.get_full_name', read_only=True)
    challenge_title = serializers.CharField(source='challenge.title', read_only=True)

    class Meta:
        model = WellnessChallengeParticipation
        fields = '__all__'
        read_only_fields = ['joined_date']


class WellnessChallengeSerializer(serializers.ModelSerializer):
    """Serializer for WellnessChallenge model."""
    participant_count = serializers.SerializerMethodField()
    challenge_type_display = serializers.CharField(source='get_challenge_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True, allow_null=True)
    participations = WellnessChallengeParticipationSerializer(many=True, read_only=True)

    class Meta:
        model = WellnessChallenge
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_participant_count(self, obj):
        return obj.get_participant_count()


class HealthScoreSerializer(serializers.ModelSerializer):
    """Serializer for HealthScore model."""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    bmi_category = serializers.SerializerMethodField()
    calculated_overall = serializers.SerializerMethodField()

    class Meta:
        model = HealthScore
        fields = '__all__'
        read_only_fields = ['employee', 'score_date']

    def get_bmi_category(self, obj):
        return obj.get_bmi_category()

    def get_calculated_overall(self, obj):
        return obj.calculate_overall_score()


class StepTrackingSerializer(serializers.ModelSerializer):
    """Serializer for StepTracking model."""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)

    class Meta:
        model = StepTracking
        fields = '__all__'
        read_only_fields = ['employee', 'synced_at']


# Compact serializers for listing views
class HealthCheckupListSerializer(serializers.ModelSerializer):
    """Compact serializer for HealthCheckup list view."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = HealthCheckup
        fields = ['id', 'checkup_type', 'scheduled_date', 'status', 'status_display', 'provider']


class FitnessProgramListSerializer(serializers.ModelSerializer):
    """Compact serializer for FitnessProgram list view."""
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = FitnessProgram
        fields = ['id', 'title', 'program_type', 'start_date', 'end_date', 'status', 'participant_count', 'capacity']

    def get_participant_count(self, obj):
        return obj.get_participant_count()


class MedicalClaimListSerializer(serializers.ModelSerializer):
    """Compact serializer for MedicalClaim list view."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = MedicalClaim
        fields = ['id', 'claim_type', 'claim_date', 'amount_claimed', 'status', 'status_display']
