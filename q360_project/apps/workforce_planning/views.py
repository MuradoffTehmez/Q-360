"""
API views for workforce_planning app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Count, Q, Avg
from django.utils import timezone

from .models import TalentMatrix, CriticalRole, SuccessionCandidate, CompetencyGap
from .serializers import (
    TalentMatrixSerializer, TalentMatrixCreateSerializer,
    CriticalRoleSerializer, SuccessionCandidateSerializer,
    CompetencyGapSerializer, CompetencyGapCreateSerializer,
    TalentMatrixSummarySerializer, SuccessionPlanSummarySerializer,
    CompetencyGapSummarySerializer
)
from apps.accounts.permissions import IsSuperAdminOrAdmin


class TalentMatrixViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing 9-Box Talent Matrix assessments.

    Provides:
    - CRUD operations for talent assessments
    - Filtering by user, assessment period, box category
    - Summary statistics endpoint
    - 9-box distribution view
    """

    queryset = TalentMatrix.objects.select_related(
        'user', 'user__profile', 'user__profile__position', 'assessed_by'
    ).order_by('-assessment_date')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'box_category', 'performance_level', 'potential_level', 'assessment_period']
    search_fields = ['user__first_name', 'user__last_name', 'assessment_period']
    ordering_fields = ['assessment_date', 'performance_score', 'potential_score']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TalentMatrixCreateSerializer
        return TalentMatrixSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperAdminOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get talent matrix summary statistics."""
        period = request.query_params.get('period', None)

        queryset = self.get_queryset()
        if period:
            queryset = queryset.filter(assessment_period=period)

        # Box distribution
        box_distribution = {}
        for i in range(1, 10):
            box_key = f'box{i}'
            count = queryset.filter(box_category=box_key).count()
            box_distribution[box_key] = count

        # High potential and high performance counts
        high_potential_count = queryset.filter(potential_level='high').count()
        high_performance_count = queryset.filter(performance_level='high').count()
        top_talent_count = queryset.filter(
            performance_level='high',
            potential_level='high'
        ).count()

        summary_data = {
            'total_assessments': queryset.count(),
            'box_distribution': box_distribution,
            'high_potential_count': high_potential_count,
            'high_performance_count': high_performance_count,
            'top_talent_count': top_talent_count,
            'assessment_period': period or 'All'
        }

        serializer = TalentMatrixSummarySerializer(summary_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def matrix_view(self, request):
        """Get 9-box matrix view with users categorized."""
        period = request.query_params.get('period', None)

        queryset = self.get_queryset()
        if period:
            queryset = queryset.filter(assessment_period=period)

        matrix = {}
        for i in range(1, 10):
            box_key = f'box{i}'
            users = queryset.filter(box_category=box_key)
            matrix[box_key] = TalentMatrixSerializer(users, many=True).data

        return Response(matrix)

    @action(detail=False, methods=['get'])
    def my_assessment(self, request):
        """Get the authenticated user's latest talent assessment."""
        latest = self.get_queryset().filter(user=request.user).first()
        if latest:
            serializer = self.get_serializer(latest)
            return Response(serializer.data)
        return Response({'detail': 'Qiymətləndirmə tapılmadı.'}, status=status.HTTP_404_NOT_FOUND)


class CriticalRoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing critical roles and succession planning.

    Provides:
    - CRUD operations for critical role designations
    - Filtering by criticality level, readiness, status
    - Succession planning dashboard
    - Role coverage analysis
    """

    queryset = CriticalRole.objects.select_related(
        'position', 'current_holder'
    ).prefetch_related('required_competencies', 'succession_candidates')
    serializer_class = CriticalRoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['criticality_level', 'succession_readiness', 'is_active']
    search_fields = ['position__title', 'current_holder__first_name', 'current_holder__last_name']
    ordering_fields = ['criticality_level', 'designated_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperAdminOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def succession_summary(self, request):
        """Get succession planning summary statistics."""
        active_roles = self.get_queryset().filter(is_active=True)

        total_critical_roles = active_roles.count()
        roles_with_successors = active_roles.exclude(succession_readiness='no_successor').count()
        roles_without_successors = active_roles.filter(succession_readiness='no_successor').count()
        ready_now_count = active_roles.filter(succession_readiness='ready_now').count()
        needs_development_count = active_roles.filter(succession_readiness='needs_development').count()

        succession_coverage_rate = 0
        if total_critical_roles > 0:
            succession_coverage_rate = (roles_with_successors / total_critical_roles) * 100

        summary_data = {
            'total_critical_roles': total_critical_roles,
            'roles_with_successors': roles_with_successors,
            'roles_without_successors': roles_without_successors,
            'ready_now_count': ready_now_count,
            'needs_development_count': needs_development_count,
            'succession_coverage_rate': round(succession_coverage_rate, 2)
        }

        serializer = SuccessionPlanSummarySerializer(summary_data)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def candidates(self, request, pk=None):
        """Get all succession candidates for this critical role."""
        role = self.get_object()
        candidates = role.succession_candidates.filter(is_active=True)
        serializer = SuccessionCandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_readiness(self, request, pk=None):
        """Update succession readiness status for a critical role."""
        role = self.get_object()
        new_readiness = request.data.get('succession_readiness')

        if new_readiness not in dict(CriticalRole._meta.get_field('succession_readiness').choices):
            return Response(
                {'detail': 'Yanlış hazırlıq statusu.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        role.succession_readiness = new_readiness
        role.save()

        serializer = self.get_serializer(role)
        return Response(serializer.data)


class SuccessionCandidateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing succession candidates.

    Provides:
    - CRUD operations for succession candidates
    - Filtering by role, readiness level, status
    - Candidate readiness tracking
    - Development plan management
    """

    queryset = SuccessionCandidate.objects.select_related(
        'critical_role', 'critical_role__position',
        'candidate', 'candidate__profile', 'candidate__profile__position',
        'nominated_by'
    ).order_by('-readiness_score')
    serializer_class = SuccessionCandidateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['critical_role', 'candidate', 'readiness_level', 'is_active']
    search_fields = ['candidate__first_name', 'candidate__last_name', 'critical_role__position__title']
    ordering_fields = ['readiness_score', 'nomination_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperAdminOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(nominated_by=self.request.user)

    @action(detail=False, methods=['get'])
    def my_candidacies(self, request):
        """Get succession candidacies for the authenticated user."""
        candidacies = self.get_queryset().filter(candidate=request.user, is_active=True)
        serializer = self.get_serializer(candidacies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_readiness(self, request, pk=None):
        """Update readiness level and score for a candidate."""
        candidate = self.get_object()

        readiness_level = request.data.get('readiness_level')
        readiness_score = request.data.get('readiness_score')

        if readiness_level:
            candidate.readiness_level = readiness_level
        if readiness_score is not None:
            candidate.readiness_score = readiness_score

        candidate.save()
        serializer = self.get_serializer(candidate)
        return Response(serializer.data)


class CompetencyGapViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing competency gap analysis.

    Provides:
    - CRUD operations for competency gaps
    - Filtering by user, competency, status, priority
    - Gap summary and statistics
    - Training recommendations
    - Gap closure tracking
    """

    queryset = CompetencyGap.objects.select_related(
        'user', 'competency', 'current_level', 'target_level', 'target_position'
    ).prefetch_related('recommended_trainings').order_by('-priority', '-gap_score')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'competency', 'gap_status', 'priority', 'is_closed']
    search_fields = ['user__first_name', 'user__last_name', 'competency__name']
    ordering_fields = ['gap_score', 'priority', 'identified_date']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CompetencyGapCreateSerializer
        return CompetencyGapSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperAdminOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get competency gap analysis summary."""
        queryset = self.get_queryset()

        total_gaps = queryset.count()
        open_gaps = queryset.filter(is_closed=False).count()
        closed_gaps = queryset.filter(is_closed=True).count()
        major_gaps_count = queryset.filter(gap_status='major_gap', is_closed=False).count()
        high_priority_count = queryset.filter(priority='high', is_closed=False).count()

        average_gap_score = queryset.filter(is_closed=False).aggregate(
            avg=Avg('gap_score')
        )['avg'] or 0

        # Top gap areas
        top_gaps = queryset.filter(is_closed=False).values(
            'competency__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        top_gap_areas = [
            {'competency': gap['competency__name'], 'count': gap['count']}
            for gap in top_gaps
        ]

        summary_data = {
            'total_gaps': total_gaps,
            'open_gaps': open_gaps,
            'closed_gaps': closed_gaps,
            'major_gaps_count': major_gaps_count,
            'high_priority_count': high_priority_count,
            'average_gap_score': round(average_gap_score, 2),
            'top_gap_areas': top_gap_areas
        }

        serializer = CompetencyGapSummarySerializer(summary_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_gaps(self, request):
        """Get competency gaps for the authenticated user."""
        gaps = self.get_queryset().filter(user=request.user, is_closed=False)
        serializer = self.get_serializer(gaps, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def close_gap(self, request, pk=None):
        """Close a competency gap with notes."""
        gap = self.get_object()

        if gap.is_closed:
            return Response(
                {'detail': 'Bu boşluq artıq bağlanmışdır.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        closure_notes = request.data.get('closure_notes', '')

        gap.is_closed = True
        gap.closed_date = timezone.now().date()
        gap.closure_notes = closure_notes
        gap.save()

        serializer = self.get_serializer(gap)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reopen_gap(self, request, pk=None):
        """Reopen a closed competency gap."""
        gap = self.get_object()

        if not gap.is_closed:
            return Response(
                {'detail': 'Bu boşluq artıq açıqdır.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        gap.is_closed = False
        gap.closed_date = None
        gap.save()

        serializer = self.get_serializer(gap)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_competency(self, request):
        """Get gaps grouped by competency."""
        competency_id = request.query_params.get('competency_id')

        if not competency_id:
            return Response(
                {'detail': 'competency_id parametri tələb olunur.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        gaps = self.get_queryset().filter(
            competency_id=competency_id,
            is_closed=False
        )
        serializer = self.get_serializer(gaps, many=True)
        return Response(serializer.data)
