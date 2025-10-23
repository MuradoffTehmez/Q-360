"""
Leave & Attendance Module Serializers.
"""
from rest_framework import serializers
from .models import LeaveRequest, Attendance, LeaveBalance, LeaveType, Holiday
from apps.accounts.models import User


class LeaveTypeSerializer(serializers.ModelSerializer):
    """Serializer for LeaveType model."""

    class Meta:
        model = LeaveType
        fields = [
            'id', 'name', 'code', 'max_days_per_year', 'requires_approval',
            'is_paid', 'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LeaveRequestSerializer(serializers.ModelSerializer):
    """Serializer for LeaveRequest model."""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name', 'leave_type', 'leave_type_name',
            'start_date', 'end_date', 'total_days', 'reason', 'status',
            'status_display', 'approved_by', 'approved_by_name', 'approval_date',
            'rejection_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'approved_by', 'approval_date']

    def validate(self, data):
        """Validate leave request dates."""
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date.'
            })
        return data


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model."""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    work_hours = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'date', 'check_in_time',
            'check_out_time', 'work_hours', 'status', 'status_display',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'work_hours']


class LeaveBalanceSerializer(serializers.ModelSerializer):
    """Serializer for LeaveBalance model."""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    remaining_days = serializers.DecimalField(max_digits=5, decimal_places=1, read_only=True)

    class Meta:
        model = LeaveBalance
        fields = [
            'id', 'employee', 'employee_name', 'leave_type', 'leave_type_name',
            'year', 'total_days', 'used_days', 'remaining_days',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'remaining_days']


class HolidaySerializer(serializers.ModelSerializer):
    """Serializer for Holiday model."""

    class Meta:
        model = Holiday
        fields = [
            'id', 'name', 'date', 'is_recurring', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
