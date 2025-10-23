"""
Compensation Module API Views.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg, Count, Min, Max
from django.utils import timezone

from .models import SalaryInformation, EmployeeBenefit, Bonus, CompensationHistory
from .serializers import (
    SalaryInformationSerializer, EmployeeBenefitSerializer,
    BonusSerializer, CompensationHistorySerializer
)


class SalaryInformationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing salary information."""
    queryset = SalaryInformation.objects.select_related('user')
    serializer_class = SalaryInformationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'currency', 'is_active', 'payment_frequency']
    search_fields = ['user__first_name', 'user__last_name', 'notes']
    ordering_fields = ['base_salary', 'effective_date', 'created_at']
    ordering = ['-effective_date']

    def get_queryset(self):
        """Filter based on user permissions."""
        user = self.request.user
        queryset = super().get_queryset()

        # Admins see all
        if user.is_superadmin() or user.is_admin():
            return queryset

        # Managers see their department
        if user.is_manager():
            return queryset.filter(user__department=user.department)

        # Employees see only their own
        return queryset.filter(user=user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get salary statistics."""
        queryset = self.get_queryset().filter(is_active=True)

        stats = queryset.aggregate(
            total_employees=Count('id'),
            avg_salary=Avg('base_salary'),
            min_salary=Min('base_salary'),
            max_salary=Max('base_salary'),
            total_payroll=Sum('base_salary')
        )

        return Response(stats)

    @action(detail=True, methods=['post'])
    def update_salary(self, request, pk=None):
        """Update employee salary and create history record."""
        salary_info = self.get_object()
        new_salary = request.data.get('new_salary')
        reason = request.data.get('reason', 'other')

        if not new_salary:
            return Response(
                {'error': 'new_salary field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create history record
        CompensationHistory.objects.create(
            user=salary_info.user,
            previous_salary=salary_info.base_salary,
            new_salary=new_salary,
            currency=salary_info.currency,
            change_reason=reason,
            effective_date=timezone.now().date(),
            created_by=request.user
        )

        # Update salary
        salary_info.base_salary = new_salary
        salary_info.save()

        return Response(
            SalaryInformationSerializer(salary_info).data,
            status=status.HTTP_200_OK
        )


class EmployeeBenefitViewSet(viewsets.ModelViewSet):
    """ViewSet for managing employee benefits."""
    queryset = EmployeeBenefit.objects.select_related('user')
    serializer_class = EmployeeBenefitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'benefit_type', 'status']
    search_fields = ['user__first_name', 'user__last_name', 'provider']
    ordering_fields = ['annual_value', 'start_date', 'created_at']
    ordering = ['-start_date']

    def get_queryset(self):
        """Filter based on user permissions."""
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_superadmin() or user.is_admin():
            return queryset

        if user.is_manager():
            return queryset.filter(user__department=user.department)

        return queryset.filter(user=user)

    @action(detail=False, methods=['get'])
    def active_benefits(self, request):
        """Get all active benefits."""
        queryset = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get benefits grouped by type."""
        benefit_type = request.query_params.get('type')
        if not benefit_type:
            return Response(
                {'error': 'type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(benefit_type=benefit_type, status='active')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BonusViewSet(viewsets.ModelViewSet):
    """ViewSet for managing bonuses."""
    queryset = Bonus.objects.select_related('user', 'approved_by')
    serializer_class = BonusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'bonus_type', 'status']
    search_fields = ['user__first_name', 'user__last_name', 'description']
    ordering_fields = ['amount', 'payment_date', 'created_at']
    ordering = ['-payment_date']

    def get_queryset(self):
        """Filter based on user permissions."""
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_superadmin() or user.is_admin():
            return queryset

        if user.is_manager():
            return queryset.filter(user__department=user.department)

        return queryset.filter(user=user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a bonus."""
        bonus = self.get_object()

        if not (request.user.is_admin() or request.user.is_manager()):
            return Response(
                {'error': 'Only admins and managers can approve bonuses'},
                status=status.HTTP_403_FORBIDDEN
            )

        if bonus.status != 'pending':
            return Response(
                {'error': 'Only pending bonuses can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bonus.status = 'approved'
        bonus.approved_by = request.user
        bonus.approved_at = timezone.now()
        bonus.save()

        return Response(
            BonusSerializer(bonus).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a bonus."""
        bonus = self.get_object()

        if not (request.user.is_admin() or request.user.is_manager()):
            return Response(
                {'error': 'Only admins and managers can reject bonuses'},
                status=status.HTTP_403_FORBIDDEN
            )

        if bonus.status != 'pending':
            return Response(
                {'error': 'Only pending bonuses can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bonus.status = 'rejected'
        bonus.save()

        return Response(
            BonusSerializer(bonus).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending bonuses."""
        queryset = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CompensationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing compensation history (read-only)."""
    queryset = CompensationHistory.objects.select_related('user', 'approved_by')
    serializer_class = CompensationHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user']
    ordering_fields = ['effective_date', 'created_at']
    ordering = ['-effective_date']

    def get_queryset(self):
        """Filter based on user permissions."""
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_superadmin() or user.is_admin():
            return queryset

        if user.is_manager():
            return queryset.filter(user__department=user.department)

        return queryset.filter(user=user)
