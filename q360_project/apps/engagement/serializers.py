from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    PulseSurvey, SurveyQuestion, SurveyResponse,
    EngagementScore, Recognition, AnonymousFeedback,
    SentimentAnalysis, GamificationBadge, UserBadge,
    UserPoints, PointsTransaction
)

User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):
    """Simple user serializer for nested representations"""

    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = fields


class SurveyQuestionSerializer(serializers.ModelSerializer):
    """Serializer for survey questions"""

    class Meta:
        model = SurveyQuestion
        fields = [
            'id', 'survey', 'question_text', 'question_type',
            'order', 'is_required', 'options'
        ]


class PulseSurveySerializer(serializers.ModelSerializer):
    """Serializer for Pulse Surveys"""

    questions = SurveyQuestionSerializer(many=True, read_only=True)
    created_by = UserSimpleSerializer(read_only=True)
    response_count = serializers.IntegerField(read_only=True)
    completion_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = PulseSurvey
        fields = [
            'id', 'title', 'description', 'survey_type', 'status',
            'created_by', 'created_at', 'updated_at',
            'start_date', 'end_date', 'is_anonymous', 'is_mandatory',
            'target_departments', 'target_users',
            'questions', 'response_count', 'completion_rate'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class SurveyResponseSerializer(serializers.ModelSerializer):
    """Serializer for survey responses"""

    user = UserSimpleSerializer(read_only=True)
    question = SurveyQuestionSerializer(read_only=True)

    class Meta:
        model = SurveyResponse
        fields = [
            'id', 'survey', 'question', 'user',
            'rating_value', 'text_value', 'boolean_value',
            'submitted_at'
        ]
        read_only_fields = ['submitted_at']


class EngagementScoreSerializer(serializers.ModelSerializer):
    """Serializer for engagement scores"""

    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = EngagementScore
        fields = [
            'id', 'user', 'score_type', 'score_value',
            'department', 'calculated_at', 'period_start', 'period_end',
            'is_promoter', 'is_passive', 'is_detractor', 'notes'
        ]
        read_only_fields = ['calculated_at']


class GamificationBadgeSerializer(serializers.ModelSerializer):
    """Serializer for gamification badges"""

    class Meta:
        model = GamificationBadge
        fields = [
            'id', 'name', 'description', 'category',
            'icon', 'color', 'points_value', 'criteria',
            'is_active', 'is_rare', 'created_at'
        ]
        read_only_fields = ['created_at']


class RecognitionSerializer(serializers.ModelSerializer):
    """Serializer for recognitions"""

    given_by = UserSimpleSerializer(read_only=True)
    given_to = UserSimpleSerializer(read_only=True)
    badge = GamificationBadgeSerializer(read_only=True)
    liked_by_users = UserSimpleSerializer(source='liked_by', many=True, read_only=True)

    class Meta:
        model = Recognition
        fields = [
            'id', 'given_by', 'given_to', 'recognition_type',
            'title', 'message', 'is_public', 'badge', 'points',
            'created_at', 'likes_count', 'liked_by_users'
        ]
        read_only_fields = ['given_by', 'created_at', 'likes_count']


class RecognitionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating recognitions"""

    class Meta:
        model = Recognition
        fields = [
            'given_to', 'recognition_type', 'title', 'message',
            'is_public', 'badge', 'points'
        ]

    def create(self, validated_data):
        validated_data['given_by'] = self.context['request'].user
        return super().create(validated_data)


class AnonymousFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for anonymous feedback"""

    responded_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = AnonymousFeedback
        fields = [
            'id', 'anonymous_id', 'category', 'subject', 'message',
            'status', 'priority', 'department', 'submitted_at', 'updated_at',
            'response', 'responded_by', 'responded_at',
            'sentiment_score', 'sentiment_label'
        ]
        read_only_fields = [
            'anonymous_id', 'submitted_at', 'updated_at',
            'responded_by', 'responded_at', 'sentiment_score', 'sentiment_label'
        ]


class SentimentAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for sentiment analysis"""

    class Meta:
        model = SentimentAnalysis
        fields = [
            'id', 'source_type', 'source_id', 'text_content',
            'sentiment', 'sentiment_score', 'confidence',
            'emotions', 'keywords', 'topics', 'analyzed_at'
        ]
        read_only_fields = ['analyzed_at']


class UserBadgeSerializer(serializers.ModelSerializer):
    """Serializer for user badges"""

    user = UserSimpleSerializer(read_only=True)
    badge = GamificationBadgeSerializer(read_only=True)
    awarded_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = [
            'id', 'user', 'badge', 'earned_at', 'awarded_by',
            'reason', 'is_displayed'
        ]
        read_only_fields = ['earned_at']


class UserPointsSerializer(serializers.ModelSerializer):
    """Serializer for user points"""

    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = UserPoints
        fields = [
            'id', 'user', 'total_points', 'current_level',
            'performance_points', 'collaboration_points',
            'innovation_points', 'learning_points',
            'rank', 'last_updated'
        ]
        read_only_fields = ['last_updated']


class PointsTransactionSerializer(serializers.ModelSerializer):
    """Serializer for points transactions"""

    user = UserSimpleSerializer(read_only=True)
    created_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = PointsTransaction
        fields = [
            'id', 'user', 'transaction_type', 'points',
            'reason', 'description', 'source_type', 'source_id',
            'created_by', 'created_at'
        ]
        read_only_fields = ['created_at']


# Stats and Analytics Serializers

class EngagementDashboardSerializer(serializers.Serializer):
    """Serializer for engagement dashboard statistics"""

    total_surveys = serializers.IntegerField()
    active_surveys = serializers.IntegerField()
    completed_surveys = serializers.IntegerField()
    average_response_rate = serializers.FloatField()

    total_recognitions = serializers.IntegerField()
    recognitions_received = serializers.IntegerField()
    recognitions_given = serializers.IntegerField()

    user_points = UserPointsSerializer()
    user_badges_count = serializers.IntegerField()

    nps_score = serializers.FloatField()
    engagement_score = serializers.FloatField()

    sentiment_distribution = serializers.DictField()


class LeaderboardSerializer(serializers.Serializer):
    """Serializer for leaderboard data"""

    rank = serializers.IntegerField()
    user = UserSimpleSerializer()
    total_points = serializers.IntegerField()
    level = serializers.IntegerField()
    badges_count = serializers.IntegerField()
