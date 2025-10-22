from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import (
    PulseSurvey, SurveyQuestion, SurveyResponse,
    EngagementScore, Recognition, AnonymousFeedback,
    SentimentAnalysis, GamificationBadge, UserBadge,
    UserPoints, PointsTransaction
)
from .serializers import (
    PulseSurveySerializer, SurveyQuestionSerializer, SurveyResponseSerializer,
    EngagementScoreSerializer, RecognitionSerializer, RecognitionCreateSerializer,
    AnonymousFeedbackSerializer, SentimentAnalysisSerializer,
    GamificationBadgeSerializer, UserBadgeSerializer,
    UserPointsSerializer, PointsTransactionSerializer,
    EngagementDashboardSerializer, LeaderboardSerializer
)


class PulseSurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Pulse Surveys
    """
    queryset = PulseSurvey.objects.all()
    serializer_class = PulseSurveySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter surveys based on user access"""
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return PulseSurvey.objects.all()

        return PulseSurvey.objects.filter(
            Q(target_users=user) | Q(target_departments=user.department)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get survey results and analytics"""
        survey = self.get_object()

        responses = SurveyResponse.objects.filter(survey=survey)

        # Calculate response rate
        total_targets = survey.target_users.count()
        total_responses = responses.values('user').distinct().count()
        response_rate = (total_responses / total_targets * 100) if total_targets > 0 else 0

        # Question-wise analysis
        questions_data = []
        for question in survey.questions.all():
            question_responses = responses.filter(question=question)

            if question.question_type in ['rating', 'nps']:
                avg_rating = question_responses.aggregate(avg=Avg('rating_value'))['avg']
                questions_data.append({
                    'question': question.question_text,
                    'type': question.question_type,
                    'average_rating': round(avg_rating, 2) if avg_rating else 0,
                    'response_count': question_responses.count()
                })
            elif question.question_type == 'yes_no':
                yes_count = question_responses.filter(boolean_value=True).count()
                no_count = question_responses.filter(boolean_value=False).count()
                questions_data.append({
                    'question': question.question_text,
                    'type': question.question_type,
                    'yes_count': yes_count,
                    'no_count': no_count,
                    'yes_percentage': (yes_count / question_responses.count() * 100) if question_responses.count() > 0 else 0
                })
            elif question.question_type == 'text':
                text_responses = list(question_responses.values_list('text_value', flat=True))
                questions_data.append({
                    'question': question.question_text,
                    'type': question.question_type,
                    'responses': text_responses
                })

        return Response({
            'survey': PulseSurveySerializer(survey).data,
            'response_rate': response_rate,
            'total_responses': total_responses,
            'questions_analysis': questions_data
        })

    @action(detail=True, methods=['post'])
    def submit_response(self, request, pk=None):
        """Submit survey response"""
        survey = self.get_object()
        user = request.user

        # Check if already responded
        if SurveyResponse.objects.filter(survey=survey, user=user).exists():
            return Response(
                {'error': 'You have already responded to this survey'},
                status=status.HTTP_400_BAD_REQUEST
            )

        responses_data = request.data.get('responses', [])

        for response_data in responses_data:
            SurveyResponse.objects.create(
                survey=survey,
                question_id=response_data['question_id'],
                user=user if not survey.is_anonymous else None,
                rating_value=response_data.get('rating_value'),
                text_value=response_data.get('text_value'),
                boolean_value=response_data.get('boolean_value')
            )

        # Award points
        user_points, created = UserPoints.objects.get_or_create(user=user)
        user_points.add_points(20, category='collaboration')

        return Response({'message': 'Survey response submitted successfully'}, status=status.HTTP_201_CREATED)


class EngagementScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Engagement Scores (Read-only)
    """
    queryset = EngagementScore.objects.all()
    serializer_class = EngagementScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter scores for current user or their team"""
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return EngagementScore.objects.all()

        return EngagementScore.objects.filter(Q(user=user) | Q(department=user.department))

    @action(detail=False, methods=['get'])
    def my_scores(self, request):
        """Get current user's engagement scores"""
        scores = EngagementScore.objects.filter(user=request.user).order_by('-calculated_at')[:10]
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def team_average(self, request):
        """Get team average engagement score"""
        user = request.user

        if not user.department:
            return Response({'error': 'User not assigned to any department'}, status=status.HTTP_400_BAD_REQUEST)

        avg_score = EngagementScore.objects.filter(
            department=user.department,
            calculated_at__gte=timezone.now() - timedelta(days=30)
        ).aggregate(avg=Avg('score_value'))

        return Response({'team_average': avg_score['avg'] or 0})


class RecognitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Recognitions
    """
    queryset = Recognition.objects.filter(is_public=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return RecognitionCreateSerializer
        return RecognitionSerializer

    def perform_create(self, serializer):
        recognition = serializer.save(given_by=self.request.user)

        # Award points
        recipient_points, created = UserPoints.objects.get_or_create(user=recognition.given_to)
        recipient_points.add_points(recognition.points, category='collaboration')

        PointsTransaction.objects.create(
            user=recognition.given_to,
            transaction_type='awarded',
            points=recognition.points,
            reason='Recognition Received',
            source_type='recognition',
            source_id=recognition.id,
            created_by=self.request.user
        )

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a recognition"""
        recognition = self.get_object()
        user = request.user

        if user in recognition.liked_by.all():
            recognition.liked_by.remove(user)
            recognition.likes_count -= 1
            liked = False
        else:
            recognition.liked_by.add(user)
            recognition.likes_count += 1
            liked = True

        recognition.save()

        return Response({
            'liked': liked,
            'likes_count': recognition.likes_count
        })

    @action(detail=False, methods=['get'])
    def my_recognitions(self, request):
        """Get recognitions received by current user"""
        recognitions = Recognition.objects.filter(given_to=request.user).order_by('-created_at')
        serializer = self.get_serializer(recognitions, many=True)
        return Response(serializer.data)


class AnonymousFeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Anonymous Feedback
    """
    queryset = AnonymousFeedback.objects.all()
    serializer_class = AnonymousFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Staff can see all feedback, users can see only their submitted feedback"""
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return AnonymousFeedback.objects.all()

        # Users can track their feedback via anonymous_id (stored in session)
        return AnonymousFeedback.objects.none()

    def perform_create(self, serializer):
        feedback = serializer.save()

        # Run sentiment analysis
        from .services import analyze_sentiment
        sentiment_result = analyze_sentiment(feedback.message)

        feedback.sentiment_score = sentiment_result.get('score')
        feedback.sentiment_label = sentiment_result.get('label')
        feedback.save()


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Leaderboard
    """
    queryset = UserPoints.objects.select_related('user').order_by('-total_points')
    serializer_class = UserPointsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top 20 performers"""
        period = request.query_params.get('period', 'all')

        if period == 'month':
            start_date = timezone.now() - timedelta(days=30)
            top_users = PointsTransaction.objects.filter(
                created_at__gte=start_date
            ).values('user').annotate(
                total_points=Count('points')
            ).order_by('-total_points')[:20]

            user_ids = [item['user'] for item in top_users]
            leaderboard = UserPoints.objects.filter(user_id__in=user_ids).select_related('user')
        else:
            leaderboard = self.get_queryset()[:20]

        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)


class GamificationBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Gamification Badges (Read-only)
    """
    queryset = GamificationBadge.objects.filter(is_active=True)
    serializer_class = GamificationBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for User Badges (Read-only)
    """
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter badges for current user"""
        return UserBadge.objects.filter(user=self.request.user)


class DashboardViewSet(viewsets.ViewSet):
    """
    API endpoint for Engagement Dashboard
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Get engagement dashboard data"""
        user = request.user

        # Surveys stats
        active_surveys = PulseSurvey.objects.filter(
            status='active',
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).filter(
            Q(target_users=user) | Q(target_departments=user.department)
        ).distinct()

        # Recognitions stats
        recognitions_received = Recognition.objects.filter(given_to=user).count()
        recognitions_given = Recognition.objects.filter(given_by=user).count()

        # Points and badges
        user_points, created = UserPoints.objects.get_or_create(user=user)
        user_badges_count = UserBadge.objects.filter(user=user).count()

        # Engagement scores
        latest_scores = EngagementScore.objects.filter(user=user).order_by('-calculated_at')[:5]

        nps_score = latest_scores.filter(score_type='nps').first()
        engagement_score = latest_scores.filter(score_type='engagement').first()

        # Sentiment distribution
        sentiment_data = SentimentAnalysis.objects.filter(
            analyzed_at__gte=timezone.now() - timedelta(days=30)
        ).values('sentiment').annotate(count=Count('id'))

        sentiment_distribution = {item['sentiment']: item['count'] for item in sentiment_data}

        data = {
            'total_surveys': active_surveys.count(),
            'active_surveys': active_surveys.count(),
            'completed_surveys': SurveyResponse.objects.filter(user=user).values('survey').distinct().count(),
            'average_response_rate': 0,  # Calculate this based on your needs

            'total_recognitions': recognitions_received + recognitions_given,
            'recognitions_received': recognitions_received,
            'recognitions_given': recognitions_given,

            'user_points': UserPointsSerializer(user_points).data,
            'user_badges_count': user_badges_count,

            'nps_score': nps_score.score_value if nps_score else 0,
            'engagement_score': engagement_score.score_value if engagement_score else 0,

            'sentiment_distribution': sentiment_distribution,
        }

        serializer = EngagementDashboardSerializer(data)
        return Response(serializer.data)
