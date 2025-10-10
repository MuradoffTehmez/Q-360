"""
Views for training app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Q
from django.utils import timezone

from .models import TrainingResource, UserTraining
from .serializers import (
    TrainingResourceSerializer,
    TrainingResourceDetailSerializer,
    UserTrainingSerializer,
    UserTrainingDetailSerializer,
    UserTrainingStatusUpdateSerializer,
    UserTrainingProgressUpdateSerializer,
    UserTrainingFeedbackSerializer,
    TrainingRecommendationSerializer,
)


class TrainingResourceViewSet(viewsets.ModelViewSet):
    """ViewSet for TrainingResource model."""

    queryset = TrainingResource.objects.prefetch_related('required_competencies')
    serializer_class = TrainingResourceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['type', 'is_active', 'is_online', 'difficulty_level', 'is_mandatory']
    search_fields = ['title', 'description', 'provider']
    ordering_fields = ['title', 'created_at', 'cost', 'duration_hours']
    ordering = ['title']

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action."""
        if self.action == 'retrieve':
            return TrainingResourceDetailSerializer
        return TrainingResourceSerializer

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

    @action(detail=True, methods=['get'])
    def assigned_users(self, request, pk=None):
        """Təlimə təyin olunmuş istifadəçiləri qaytarır."""
        resource = self.get_object()
        user_trainings = resource.user_trainings.select_related(
            'user', 'assigned_by'
        ).filter(user__is_active=True)

        serializer = UserTrainingSerializer(user_trainings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_to_users(self, request, pk=None):
        """Təlimi seçilmiş istifadəçilərə təyin edir (Manager üçün)."""
        from apps.accounts.rbac import RoleManager
        from apps.accounts.models import User

        if not RoleManager.is_manager(request.user):
            return Response(
                {'detail': 'Bu əməliyyat üçün Manager icazəsi tələb olunur.'},
                status=status.HTTP_403_FORBIDDEN
            )

        resource = self.get_object()
        user_ids = request.data.get('user_ids', [])
        due_date = request.data.get('due_date')
        assignment_type = request.data.get('assignment_type', 'manager_assigned')

        if not user_ids:
            return Response(
                {'detail': 'İstifadəçi ID-ləri tələb olunur.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        assigned_trainings = []

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)

                # Check if already assigned
                if UserTraining.objects.filter(user=user, resource=resource).exists():
                    continue

                training = UserTraining.objects.create(
                    user=user,
                    resource=resource,
                    assigned_by=request.user,
                    assignment_type=assignment_type,
                    due_date=due_date,
                    start_date=timezone.now().date(),
                    status='pending'
                )

                assigned_trainings.append(UserTrainingSerializer(training).data)

            except User.DoesNotExist:
                continue

        return Response({
            'detail': f'{len(assigned_trainings)} istifadəçiyə təlim təyin edildi.',
            'assigned_trainings': assigned_trainings
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Təlim statistikalarını qaytarır."""
        total_resources = TrainingResource.objects.filter(is_active=True).count()
        total_assignments = UserTraining.objects.count()
        completed_count = UserTraining.objects.filter(status='completed').count()
        avg_completion_rate = TrainingResource.objects.aggregate(
            avg_rate=Avg('user_trainings__progress_percentage')
        )['avg_rate'] or 0

        most_popular = TrainingResource.objects.annotate(
            assignment_count=Count('user_trainings')
        ).order_by('-assignment_count')[:10]

        return Response({
            'total_resources': total_resources,
            'total_assignments': total_assignments,
            'completed_assignments': completed_count,
            'average_completion_rate': round(avg_completion_rate, 2),
            'most_popular_trainings': TrainingResourceSerializer(most_popular, many=True).data
        })


class UserTrainingViewSet(viewsets.ModelViewSet):
    """ViewSet for UserTraining model."""

    queryset = UserTraining.objects.select_related(
        'user',
        'resource',
        'assigned_by',
        'related_goal'
    )
    serializer_class = UserTrainingSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user', 'resource', 'status', 'assignment_type']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action."""
        if self.action == 'retrieve':
            return UserTrainingDetailSerializer
        return UserTrainingSerializer

    def get_queryset(self):
        """
        İstifadəçilər yalnız öz təlimlərini görə bilər.
        Manager və admin rolları bütün təlimləri görə bilər.
        """
        from apps.accounts.rbac import RoleManager
        user = self.request.user

        if RoleManager.is_manager(user):
            return self.queryset.all()

        # Regular users can only see their own trainings
        return self.queryset.filter(user=user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Təlim statusunu yenilə."""
        training = self.get_object()

        # Users can only update their own trainings
        if training.user != request.user:
            from apps.accounts.rbac import RoleManager
            if not RoleManager.is_manager(request.user):
                return Response(
                    {'detail': 'Bu təlimi yeniləmək icazəniz yoxdur.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = UserTrainingStatusUpdateSerializer(data=request.data)

        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            completion_note = serializer.validated_data.get('completion_note', '')
            progress = serializer.validated_data.get('progress_percentage')

            training.status = new_status

            if new_status == 'completed':
                training.mark_completed(completion_note)
            elif progress is not None:
                training.update_progress(progress)
            else:
                training.save()

            return Response({
                'detail': 'Status yeniləndi.',
                'training': UserTrainingSerializer(training).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Təlim proqresini yenilə."""
        training = self.get_object()

        # Users can only update their own trainings
        if training.user != request.user:
            return Response(
                {'detail': 'Bu təlimi yeniləmək icazəniz yoxdur.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserTrainingProgressUpdateSerializer(data=request.data)

        if serializer.is_valid():
            progress = serializer.validated_data['progress_percentage']
            training.update_progress(progress)

            return Response({
                'detail': 'Proqres yeniləndi.',
                'training': UserTrainingSerializer(training).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def submit_feedback(self, request, pk=None):
        """Təlim üçün rəy və reytinq göndər."""
        training = self.get_object()

        # Users can only submit feedback for their own trainings
        if training.user != request.user:
            return Response(
                {'detail': 'Bu təlim üçün rəy göndərmək icazəniz yoxdur.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Can only submit feedback for completed trainings
        if training.status != 'completed':
            return Response(
                {'detail': 'Yalnız tamamlanmış təlimlər üçün rəy göndərilə bilər.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserTrainingFeedbackSerializer(data=request.data)

        if serializer.is_valid():
            training.user_feedback = serializer.validated_data['user_feedback']
            training.rating = serializer.validated_data.get('rating')
            training.save()

            return Response({
                'detail': 'Rəy göndərildi.',
                'training': UserTrainingSerializer(training).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_trainings(self, request):
        """Cari istifadəçinin təlimlərini qaytarır."""
        my_trainings = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(my_trainings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_pending(self, request):
        """Cari istifadəçinin pending təlimlərini qaytarır."""
        pending_trainings = self.queryset.filter(
            user=request.user,
            status='pending'
        )
        serializer = self.get_serializer(pending_trainings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_in_progress(self, request):
        """Cari istifadəçinin davam edən təlimlərini qaytarır."""
        in_progress_trainings = self.queryset.filter(
            user=request.user,
            status='in_progress'
        )
        serializer = self.get_serializer(in_progress_trainings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_completed(self, request):
        """Cari istifadəçinin tamamlanmış təlimlərini qaytarır."""
        completed_trainings = self.queryset.filter(
            user=request.user,
            status='completed'
        )
        serializer = self.get_serializer(completed_trainings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Vaxtı keçmiş təlimləri qaytarır (Manager üçün)."""
        from apps.accounts.rbac import RoleManager

        if not RoleManager.is_manager(request.user):
            return Response(
                {'detail': 'Bu əməliyyat üçün Manager icazəsi tələb olunur.'},
                status=status.HTTP_403_FORBIDDEN
            )

        overdue_trainings = self.queryset.filter(
            due_date__lt=timezone.now().date(),
            status__in=['pending', 'in_progress']
        )

        serializer = self.get_serializer(overdue_trainings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def get_recommendations(self, request):
        """İstifadəçi üçün təlim tövsiyələri."""
        from apps.training.tasks import recommend_trainings_for_user

        serializer = TrainingRecommendationSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            competency_ids = serializer.validated_data.get('competency_ids')
            limit = serializer.validated_data.get('limit', 5)

            # Trigger recommendation task
            result = recommend_trainings_for_user.delay(
                user_id=user_id,
                competency_ids=competency_ids,
                limit=limit
            )

            # Wait for result (or you can return task ID for async polling)
            recommendations = result.get(timeout=10)

            return Response(recommendations)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
