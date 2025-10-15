"""
API views for continuous_feedback app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Count, Q, Avg, F
from django.utils import timezone
from datetime import timedelta

from .models import (
    QuickFeedback, FeedbackBank, PublicRecognition,
    RecognitionLike, RecognitionComment, FeedbackTag
)
from .serializers import (
    QuickFeedbackSerializer, QuickFeedbackCreateSerializer,
    FeedbackResponseSerializer, FeedbackBankSerializer,
    PublicRecognitionSerializer, PublicRecognitionListSerializer,
    RecognitionLikeSerializer, RecognitionCommentSerializer,
    FeedbackTagSerializer,
    FeedbackStatisticsSerializer, UserFeedbackSummarySerializer
)


class QuickFeedbackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing quick feedback (continuous feedback system).

    Provides:
    - Send feedback to colleagues (recognition or improvement)
    - View received and sent feedbacks
    - Mark feedback as read
    - Respond to feedback
    - Filter by type, visibility, status
    """

    queryset = QuickFeedback.objects.select_related(
        'sender', 'recipient', 'related_competency'
    ).prefetch_related('tags').order_by('-created_at')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['feedback_type', 'visibility', 'is_read', 'sender', 'recipient']
    search_fields = ['title', 'message', 'recipient__first_name', 'recipient__last_name']
    ordering_fields = ['created_at', 'rating']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return QuickFeedbackCreateSerializer
        return QuickFeedbackSerializer

    def get_queryset(self):
        """Filter feedbacks based on user role and permissions."""
        user = self.request.user

        if user.is_admin():
            return super().get_queryset()

        # Regular users can see:
        # 1. Feedbacks they sent
        # 2. Feedbacks they received
        # 3. Public feedbacks
        return super().get_queryset().filter(
            Q(sender=user) | Q(recipient=user) | Q(visibility='public')
        )

    def perform_create(self, serializer):
        """Create feedback and update feedback bank."""
        feedback = serializer.save(sender=self.request.user)

        # Update or create feedback bank for recipient
        feedback_bank, created = FeedbackBank.objects.get_or_create(
            user=feedback.recipient
        )
        feedback_bank.update_stats()

        # Create public recognition if applicable
        if feedback.feedback_type == 'recognition' and feedback.visibility == 'public':
            PublicRecognition.objects.create(feedback=feedback)

    @action(detail=False, methods=['get'])
    def my_received_feedbacks(self, request):
        """Get feedbacks received by the authenticated user."""
        feedbacks = self.get_queryset().filter(recipient=request.user)

        # Apply filters
        feedback_type = request.query_params.get('feedback_type')
        is_read = request.query_params.get('is_read')

        if feedback_type:
            feedbacks = feedbacks.filter(feedback_type=feedback_type)
        if is_read is not None:
            feedbacks = feedbacks.filter(is_read=is_read.lower() == 'true')

        page = self.paginate_queryset(feedbacks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(feedbacks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_sent_feedbacks(self, request):
        """Get feedbacks sent by the authenticated user."""
        feedbacks = self.get_queryset().filter(sender=request.user)

        page = self.paginate_queryset(feedbacks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(feedbacks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark feedback as read."""
        feedback = self.get_object()

        if feedback.recipient != request.user:
            return Response(
                {'detail': 'Bu rəyi yalnız alan şəxs oxuya bilər.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not feedback.is_read:
            feedback.is_read = True
            feedback.read_at = timezone.now()
            feedback.save()

        serializer = self.get_serializer(feedback)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """Respond to received feedback."""
        feedback = self.get_object()

        if feedback.recipient != request.user:
            return Response(
                {'detail': 'Bu rəyə yalnız alan şəxs cavab verə bilər.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = FeedbackResponseSerializer(data=request.data)
        if serializer.is_valid():
            feedback.recipient_response = serializer.validated_data['response']
            feedback.responded_at = timezone.now()
            feedback.save()

            response_serializer = self.get_serializer(feedback)
            return Response(response_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def flag(self, request, pk=None):
        """Flag feedback as inappropriate."""
        feedback = self.get_object()
        reason = request.data.get('reason', '')

        if not reason:
            return Response(
                {'detail': 'Bildirmə səbəbi tələb olunur.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        feedback.is_flagged = True
        feedback.flagged_reason = reason
        feedback.save()

        return Response({'detail': 'Rəy bildirildi. Admin tərəfindən yoxlanılacaq.'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread feedbacks for the authenticated user."""
        count = QuickFeedback.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        return Response({'unread_count': count})


class FeedbackBankViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing feedback banks (aggregated feedback repositories).

    Provides:
    - View user's feedback bank with statistics
    - Access aggregated feedback data
    - View top strengths and improvement areas
    """

    queryset = FeedbackBank.objects.select_related('user').order_by('-total_feedbacks_received')
    serializer_class = FeedbackBankSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user']
    search_fields = ['user__first_name', 'user__last_name']

    def get_queryset(self):
        """Regular users can only see their own feedback bank."""
        user = self.request.user

        if user.is_admin():
            return super().get_queryset()

        return super().get_queryset().filter(user=user)

    @action(detail=False, methods=['get'])
    def my_bank(self, request):
        """Get the authenticated user's feedback bank."""
        feedback_bank, created = FeedbackBank.objects.get_or_create(user=request.user)

        # Update stats if needed
        if created or not feedback_bank.last_feedback_date:
            feedback_bank.update_stats()

        serializer = self.get_serializer(feedback_bank)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def refresh_stats(self, request, pk=None):
        """Manually refresh feedback bank statistics."""
        feedback_bank = self.get_object()
        feedback_bank.update_stats()
        serializer = self.get_serializer(feedback_bank)
        return Response(serializer.data)


class PublicRecognitionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for public recognition feed.

    Provides:
    - View public recognition posts
    - Like and unlike recognitions
    - Comment on recognitions
    - View featured recognitions
    - Track engagement (views, likes, comments)
    """

    queryset = PublicRecognition.objects.select_related(
        'feedback', 'feedback__sender', 'feedback__recipient'
    ).prefetch_related('likes', 'comments').order_by('-published_at')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_featured']
    ordering_fields = ['published_at', 'likes_count', 'comments_count']

    def get_serializer_class(self):
        if self.action == 'list':
            return PublicRecognitionListSerializer
        return PublicRecognitionSerializer

    def retrieve(self, request, *args, **kwargs):
        """Increment view count when retrieving a recognition."""
        instance = self.get_object()
        instance.views_count = F('views_count') + 1
        instance.save(update_fields=['views_count'])
        instance.refresh_from_db()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured recognitions."""
        featured = self.get_queryset().filter(
            is_featured=True,
            featured_until__gte=timezone.now()
        )
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending recognitions (most liked/commented recently)."""
        # Recognitions from last 7 days, ordered by engagement
        week_ago = timezone.now() - timedelta(days=7)
        trending = self.get_queryset().filter(
            published_at__gte=week_ago
        ).annotate(
            engagement=F('likes_count') + F('comments_count')
        ).order_by('-engagement')[:10]

        serializer = self.get_serializer(trending, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a public recognition."""
        recognition = self.get_object()

        # Check if already liked
        like, created = RecognitionLike.objects.get_or_create(
            recognition=recognition,
            user=request.user
        )

        if not created:
            return Response(
                {'detail': 'Artıq bəyənmişsiniz.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update like count
        recognition.likes_count = F('likes_count') + 1
        recognition.save(update_fields=['likes_count'])
        recognition.refresh_from_db()

        serializer = self.get_serializer(recognition)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Unlike a public recognition."""
        recognition = self.get_object()

        try:
            like = RecognitionLike.objects.get(
                recognition=recognition,
                user=request.user
            )
            like.delete()

            # Update like count
            recognition.likes_count = F('likes_count') - 1
            recognition.save(update_fields=['likes_count'])
            recognition.refresh_from_db()

            serializer = self.get_serializer(recognition)
            return Response(serializer.data)

        except RecognitionLike.DoesNotExist:
            return Response(
                {'detail': 'Bəyənməmisiniz.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to a public recognition."""
        recognition = self.get_object()
        comment_text = request.data.get('comment')

        if not comment_text or not comment_text.strip():
            return Response(
                {'detail': 'Şərh boş ola bilməz.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        comment = RecognitionComment.objects.create(
            recognition=recognition,
            user=request.user,
            comment=comment_text
        )

        # Update comment count
        recognition.comments_count = F('comments_count') + 1
        recognition.save(update_fields=['comments_count'])
        recognition.refresh_from_db()

        comment_serializer = RecognitionCommentSerializer(comment)
        return Response(comment_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def delete_comment(self, request, pk=None):
        """Delete a comment from a public recognition."""
        recognition = self.get_object()
        comment_id = request.data.get('comment_id')

        if not comment_id:
            return Response(
                {'detail': 'comment_id tələb olunur.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            comment = RecognitionComment.objects.get(
                id=comment_id,
                recognition=recognition
            )

            # Only comment author or admin can delete
            if comment.user != request.user and not request.user.is_admin():
                return Response(
                    {'detail': 'Bu şərhi silmək üçün icazəniz yoxdur.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            comment.delete()

            # Update comment count
            recognition.comments_count = F('comments_count') - 1
            recognition.save(update_fields=['comments_count'])
            recognition.refresh_from_db()

            return Response({'detail': 'Şərh silindi.'})

        except RecognitionComment.DoesNotExist:
            return Response(
                {'detail': 'Şərh tapılmadı.'},
                status=status.HTTP_404_NOT_FOUND
            )


class FeedbackTagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing feedback tags.

    Provides:
    - CRUD operations for feedback tags
    - View popular tags
    - Tag usage statistics
    """

    queryset = FeedbackTag.objects.filter(is_active=True).order_by('name')
    serializer_class = FeedbackTagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'usage_count']

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular feedback tags."""
        popular_tags = self.get_queryset().order_by('-usage_count')[:10]
        serializer = self.get_serializer(popular_tags, many=True)
        return Response(serializer.data)


# Analytics & Statistics Views

class FeedbackStatisticsViewSet(viewsets.ViewSet):
    """
    ViewSet for feedback statistics and analytics.

    Provides:
    - Overall feedback statistics
    - User feedback summary
    - Feedback trends
    - Top contributors
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get overall feedback statistics."""
        # Total counts
        total_feedbacks = QuickFeedback.objects.count()
        total_recognitions = QuickFeedback.objects.filter(feedback_type='recognition').count()
        total_improvements = QuickFeedback.objects.filter(feedback_type='improvement').count()

        # Unique users
        total_users_giving = QuickFeedback.objects.values('sender').distinct().count()
        total_users_receiving = QuickFeedback.objects.values('recipient').distinct().count()

        # Average rating
        avg_rating = QuickFeedback.objects.filter(rating__isnull=False).aggregate(
            avg=Avg('rating')
        )['avg'] or 0

        # Feedback trend (last 7 days)
        feedback_trend = []
        for i in range(7):
            date = timezone.now().date() - timedelta(days=i)
            count = QuickFeedback.objects.filter(created_at__date=date).count()
            feedback_trend.append({
                'date': date.isoformat(),
                'count': count
            })

        # Top contributors
        top_contributors = QuickFeedback.objects.values(
            'sender__id', 'sender__first_name', 'sender__last_name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        top_contributors_list = [
            {
                'user_id': contrib['sender__id'],
                'user_name': f"{contrib['sender__first_name']} {contrib['sender__last_name']}",
                'feedbacks_given': contrib['count']
            }
            for contrib in top_contributors
        ]

        # Most recognized users
        most_recognized = QuickFeedback.objects.filter(
            feedback_type='recognition'
        ).values(
            'recipient__id', 'recipient__first_name', 'recipient__last_name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        most_recognized_list = [
            {
                'user_id': user['recipient__id'],
                'user_name': f"{user['recipient__first_name']} {user['recipient__last_name']}",
                'recognitions_received': user['count']
            }
            for user in most_recognized
        ]

        statistics = {
            'total_feedbacks': total_feedbacks,
            'total_recognitions': total_recognitions,
            'total_improvements': total_improvements,
            'total_users_giving_feedback': total_users_giving,
            'total_users_receiving_feedback': total_users_receiving,
            'average_rating': round(avg_rating, 2),
            'feedback_trend': feedback_trend,
            'top_contributors': top_contributors_list,
            'most_recognized_users': most_recognized_list
        }

        serializer = FeedbackStatisticsSerializer(statistics)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_summary(self, request):
        """Get feedback summary for the authenticated user."""
        user = request.user

        feedbacks_received = QuickFeedback.objects.filter(recipient=user)
        feedbacks_sent = QuickFeedback.objects.filter(sender=user)

        recognitions_received = feedbacks_received.filter(feedback_type='recognition').count()
        improvements_received = feedbacks_received.filter(feedback_type='improvement').count()

        avg_rating = feedbacks_received.filter(rating__isnull=False).aggregate(
            avg=Avg('rating')
        )['avg'] or 0

        unread_feedbacks = feedbacks_received.filter(is_read=False).count()

        # Recent feedbacks (last 5)
        recent_feedbacks = feedbacks_received.order_by('-created_at')[:5]

        summary = {
            'user_id': user.id,
            'user_name': user.get_full_name(),
            'feedbacks_received_count': feedbacks_received.count(),
            'feedbacks_sent_count': feedbacks_sent.count(),
            'recognitions_received': recognitions_received,
            'improvements_received': improvements_received,
            'average_rating': round(avg_rating, 2),
            'unread_feedbacks': unread_feedbacks,
            'recent_feedbacks': recent_feedbacks
        }

        serializer = UserFeedbackSummarySerializer(summary)
        return Response(serializer.data)
