"""
Views for competencies app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from django.db.models import Count, Q
from django.utils import timezone

from .models import Competency, ProficiencyLevel, PositionCompetency, UserSkill
from .serializers import (
    CompetencySerializer,
    CompetencyDetailSerializer,
    ProficiencyLevelSerializer,
    PositionCompetencySerializer,
    UserSkillSerializer,
    UserSkillDetailSerializer,
    UserSkillApprovalSerializer,
)


class CompetencyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Competency model.
    Requires Admin role for create, update, delete operations.
    """

    queryset = Competency.objects.all()
    serializer_class = CompetencySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_active', 'name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    renderer_classes = [JSONRenderer]  # Only JSON, no browsable API

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action."""
        if self.action == 'retrieve':
            return CompetencyDetailSerializer
        return CompetencySerializer

    def get_permissions(self):
        """
        Admin və superadmin rolları create, update, delete üçün icazəlidir.
        Digər istifadəçilər yalnız oxuya bilər.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            from apps.accounts.rbac import RoleManager
            user = self.request.user
            if not RoleManager.is_admin(user):
                self.permission_denied(
                    self.request,
                    message="Bu əməliyyat üçün Admin icazəsi tələb olunur."
                )
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def positions(self, request, pk=None):
        """Kompetensiyanın əlaqəli olduğu vəzifələri qaytarır."""
        competency = self.get_object()
        position_competencies = competency.position_competencies.filter(
            position__is_active=True
        ).select_related('position', 'required_level')

        serializer = PositionCompetencySerializer(position_competencies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """Bu kompetensiyaya malik istifadəçiləri qaytarır."""
        competency = self.get_object()
        user_skills = competency.user_skills.filter(
            is_approved=True,
            user__is_active=True
        ).select_related('user', 'level')

        serializer = UserSkillSerializer(user_skills, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Kompetensiya statistikalarını qaytarır."""
        total_competencies = Competency.objects.filter(is_active=True).count()
        total_skills = UserSkill.objects.filter(is_approved=True).count()
        pending_approvals = UserSkill.objects.filter(approval_status='pending').count()

        most_common_competencies = Competency.objects.annotate(
            skill_count=Count('user_skills', filter=Q(user_skills__is_approved=True))
        ).order_by('-skill_count')[:10]

        return Response({
            'total_competencies': total_competencies,
            'total_skills': total_skills,
            'pending_approvals': pending_approvals,
            'most_common_competencies': CompetencySerializer(
                most_common_competencies,
                many=True
            ).data,
        })


class ProficiencyLevelViewSet(viewsets.ModelViewSet):
    """ViewSet for ProficiencyLevel model."""

    queryset = ProficiencyLevel.objects.all()
    serializer_class = ProficiencyLevelSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['score_min']

    def get_permissions(self):
        """Admin rolları create, update, delete üçün icazəlidir."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            from apps.accounts.rbac import RoleManager
            user = self.request.user
            if not RoleManager.is_admin(user):
                self.permission_denied(
                    self.request,
                    message="Bu əməliyyat üçün Admin icazəsi tələb olunur."
                )
        return super().get_permissions()


class PositionCompetencyViewSet(viewsets.ModelViewSet):
    """ViewSet for PositionCompetency model."""

    queryset = PositionCompetency.objects.select_related(
        'position',
        'competency',
        'required_level'
    )
    serializer_class = PositionCompetencySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['position', 'competency', 'is_mandatory']
    ordering = ['-weight', 'competency__name']

    def get_permissions(self):
        """Admin və manager rolları create, update, delete üçün icazəlidir."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            from apps.accounts.rbac import RoleManager
            user = self.request.user
            if not RoleManager.is_manager(user):
                self.permission_denied(
                    self.request,
                    message="Bu əməliyyat üçün Manager icazəsi tələb olunur."
                )
        return super().get_permissions()


class UserSkillViewSet(viewsets.ModelViewSet):
    """ViewSet for UserSkill model."""

    queryset = UserSkill.objects.select_related(
        'user',
        'competency',
        'level',
        'approved_by'
    )
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user', 'competency', 'is_approved', 'approval_status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action."""
        if self.action == 'retrieve':
            return UserSkillDetailSerializer
        return UserSkillSerializer

    def get_queryset(self):
        """
        İstifadəçilər yalnız öz bacarıqlarını görə bilər.
        Manager və admin rolları bütün bacarıqları görə bilər.
        """
        from apps.accounts.rbac import RoleManager
        user = self.request.user

        if RoleManager.is_manager(user):
            return self.queryset.all()

        # Regular users can only see their own skills
        return self.queryset.filter(user=user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Bacarığı təsdiq et (Manager və Admin üçün)."""
        from apps.accounts.rbac import RoleManager

        if not RoleManager.is_manager(request.user):
            return Response(
                {'detail': 'Bu əməliyyat üçün Manager icazəsi tələb olunur.'},
                status=status.HTTP_403_FORBIDDEN
            )

        user_skill = self.get_object()
        serializer = UserSkillApprovalSerializer(data={'action': 'approve'})

        if serializer.is_valid():
            user_skill.approve(request.user)
            return Response({
                'detail': 'Bacarıq təsdiqləndi.',
                'skill': UserSkillSerializer(user_skill).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Bacarığı rədd et (Manager və Admin üçün)."""
        from apps.accounts.rbac import RoleManager

        if not RoleManager.is_manager(request.user):
            return Response(
                {'detail': 'Bu əməliyyat üçün Manager icazəsi tələb olunur.'},
                status=status.HTTP_403_FORBIDDEN
            )

        user_skill = self.get_object()
        serializer = UserSkillApprovalSerializer(data={'action': 'reject'})

        if serializer.is_valid():
            user_skill.reject(request.user)
            return Response({
                'detail': 'Bacarıq rədd edildi.',
                'skill': UserSkillSerializer(user_skill).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def pending_approvals(self, request):
        """Təsdiq gözləyən bacarıqları qaytarır (Manager üçün)."""
        from apps.accounts.rbac import RoleManager

        if not RoleManager.is_manager(request.user):
            return Response(
                {'detail': 'Bu əməliyyat üçün Manager icazəsi tələb olunur.'},
                status=status.HTTP_403_FORBIDDEN
            )

        pending_skills = self.queryset.filter(approval_status='pending')
        serializer = self.get_serializer(pending_skills, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_skills(self, request):
        """Cari istifadəçinin bacarıqlarını qaytarır."""
        my_skills = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(my_skills, many=True)
        return Response(serializer.data)
