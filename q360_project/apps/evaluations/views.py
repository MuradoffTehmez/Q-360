"""
API views for evaluations app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import (
    EvaluationCampaign, QuestionCategory, Question,
    EvaluationAssignment, Response as EvalResponse, EvaluationResult
)
from .serializers import (
    EvaluationCampaignSerializer, QuestionCategorySerializer,
    QuestionSerializer, EvaluationAssignmentSerializer,
    ResponseSerializer, EvaluationResultSerializer
)
from apps.accounts.permissions import IsSuperAdminOrAdmin


class EvaluationCampaignViewSet(viewsets.ModelViewSet):
    """ViewSet for managing evaluation campaigns."""

    queryset = EvaluationCampaign.objects.all()
    serializer_class = EvaluationCampaignSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperAdminOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        campaign = self.get_object()
        campaign.status = 'active'
        campaign.save()
        return Response({'detail': 'Kampaniya aktivləşdirildi.'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        campaign = self.get_object()
        campaign.status = 'completed'
        campaign.save()
        return Response({'detail': 'Kampaniya tamamlandı.'})


class QuestionCategoryViewSet(viewsets.ModelViewSet):
    queryset = QuestionCategory.objects.all()
    serializer_class = QuestionCategorySerializer
    permission_classes = [IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related('category')
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'question_type', 'is_active']


class EvaluationAssignmentViewSet(viewsets.ModelViewSet):
    queryset = EvaluationAssignment.objects.select_related(
        'campaign', 'evaluator', 'evaluatee'
    ).prefetch_related('responses')
    serializer_class = EvaluationAssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['campaign', 'evaluator', 'evaluatee', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return super().get_queryset()
        return super().get_queryset().filter(evaluator=user)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        assignment = self.get_object()
        assignment.status = 'in_progress'
        assignment.started_at = timezone.now()
        assignment.save()
        return Response({'detail': 'Qiymətləndirmə başladıldı.'})

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        assignment = self.get_object()
        assignment.status = 'completed'
        assignment.completed_at = timezone.now()
        assignment.save()
        return Response({'detail': 'Qiymətləndirmə təqdim edildi.'})


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = EvalResponse.objects.select_related('assignment', 'question')
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assignment', 'question']


class EvaluationResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EvaluationResult.objects.select_related('campaign', 'evaluatee')
    serializer_class = EvaluationResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['campaign', 'evaluatee', 'is_finalized']

    @action(detail=True, methods=['post'])
    def recalculate(self, request, pk=None):
        result = self.get_object()
        result.calculate_scores()
        return Response({'detail': 'Nəticələr yenidən hesablandı.'})
