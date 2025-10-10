"""
Serializers for competencies app.
"""
from rest_framework import serializers
from .models import Competency, ProficiencyLevel, PositionCompetency, UserSkill


class CompetencySerializer(serializers.ModelSerializer):
    """Serializer for Competency model."""

    active_positions_count = serializers.SerializerMethodField()
    total_users_with_skill = serializers.SerializerMethodField()

    class Meta:
        model = Competency
        fields = [
            'id',
            'name',
            'description',
            'is_active',
            'active_positions_count',
            'total_users_with_skill',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_active_positions_count(self, obj):
        """Aktiv vəzifə sayını qaytarır."""
        return obj.get_active_positions().count()

    def get_total_users_with_skill(self, obj):
        """Bu kompetensiyaya malik istifadəçi sayını qaytarır."""
        return obj.get_total_users_with_skill()


class ProficiencyLevelSerializer(serializers.ModelSerializer):
    """Serializer for ProficiencyLevel model."""

    class Meta:
        model = ProficiencyLevel
        fields = [
            'id',
            'name',
            'display_name',
            'score_min',
            'score_max',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """Validate that score_min is less than score_max."""
        if data.get('score_min') and data.get('score_max'):
            if data['score_min'] >= data['score_max']:
                raise serializers.ValidationError({
                    'score_max': 'Maksimum bal minimum baldan böyük olmalıdır.'
                })
        return data


class PositionCompetencySerializer(serializers.ModelSerializer):
    """Serializer for PositionCompetency model."""

    competency_name = serializers.CharField(source='competency.name', read_only=True)
    position_title = serializers.CharField(source='position.title', read_only=True)
    required_level_name = serializers.CharField(
        source='required_level.display_name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = PositionCompetency
        fields = [
            'id',
            'position',
            'position_title',
            'competency',
            'competency_name',
            'weight',
            'required_level',
            'required_level_name',
            'is_mandatory',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_weight(self, value):
        """Validate weight is between 1 and 100."""
        if value < 1 or value > 100:
            raise serializers.ValidationError(
                'Çəki 1 ilə 100 arasında olmalıdır.'
            )
        return value


class UserSkillSerializer(serializers.ModelSerializer):
    """Serializer for UserSkill model."""

    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    competency_name = serializers.CharField(source='competency.name', read_only=True)
    level_name = serializers.CharField(source='level.display_name', read_only=True)
    approved_by_name = serializers.CharField(
        source='approved_by.get_full_name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = UserSkill
        fields = [
            'id',
            'user',
            'user_full_name',
            'competency',
            'competency_name',
            'level',
            'level_name',
            'current_score',
            'is_approved',
            'approval_status',
            'approved_by',
            'approved_by_name',
            'approved_at',
            'self_assessment_score',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'approved_by',
            'approved_at',
            'approval_status',
            'created_at',
            'updated_at',
        ]

    def validate(self, data):
        """Validate user skill data."""
        user = data.get('user')
        competency = data.get('competency')

        # Check for existing skill
        if self.instance is None:  # Only for creation
            if UserSkill.objects.filter(user=user, competency=competency).exists():
                raise serializers.ValidationError({
                    'competency': 'Bu istifadəçi üçün bu kompetensiya artıq mövcuddur.'
                })

        return data


class UserSkillApprovalSerializer(serializers.Serializer):
    """Serializer for approving/rejecting user skills."""

    action = serializers.ChoiceField(choices=['approve', 'reject'])
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        """Validate approval action."""
        if data['action'] not in ['approve', 'reject']:
            raise serializers.ValidationError({
                'action': 'Yalnız approve və ya reject əməliyyatları mümkündür.'
            })
        return data


class CompetencyDetailSerializer(CompetencySerializer):
    """Detailed serializer for Competency with related data."""

    positions = PositionCompetencySerializer(
        source='position_competencies',
        many=True,
        read_only=True
    )
    users_with_skill = UserSkillSerializer(
        source='user_skills',
        many=True,
        read_only=True
    )

    class Meta(CompetencySerializer.Meta):
        fields = CompetencySerializer.Meta.fields + ['positions', 'users_with_skill']


class UserSkillDetailSerializer(UserSkillSerializer):
    """Detailed serializer for UserSkill with competency details."""

    competency_details = CompetencySerializer(source='competency', read_only=True)
    level_details = ProficiencyLevelSerializer(source='level', read_only=True)

    class Meta(UserSkillSerializer.Meta):
        fields = UserSkillSerializer.Meta.fields + [
            'competency_details',
            'level_details',
        ]
