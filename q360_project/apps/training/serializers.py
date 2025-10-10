"""
Serializers for training app.
"""
from rest_framework import serializers
from django.utils import timezone
from .models import TrainingResource, UserTraining


class TrainingResourceSerializer(serializers.ModelSerializer):
    """Serializer for TrainingResource model."""

    competency_names = serializers.SerializerMethodField()
    assigned_users_count = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()

    class Meta:
        model = TrainingResource
        fields = [
            'id',
            'title',
            'description',
            'type',
            'is_online',
            'delivery_method',
            'link',
            'difficulty_level',
            'duration_hours',
            'language',
            'required_competencies',
            'competency_names',
            'provider',
            'instructor',
            'cost',
            'max_participants',
            'is_active',
            'is_mandatory',
            'assigned_users_count',
            'completion_rate',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_competency_names(self, obj):
        """Əlaqəli kompetensiya adlarını qaytarır."""
        return [comp.name for comp in obj.required_competencies.all()]

    def get_assigned_users_count(self, obj):
        """Təlimə təyin olunmuş istifadəçi sayını qaytarır."""
        return obj.get_assigned_users_count()

    def get_completion_rate(self, obj):
        """Tamamlanma faizini qaytarır."""
        return obj.get_completion_rate()


class TrainingResourceDetailSerializer(TrainingResourceSerializer):
    """Detailed serializer for TrainingResource with related data."""

    from apps.competencies.serializers import CompetencySerializer

    competency_details = CompetencySerializer(
        source='required_competencies',
        many=True,
        read_only=True
    )

    class Meta(TrainingResourceSerializer.Meta):
        fields = TrainingResourceSerializer.Meta.fields + ['competency_details']


class UserTrainingSerializer(serializers.ModelSerializer):
    """Serializer for UserTraining model."""

    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    resource_title = serializers.CharField(source='resource.title', read_only=True)
    assigned_by_name = serializers.CharField(
        source='assigned_by.get_full_name',
        read_only=True,
        allow_null=True
    )
    is_overdue = serializers.SerializerMethodField()
    days_until_due = serializers.SerializerMethodField()

    class Meta:
        model = UserTraining
        fields = [
            'id',
            'user',
            'user_full_name',
            'resource',
            'resource_title',
            'assigned_by',
            'assigned_by_name',
            'assignment_type',
            'related_goal',
            'start_date',
            'due_date',
            'completed_date',
            'status',
            'progress_percentage',
            'completion_note',
            'user_feedback',
            'rating',
            'certificate_url',
            'is_overdue',
            'days_until_due',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['assigned_by', 'created_at', 'updated_at']

    def get_is_overdue(self, obj):
        """Vaxtın keçib-keçmədiyini qaytarır."""
        return obj.is_overdue()

    def get_days_until_due(self, obj):
        """Son tarixə qalan gün sayını qaytarır."""
        return obj.get_days_until_due()

    def validate(self, data):
        """Validate user training data."""
        user = data.get('user')
        resource = data.get('resource')

        # Check for existing training
        if self.instance is None:  # Only for creation
            if UserTraining.objects.filter(user=user, resource=resource).exists():
                raise serializers.ValidationError({
                    'resource': 'Bu istifadəçi üçün bu təlim artıq mövcuddur.'
                })

        # Validate dates
        start_date = data.get('start_date')
        due_date = data.get('due_date')

        if start_date and due_date and start_date > due_date:
            raise serializers.ValidationError({
                'due_date': 'Son tarix başlama tarixindən sonra olmalıdır.'
            })

        # Validate progress percentage
        progress = data.get('progress_percentage', 0)
        if progress < 0 or progress > 100:
            raise serializers.ValidationError({
                'progress_percentage': 'Proqres 0 ilə 100 arasında olmalıdır.'
            })

        return data


class UserTrainingDetailSerializer(UserTrainingSerializer):
    """Detailed serializer for UserTraining with resource details."""

    resource_details = TrainingResourceSerializer(source='resource', read_only=True)

    class Meta(UserTrainingSerializer.Meta):
        fields = UserTrainingSerializer.Meta.fields + ['resource_details']


class UserTrainingStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating training status."""

    status = serializers.ChoiceField(choices=UserTraining.STATUS_CHOICES)
    completion_note = serializers.CharField(required=False, allow_blank=True)
    progress_percentage = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=100
    )

    def validate(self, data):
        """Validate status update."""
        if data.get('status') == 'completed' and data.get('progress_percentage', 100) != 100:
            data['progress_percentage'] = 100

        return data


class UserTrainingProgressUpdateSerializer(serializers.Serializer):
    """Serializer for updating training progress."""

    progress_percentage = serializers.IntegerField(min_value=0, max_value=100)

    def validate_progress_percentage(self, value):
        """Validate progress percentage."""
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                'Proqres 0 ilə 100 arasında olmalıdır.'
            )
        return value


class UserTrainingFeedbackSerializer(serializers.Serializer):
    """Serializer for submitting training feedback."""

    user_feedback = serializers.CharField(allow_blank=True)
    rating = serializers.IntegerField(min_value=1, max_value=5, required=False)

    def validate_rating(self, value):
        """Validate rating."""
        if value and (value < 1 or value > 5):
            raise serializers.ValidationError(
                'Reytinq 1 ilə 5 arasında olmalıdır.'
            )
        return value


class TrainingRecommendationSerializer(serializers.Serializer):
    """Serializer for training recommendations based on competencies."""

    user_id = serializers.IntegerField()
    competency_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    limit = serializers.IntegerField(default=5, min_value=1, max_value=20)

    def validate_user_id(self, value):
        """Validate user exists."""
        from apps.accounts.models import User
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('İstifadəçi tapılmadı.')
        return value


class TrainingStatisticsSerializer(serializers.Serializer):
    """Serializer for training statistics."""

    total_trainings = serializers.IntegerField()
    active_trainings = serializers.IntegerField()
    completed_trainings = serializers.IntegerField()
    in_progress_trainings = serializers.IntegerField()
    overdue_trainings = serializers.IntegerField()
    average_completion_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    most_popular_trainings = TrainingResourceSerializer(many=True)
