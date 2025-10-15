"""
Serializers for continuous_feedback app API endpoints.
"""
from rest_framework import serializers
from django.utils import timezone
from .models import (
    QuickFeedback, FeedbackBank, PublicRecognition,
    RecognitionLike, RecognitionComment, FeedbackTag
)
from apps.accounts.models import User


class FeedbackTagSerializer(serializers.ModelSerializer):
    """Serializer for FeedbackTag model."""

    class Meta:
        model = FeedbackTag
        fields = ['id', 'name', 'description', 'icon', 'is_active', 'usage_count']
        read_only_fields = ['usage_count']


class QuickFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for QuickFeedback model - Continuous feedback messages."""

    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    feedback_type_display = serializers.CharField(source='get_feedback_type_display', read_only=True)
    visibility_display = serializers.CharField(source='get_visibility_display', read_only=True)
    related_competency_name = serializers.CharField(source='related_competency.name', read_only=True)
    tags_list = FeedbackTagSerializer(source='tags', many=True, read_only=True)

    class Meta:
        model = QuickFeedback
        fields = [
            'id', 'sender', 'sender_name', 'recipient', 'recipient_name',
            'feedback_type', 'feedback_type_display',
            'visibility', 'visibility_display',
            'title', 'message',
            'related_competency', 'related_competency_name',
            'context', 'rating',
            'is_anonymous',
            'is_read', 'read_at',
            'recipient_response', 'responded_at',
            'tags', 'tags_list',
            'created_at', 'updated_at',
            'is_flagged', 'flagged_reason'
        ]
        read_only_fields = ['sender', 'is_read', 'read_at', 'responded_at', 'created_at', 'updated_at']

    def get_sender_name(self, obj):
        """Return sender name or 'Anonim' if anonymous."""
        if obj.is_anonymous:
            return "Anonim"
        return obj.sender.get_full_name()

    def validate(self, data):
        """Validate feedback data."""
        feedback_type = data.get('feedback_type')
        visibility = data.get('visibility')

        # Recognition feedback should typically be public or team
        if feedback_type == 'recognition' and visibility == 'private':
            # This is allowed but we can warn or suggest
            pass

        # Rating validation
        rating = data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise serializers.ValidationError("Qiymət 1-5 arasında olmalıdır.")

        return data


class QuickFeedbackCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating QuickFeedback."""

    class Meta:
        model = QuickFeedback
        fields = [
            'recipient', 'feedback_type', 'visibility',
            'title', 'message',
            'related_competency', 'context', 'rating',
            'is_anonymous', 'tags'
        ]

    def validate(self, data):
        """Validate feedback creation."""
        # Prevent self-feedback
        request = self.context.get('request')
        if request and data.get('recipient') == request.user:
            raise serializers.ValidationError("Özünüzə rəy göndərə bilməzsiniz.")

        return data


class FeedbackResponseSerializer(serializers.Serializer):
    """Serializer for responding to feedback."""

    response = serializers.CharField(required=True, max_length=2000)

    def validate_response(self, value):
        if not value.strip():
            raise serializers.ValidationError("Cavab boş ola bilməz.")
        return value


class FeedbackBankSerializer(serializers.ModelSerializer):
    """Serializer for FeedbackBank model - Aggregated feedback repository."""

    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_position = serializers.CharField(source='user.profile.position.title', read_only=True)

    class Meta:
        model = FeedbackBank
        fields = [
            'id', 'user', 'user_name', 'user_position',
            'total_feedbacks_received', 'total_recognitions', 'total_improvements',
            'average_rating',
            'top_strengths', 'top_improvement_areas',
            'positive_sentiment_score',
            'last_feedback_date', 'last_updated'
        ]
        read_only_fields = [
            'total_feedbacks_received', 'total_recognitions', 'total_improvements',
            'average_rating', 'top_strengths', 'top_improvement_areas',
            'positive_sentiment_score', 'last_feedback_date', 'last_updated'
        ]


class RecognitionLikeSerializer(serializers.ModelSerializer):
    """Serializer for RecognitionLike model."""

    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = RecognitionLike
        fields = ['id', 'recognition', 'user', 'user_name', 'created_at']
        read_only_fields = ['user', 'created_at']


class RecognitionCommentSerializer(serializers.ModelSerializer):
    """Serializer for RecognitionComment model."""

    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_avatar = serializers.CharField(source='user.profile.avatar', read_only=True)

    class Meta:
        model = RecognitionComment
        fields = ['id', 'recognition', 'user', 'user_name', 'user_avatar', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class PublicRecognitionSerializer(serializers.ModelSerializer):
    """Serializer for PublicRecognition model - Public recognition feed."""

    feedback_detail = QuickFeedbackSerializer(source='feedback', read_only=True)
    likes = RecognitionLikeSerializer(many=True, read_only=True)
    comments = RecognitionCommentSerializer(many=True, read_only=True)

    # Engagement counts
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = PublicRecognition
        fields = [
            'id', 'feedback', 'feedback_detail',
            'likes_count', 'comments_count', 'views_count',
            'is_featured', 'featured_until',
            'published_at',
            'likes', 'comments', 'user_has_liked'
        ]
        read_only_fields = ['likes_count', 'comments_count', 'views_count', 'published_at']

    def get_user_has_liked(self, obj):
        """Check if current user has liked this recognition."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PublicRecognitionListSerializer(serializers.ModelSerializer):
    """Simplified serializer for public recognition list view."""

    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.CharField(source='feedback.recipient.get_full_name', read_only=True)
    title = serializers.CharField(source='feedback.title', read_only=True)
    message = serializers.CharField(source='feedback.message', read_only=True)
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = PublicRecognition
        fields = [
            'id', 'sender_name', 'recipient_name',
            'title', 'message',
            'likes_count', 'comments_count', 'views_count',
            'is_featured', 'published_at',
            'user_has_liked'
        ]

    def get_sender_name(self, obj):
        """Return sender name or 'Anonim' if anonymous."""
        if obj.feedback.is_anonymous:
            return "Anonim"
        return obj.feedback.sender.get_full_name()

    def get_user_has_liked(self, obj):
        """Check if current user has liked this recognition."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


# Summary/Statistics Serializers

class FeedbackStatisticsSerializer(serializers.Serializer):
    """Serializer for feedback statistics dashboard."""

    total_feedbacks = serializers.IntegerField()
    total_recognitions = serializers.IntegerField()
    total_improvements = serializers.IntegerField()
    total_users_giving_feedback = serializers.IntegerField()
    total_users_receiving_feedback = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    feedback_trend = serializers.ListField()
    top_contributors = serializers.ListField()
    most_recognized_users = serializers.ListField()


class UserFeedbackSummarySerializer(serializers.Serializer):
    """Serializer for individual user feedback summary."""

    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    feedbacks_received_count = serializers.IntegerField()
    feedbacks_sent_count = serializers.IntegerField()
    recognitions_received = serializers.IntegerField()
    improvements_received = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    unread_feedbacks = serializers.IntegerField()
    recent_feedbacks = QuickFeedbackSerializer(many=True, read_only=True)
