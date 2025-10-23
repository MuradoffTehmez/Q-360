"""
Compensation Module Serializers.
"""
from rest_framework import serializers
from .models import SalaryInformation, EmployeeBenefit, Bonus, CompensationHistory
from apps.accounts.models import User


class SalaryInformationSerializer(serializers.ModelSerializer):
    """Serializer for SalaryInformation model."""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = SalaryInformation
        fields = [
            'id', 'user', 'user_name', 'base_salary', 'currency', 'payment_frequency',
            'effective_date', 'end_date', 'bank_name', 'bank_account_number',
            'swift_code', 'notes', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class EmployeeBenefitSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeBenefit model."""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    benefit_type_display = serializers.CharField(source='get_benefit_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EmployeeBenefit
        fields = [
            'id', 'user', 'user_name', 'benefit_type', 'benefit_type_display',
            'provider', 'coverage_type', 'annual_value', 'employee_contribution',
            'currency', 'start_date', 'end_date', 'status', 'status_display',
            'policy_number', 'coverage_details', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class BonusSerializer(serializers.ModelSerializer):
    """Serializer for Bonus model."""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    bonus_type_display = serializers.CharField(source='get_bonus_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = Bonus
        fields = [
            'id', 'user', 'user_name', 'bonus_type', 'bonus_type_display',
            'amount', 'currency', 'status', 'status_display', 'payment_date',
            'fiscal_year', 'description', 'approved_by', 'approved_by_name',
            'approved_at', 'created_at'
        ]
        read_only_fields = ['created_at', 'approved_by', 'approved_at']


class CompensationHistorySerializer(serializers.ModelSerializer):
    """Serializer for CompensationHistory model."""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    change_reason_display = serializers.CharField(source='get_change_reason_display', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = CompensationHistory
        fields = [
            'id', 'user', 'user_name', 'previous_salary', 'new_salary',
            'currency', 'change_percentage', 'change_reason', 'change_reason_display',
            'effective_date', 'notes', 'approved_by', 'approved_by_name', 'created_at'
        ]
        read_only_fields = ['created_at', 'change_percentage']
