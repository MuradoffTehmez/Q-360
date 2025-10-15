"""
Serializers for workforce_planning app API endpoints.
"""
from rest_framework import serializers
from .models import TalentMatrix, CriticalRole, SuccessionCandidate, CompetencyGap
from apps.accounts.models import User
from apps.departments.models import Position
from apps.competencies.models import Competency, ProficiencyLevel
from apps.training.models import TrainingResource


class TalentMatrixSerializer(serializers.ModelSerializer):
    """Serializer for TalentMatrix model - 9-Box Talent Assessment."""

    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_position = serializers.CharField(source='user.profile.position.title', read_only=True)
    assessed_by_name = serializers.CharField(source='assessed_by.get_full_name', read_only=True)
    box_category_display = serializers.CharField(source='get_box_category_display', read_only=True)
    performance_level_display = serializers.CharField(source='get_performance_level_display', read_only=True)
    potential_level_display = serializers.CharField(source='get_potential_level_display', read_only=True)

    class Meta:
        model = TalentMatrix
        fields = [
            'id', 'user', 'user_name', 'user_position',
            'performance_level', 'performance_level_display', 'performance_score',
            'potential_level', 'potential_level_display', 'potential_score',
            'box_category', 'box_category_display',
            'assessed_by', 'assessed_by_name', 'assessment_date', 'assessment_period',
            'notes', 'development_actions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['box_category', 'created_at', 'updated_at']


class TalentMatrixCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating TalentMatrix assessments."""

    class Meta:
        model = TalentMatrix
        fields = [
            'user', 'performance_level', 'performance_score',
            'potential_level', 'potential_score',
            'assessed_by', 'assessment_date', 'assessment_period',
            'notes', 'development_actions'
        ]

    def validate(self, data):
        """Validate performance and potential scores match their levels."""
        perf_score = data.get('performance_score')
        pot_score = data.get('potential_score')

        if perf_score is not None:
            if perf_score < 0 or perf_score > 100:
                raise serializers.ValidationError("Performans balı 0-100 arasında olmalıdır.")

        if pot_score is not None:
            if pot_score < 0 or pot_score > 100:
                raise serializers.ValidationError("Potensial balı 0-100 arasında olmalıdır.")

        return data


class CriticalRoleSerializer(serializers.ModelSerializer):
    """Serializer for CriticalRole model - Critical positions requiring succession planning."""

    position_title = serializers.CharField(source='position.title', read_only=True)
    current_holder_name = serializers.CharField(source='current_holder.get_full_name', read_only=True)
    criticality_level_display = serializers.CharField(source='get_criticality_level_display', read_only=True)
    succession_readiness_display = serializers.CharField(source='get_succession_readiness_display', read_only=True)

    required_competencies_list = serializers.SerializerMethodField()
    succession_candidates_count = serializers.SerializerMethodField()

    class Meta:
        model = CriticalRole
        fields = [
            'id', 'position', 'position_title',
            'current_holder', 'current_holder_name',
            'criticality_level', 'criticality_level_display',
            'business_impact',
            'required_competencies', 'required_competencies_list',
            'required_experience_years',
            'succession_readiness', 'succession_readiness_display',
            'succession_candidates_count',
            'is_active', 'designated_date', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['designated_date', 'created_at', 'updated_at']

    def get_required_competencies_list(self, obj):
        """Get list of required competency names."""
        return [comp.name for comp in obj.required_competencies.all()]

    def get_succession_candidates_count(self, obj):
        """Get count of active succession candidates."""
        return obj.succession_candidates.filter(is_active=True).count()


class SuccessionCandidateSerializer(serializers.ModelSerializer):
    """Serializer for SuccessionCandidate model - Candidates for critical role succession."""

    candidate_name = serializers.CharField(source='candidate.get_full_name', read_only=True)
    candidate_position = serializers.CharField(source='candidate.profile.position.title', read_only=True)
    critical_role_title = serializers.CharField(source='critical_role.position.title', read_only=True)
    nominated_by_name = serializers.CharField(source='nominated_by.get_full_name', read_only=True)
    readiness_level_display = serializers.CharField(source='get_readiness_level_display', read_only=True)

    class Meta:
        model = SuccessionCandidate
        fields = [
            'id', 'critical_role', 'critical_role_title',
            'candidate', 'candidate_name', 'candidate_position',
            'readiness_level', 'readiness_level_display', 'readiness_score',
            'strengths', 'development_needs', 'development_plan',
            'nominated_by', 'nominated_by_name', 'nomination_date',
            'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['nomination_date', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate succession candidate data."""
        critical_role = data.get('critical_role')
        candidate = data.get('candidate')

        # Check if candidate is already nominated for this role
        if critical_role and candidate:
            existing = SuccessionCandidate.objects.filter(
                critical_role=critical_role,
                candidate=candidate,
                is_active=True
            ).exclude(pk=self.instance.pk if self.instance else None)

            if existing.exists():
                raise serializers.ValidationError(
                    "Bu namizəd artıq bu kritik rol üçün təyin edilmişdir."
                )

        return data


class CompetencyGapSerializer(serializers.ModelSerializer):
    """Serializer for CompetencyGap model - Gap analysis for competency development."""

    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    competency_name = serializers.CharField(source='competency.name', read_only=True)
    current_level_name = serializers.CharField(source='current_level.name', read_only=True)
    target_level_name = serializers.CharField(source='target_level.name', read_only=True)
    target_position_title = serializers.CharField(source='target_position.title', read_only=True)
    gap_status_display = serializers.CharField(source='get_gap_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    recommended_trainings_list = serializers.SerializerMethodField()

    class Meta:
        model = CompetencyGap
        fields = [
            'id', 'user', 'user_name',
            'competency', 'competency_name',
            'current_level', 'current_level_name', 'current_score',
            'target_level', 'target_level_name', 'target_score',
            'gap_score', 'gap_status', 'gap_status_display',
            'target_position', 'target_position_title',
            'recommended_actions',
            'recommended_trainings', 'recommended_trainings_list',
            'priority', 'priority_display',
            'identified_date', 'target_close_date',
            'is_closed', 'closed_date', 'closure_notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['gap_score', 'gap_status', 'identified_date', 'created_at', 'updated_at']

    def get_recommended_trainings_list(self, obj):
        """Get list of recommended training resources."""
        return [
            {
                'id': training.id,
                'title': training.title,
                'training_type': training.get_training_type_display()
            }
            for training in obj.recommended_trainings.all()
        ]


class CompetencyGapCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating CompetencyGap records."""

    class Meta:
        model = CompetencyGap
        fields = [
            'user', 'competency',
            'current_level', 'current_score',
            'target_level', 'target_score',
            'target_position',
            'recommended_actions', 'recommended_trainings',
            'priority', 'target_close_date'
        ]

    def validate(self, data):
        """Validate competency gap data."""
        current_score = data.get('current_score', 0)
        target_score = data.get('target_score')

        if current_score < 0 or current_score > 100:
            raise serializers.ValidationError("Cari bal 0-100 arasında olmalıdır.")

        if target_score < 0 or target_score > 100:
            raise serializers.ValidationError("Hədəf bal 0-100 arasında olmalıdır.")

        if target_score <= current_score:
            raise serializers.ValidationError(
                "Hədəf bal cari baldan yüksək olmalıdır."
            )

        return data


# Summary/Dashboard Serializers

class TalentMatrixSummarySerializer(serializers.Serializer):
    """Serializer for talent matrix summary statistics."""

    total_assessments = serializers.IntegerField()
    box_distribution = serializers.DictField()
    high_potential_count = serializers.IntegerField()
    high_performance_count = serializers.IntegerField()
    top_talent_count = serializers.IntegerField()
    assessment_period = serializers.CharField()


class SuccessionPlanSummarySerializer(serializers.Serializer):
    """Serializer for succession planning summary."""

    total_critical_roles = serializers.IntegerField()
    roles_with_successors = serializers.IntegerField()
    roles_without_successors = serializers.IntegerField()
    ready_now_count = serializers.IntegerField()
    needs_development_count = serializers.IntegerField()
    succession_coverage_rate = serializers.DecimalField(max_digits=5, decimal_places=2)


class CompetencyGapSummarySerializer(serializers.Serializer):
    """Serializer for competency gap analysis summary."""

    total_gaps = serializers.IntegerField()
    open_gaps = serializers.IntegerField()
    closed_gaps = serializers.IntegerField()
    major_gaps_count = serializers.IntegerField()
    high_priority_count = serializers.IntegerField()
    average_gap_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    top_gap_areas = serializers.ListField()
