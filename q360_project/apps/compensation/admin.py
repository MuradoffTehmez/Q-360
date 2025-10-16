"""Admin configuration for compensation app."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    SalaryInformation,
    CompensationHistory,
    Bonus,
    Allowance,
    Deduction,
    DepartmentBudget
)


@admin.register(SalaryInformation)
class SalaryInformationAdmin(SimpleHistoryAdmin):
    """Admin for Salary Information."""

    list_display = [
        'user', 'base_salary', 'currency', 'payment_frequency',
        'effective_date', 'is_active'
    ]
    list_filter = ['currency', 'payment_frequency', 'is_active', 'effective_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    date_hierarchy = 'effective_date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('İstifadəçi Məlumatları', {
            'fields': ('user',)
        }),
        ('Maaş Məlumatları', {
            'fields': ('base_salary', 'currency', 'payment_frequency', 'effective_date', 'end_date')
        }),
        ('Bank Məlumatları', {
            'fields': ('bank_name', 'bank_account_number', 'swift_code')
        }),
        ('Əlavə Məlumat', {
            'fields': ('notes', 'is_active', 'updated_by')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CompensationHistory)
class CompensationHistoryAdmin(SimpleHistoryAdmin):
    """Admin for Compensation History."""

    list_display = [
        'user', 'previous_salary', 'new_salary', 'currency',
        'change_percentage', 'change_reason', 'effective_date'
    ]
    list_filter = ['change_reason', 'currency', 'effective_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    date_hierarchy = 'effective_date'
    readonly_fields = ['created_at', 'change_percentage']

    fieldsets = (
        ('İstifadəçi Məlumatları', {
            'fields': ('user',)
        }),
        ('Maaş Dəyişikliyi', {
            'fields': ('previous_salary', 'new_salary', 'currency', 'change_percentage', 'change_reason')
        }),
        ('Tarix və Təsdiq', {
            'fields': ('effective_date', 'approved_by')
        }),
        ('Əlavə Məlumat', {
            'fields': ('notes', 'created_by', 'created_at')
        }),
    )


@admin.register(Bonus)
class BonusAdmin(SimpleHistoryAdmin):
    """Admin for Bonuses."""

    list_display = [
        'user', 'bonus_type', 'amount', 'currency',
        'fiscal_year', 'status', 'payment_date'
    ]
    list_filter = ['bonus_type', 'status', 'fiscal_year', 'currency']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'description']
    date_hierarchy = 'payment_date'
    readonly_fields = ['created_at', 'approved_at']

    fieldsets = (
        ('İstifadəçi Məlumatları', {
            'fields': ('user',)
        }),
        ('Bonus Məlumatları', {
            'fields': ('bonus_type', 'amount', 'currency', 'fiscal_year', 'description')
        }),
        ('Status və Ödəniş', {
            'fields': ('status', 'payment_date')
        }),
        ('Təsdiq', {
            'fields': ('approved_by', 'approved_at')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Allowance)
class AllowanceAdmin(SimpleHistoryAdmin):
    """Admin for Allowances."""

    list_display = [
        'user', 'allowance_type', 'amount', 'currency',
        'payment_frequency', 'start_date', 'is_active'
    ]
    list_filter = ['allowance_type', 'payment_frequency', 'is_active', 'is_taxable']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'description']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('İstifadəçi Məlumatları', {
            'fields': ('user',)
        }),
        ('Müavinət Məlumatları', {
            'fields': ('allowance_type', 'amount', 'currency', 'payment_frequency')
        }),
        ('Tarix Məlumatları', {
            'fields': ('start_date', 'end_date')
        }),
        ('Əlavə Parametrlər', {
            'fields': ('is_taxable', 'is_active', 'description')
        }),
        ('Təsdiq və Sistem', {
            'fields': ('approved_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Deduction)
class DeductionAdmin(SimpleHistoryAdmin):
    """Admin for Deductions."""

    list_display = [
        'user', 'deduction_type', 'calculation_method', 'amount',
        'currency', 'start_date', 'is_active'
    ]
    list_filter = ['deduction_type', 'calculation_method', 'is_active']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'description']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('İstifadəçi Məlumatları', {
            'fields': ('user',)
        }),
        ('Tutma Məlumatları', {
            'fields': ('deduction_type', 'calculation_method', 'amount', 'currency')
        }),
        ('Tarix Məlumatları', {
            'fields': ('start_date', 'end_date')
        }),
        ('Əlavə Məlumat', {
            'fields': ('description', 'is_active')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DepartmentBudget)
class DepartmentBudgetAdmin(SimpleHistoryAdmin):
    """Admin for Department Budget."""

    list_display = [
        'department', 'fiscal_year', 'annual_budget', 'utilized_amount',
        'utilization_percentage_display', 'remaining_budget_display', 'is_active'
    ]
    list_filter = ['fiscal_year', 'is_active', 'currency']
    search_fields = ['department__name', 'notes']
    readonly_fields = ['created_at', 'updated_at', 'utilization_percentage_display', 'remaining_budget_display']

    fieldsets = (
        ('Departament Məlumatları', {
            'fields': ('department', 'fiscal_year')
        }),
        ('Büdcə Məlumatları', {
            'fields': ('annual_budget', 'utilized_amount', 'currency', 'remaining_budget_display', 'utilization_percentage_display')
        }),
        ('Status', {
            'fields': ('is_active', 'notes')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def utilization_percentage_display(self, obj):
        """Display utilization percentage."""
        percentage = obj.utilization_percentage
        color = 'green' if percentage < 80 else 'orange' if percentage < 100 else 'red'
        return f'<span style="color: {color}; font-weight: bold;">{percentage:.2f}%</span>'
    utilization_percentage_display.short_description = 'İstifadə Faizi'
    utilization_percentage_display.allow_tags = True

    def remaining_budget_display(self, obj):
        """Display remaining budget."""
        remaining = obj.remaining_budget
        color = 'green' if remaining > 0 else 'red'
        return f'<span style="color: {color}; font-weight: bold;">{remaining} {obj.currency}</span>'
    remaining_budget_display.short_description = 'Qalıq Büdcə'
    remaining_budget_display.allow_tags = True
