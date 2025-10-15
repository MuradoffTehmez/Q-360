"""
Serializers for evaluations app API endpoints.
"""
from rest_framework import serializers
from .models import (
    EvaluationCampaign, QuestionCategory, Question, CampaignQuestion,
    EvaluationAssignment, Response, EvaluationResult
)


class QuestionCategorySerializer(serializers.ModelSerializer):
    """Serializer for QuestionCategory model."""

    question_count = serializers.SerializerMethodField()

    class Meta:
        model = QuestionCategory
        fields = ['id', 'name', 'description', 'order', 'is_active', 'question_count']

    def get_question_count(self, obj):
        return obj.questions.filter(is_active=True).count()


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model."""

    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'category', 'category_name', 'text', 'question_type',
            'max_score', 'is_required', 'order', 'is_active'
        ]


class CampaignQuestionSerializer(serializers.ModelSerializer):
    """Serializer for CampaignQuestion model."""

    question_detail = QuestionSerializer(source='question', read_only=True)

    class Meta:
        model = CampaignQuestion
        fields = ['id', 'campaign', 'question', 'question_detail', 'order']


class EvaluationCampaignSerializer(serializers.ModelSerializer):
    """Serializer for EvaluationCampaign model."""

    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    completion_rate = serializers.ReadOnlyField(source='get_completion_rate')
    is_currently_active = serializers.ReadOnlyField(source='is_active')
    questions = CampaignQuestionSerializer(source='campaign_questions', many=True, read_only=True)

    class Meta:
        model = EvaluationCampaign
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date',
            'status', 'is_anonymous', 'allow_self_evaluation',
            'weight_self', 'weight_supervisor', 'weight_peer', 'weight_subordinate',
            'target_departments', 'target_users', 'created_by',
            'created_by_name', 'completion_rate', 'is_currently_active',
            'questions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Validate campaign data.
        Ensures model's clean() method is called for consistency.
        """
        from decimal import Decimal

        # Validate weights sum to 100%
        weight_self = Decimal(str(data.get('weight_self', 20)))
        weight_supervisor = Decimal(str(data.get('weight_supervisor', 50)))
        weight_peer = Decimal(str(data.get('weight_peer', 20)))
        weight_subordinate = Decimal(str(data.get('weight_subordinate', 10)))

        total_weight = weight_self + weight_supervisor + weight_peer + weight_subordinate

        if total_weight != Decimal('100.00'):
            raise serializers.ValidationError({
                'weight_self': f'Ağırlıq çəkilərinin cəmi 100% olmalıdır. Hazırda: {total_weight}%'
            })

        # Validate dates
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                'end_date': 'Bitmə tarixi başlama tarixindən sonra olmalıdır.'
            })

        return data


class ResponseSerializer(serializers.ModelSerializer):
    """Serializer for Response model."""

    question_text = serializers.CharField(source='question.text', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)

    class Meta:
        model = Response
        fields = [
            'id', 'assignment', 'question', 'question_text', 'question_type',
            'score', 'boolean_answer', 'text_answer', 'comment',
            'created_at', 'updated_at'
        ]

    def validate(self, data):
        """Validate response based on question type."""
        question = data.get('question')
        if question:
            if question.question_type == 'scale' and not data.get('score'):
                raise serializers.ValidationError("Bal skalası üçün bal daxil edilməlidir.")
            if question.question_type == 'boolean' and data.get('boolean_answer') is None:
                raise serializers.ValidationError("Bəli/Xeyr sualı üçün cavab seçilməlidir.")
        return data


class EvaluationAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for EvaluationAssignment model."""

    evaluator_name = serializers.CharField(source='evaluator.get_full_name', read_only=True)
    evaluatee_name = serializers.CharField(source='evaluatee.get_full_name', read_only=True)
    campaign_title = serializers.CharField(source='campaign.title', read_only=True)
    progress = serializers.ReadOnlyField(source='get_progress')
    responses = ResponseSerializer(many=True, read_only=True)

    class Meta:
        model = EvaluationAssignment
        fields = [
            'id', 'campaign', 'campaign_title', 'evaluator', 'evaluator_name',
            'evaluatee', 'evaluatee_name', 'relationship', 'status',
            'progress', 'started_at', 'completed_at', 'responses',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['started_at', 'completed_at', 'created_at', 'updated_at']


class EvaluationResultSerializer(serializers.ModelSerializer):
    """Serializer for EvaluationResult model."""

    evaluatee_name = serializers.CharField(source='evaluatee.get_full_name', read_only=True)
    campaign_title = serializers.CharField(source='campaign.title', read_only=True)

    class Meta:
        model = EvaluationResult
        fields = [
            'id', 'campaign', 'campaign_title', 'evaluatee', 'evaluatee_name',
            'overall_score', 'self_score', 'supervisor_score',
            'peer_score', 'subordinate_score', 'total_evaluators',
            'completion_rate', 'is_finalized', 'finalized_at',
            'calculated_at', 'created_at'
        ]
