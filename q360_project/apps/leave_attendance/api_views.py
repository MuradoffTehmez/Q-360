"""
Leave & Attendance Module API Views.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import LeaveRequest, Attendance, LeaveBalance, LeaveType, Holiday
from .serializers import (
    LeaveRequestSerializer, AttendanceSerializer,
    LeaveBalanceSerializer, LeaveTypeSerializer, HolidaySerializer
)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for managing leave requests."""
    queryset = LeaveRequest.objects.select_related('employee', 'leave_type', 'approved_by')
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'leave_type', 'status']
    search_fields = ['employee__first_name', 'employee__last_name', 'reason']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter based on user permissions."""
        user = self.request.user
        queryset = super().get_queryset()

        # Admins see all
        if user.is_superadmin() or user.is_admin():
            return queryset

        # Managers see their department + their own
        if user.is_manager():
            return queryset.filter(
                Q(employee__department=user.department) | Q(employee=user)
            )

        # Employees see only their own
        return queryset.filter(employee=user)

    def perform_create(self, serializer):
        """Set employee to current user when creating."""
        serializer.save(employee=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a leave request."""
        leave_request = self.get_object()

        if not (request.user.is_admin() or request.user.is_manager()):
            return Response(
                {'error': 'Only admins and managers can approve leave requests'},
                status=status.HTTP_403_FORBIDDEN
            )

        if leave_request.status != 'pending':
            return Response(
                {'error': 'Only pending leave requests can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check leave balance
        balance = LeaveBalance.objects.filter(
            employee=leave_request.employee,
            leave_type=leave_request.leave_type,
            year=leave_request.start_date.year
        ).first()

        if balance and balance.remaining_days < leave_request.total_days:
            return Response(
                {'error': f'Insufficient leave balance. Available: {balance.remaining_days} days'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Approve the request
        leave_request.status = 'approved'
        leave_request.approved_by = request.user
        leave_request.approval_date = timezone.now()
        leave_request.save()

        # Update leave balance
        if balance:
            balance.used_days += leave_request.total_days
            balance.save()

        return Response(
            LeaveRequestSerializer(leave_request).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a leave request."""
        leave_request = self.get_object()

        if not (request.user.is_admin() or request.user.is_manager()):
            return Response(
                {'error': 'Only admins and managers can reject leave requests'},
                status=status.HTTP_403_FORBIDDEN
            )

        if leave_request.status != 'pending':
            return Response(
                {'error': 'Only pending leave requests can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rejection_reason = request.data.get('rejection_reason', '')
        leave_request.status = 'rejected'
        leave_request.rejection_reason = rejection_reason
        leave_request.save()

        return Response(
            LeaveRequestSerializer(leave_request).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending leave requests."""
        queryset = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_requests(self, request):
        """Get current user's leave requests."""
        queryset = LeaveRequest.objects.filter(employee=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing attendance records."""
    queryset = Attendance.objects.select_related('employee')
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'date', 'status']
    search_fields = ['employee__first_name', 'employee__last_name']
    ordering_fields = ['date', 'check_in_time', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        """Filter based on user permissions."""
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_superadmin() or user.is_admin():
            return queryset

        if user.is_manager():
            return queryset.filter(
                Q(employee__department=user.department) | Q(employee=user)
            )

        return queryset.filter(employee=user)

    @action(detail=False, methods=['post'])
    def check_in(self, request):
        """Check in for today."""
        today = timezone.now().date()
        employee = request.user

        # Check if already checked in today
        existing = Attendance.objects.filter(employee=employee, date=today).first()
        if existing:
            return Response(
                {'error': 'Already checked in today'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create attendance record
        attendance = Attendance.objects.create(
            employee=employee,
            date=today,
            check_in_time=timezone.now().time(),
            status='present'
        )

        return Response(
            AttendanceSerializer(attendance).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'])
    def check_out(self, request):
        """Check out for today."""
        today = timezone.now().date()
        employee = request.user

        # Get today's attendance
        attendance = Attendance.objects.filter(employee=employee, date=today).first()
        if not attendance:
            return Response(
                {'error': 'No check-in record found for today'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if attendance.check_out_time:
            return Response(
                {'error': 'Already checked out today'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update attendance with check-out time
        attendance.check_out_time = timezone.now().time()
        attendance.save()

        return Response(
            AttendanceSerializer(attendance).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def my_attendance(self, request):
        """Get current user's attendance records."""
        queryset = Attendance.objects.filter(employee=request.user)

        # Optional date range filter
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get attendance statistics."""
        queryset = self.get_queryset()

        # Optional filters
        employee_id = request.query_params.get('employee')
        month = request.query_params.get('month')  # Format: YYYY-MM

        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        if month:
            year, month_num = month.split('-')
            queryset = queryset.filter(date__year=year, date__month=month_num)

        stats = queryset.aggregate(
            total_days=Count('id'),
            present_days=Count('id', filter=Q(status='present')),
            absent_days=Count('id', filter=Q(status='absent')),
            late_days=Count('id', filter=Q(status='late')),
            half_day_count=Count('id', filter=Q(status='half_day'))
        )

        return Response(stats)


class LeaveBalanceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing leave balances."""
    queryset = LeaveBalance.objects.select_related('employee', 'leave_type')
    serializer_class = LeaveBalanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'leave_type', 'year']
    ordering_fields = ['year', 'total_days', 'used_days']
    ordering = ['-year']

    def get_queryset(self):
        """Filter based on user permissions."""
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_superadmin() or user.is_admin():
            return queryset

        if user.is_manager():
            return queryset.filter(
                Q(employee__department=user.department) | Q(employee=user)
            )

        return queryset.filter(employee=user)

    @action(detail=False, methods=['get'])
    def my_balance(self, request):
        """Get current user's leave balance."""
        current_year = timezone.now().year
        queryset = LeaveBalance.objects.filter(
            employee=request.user,
            year=current_year
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LeaveTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing leave types."""
    queryset = LeaveType.objects.filter(is_active=True)
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'max_days_per_year']
    ordering = ['name']

    def get_queryset(self):
        """Only admins can see inactive leave types."""
        queryset = super().get_queryset()
        if self.request.user.is_admin():
            return LeaveType.objects.all()
        return queryset


class HolidayViewSet(viewsets.ModelViewSet):
    """ViewSet for managing holidays."""
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_recurring']
    ordering_fields = ['date']
    ordering = ['date']

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming holidays."""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(date__gte=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
