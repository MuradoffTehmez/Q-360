"""Admin configuration for leave and attendance app."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    LeaveType,
    LeaveBalance,
    LeaveRequest,
    Attendance,
    Holiday
)


@admin.register(LeaveType)
class LeaveTypeAdmin(SimpleHistoryAdmin):
    """Admin for Leave Types."""

    list_display = [
        'name', 'code', 'days_per_year', 'is_paid',
        'requires_approval', 'carry_forward', 'is_active'
    ]
    list_filter = ['is_paid', 'requires_approval', 'requires_document', 'carry_forward', 'is_active']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Əsas Məlumat', {
            'fields': ('name', 'code', 'description', 'color_code')
        }),
        ('Məzuniyyət Şərtləri', {
            'fields': ('days_per_year', 'max_consecutive_days', 'notice_days')
        }),
        ('Parametrlər', {
            'fields': ('is_paid', 'requires_approval', 'requires_document')
        }),
        ('Keçid Parametrləri', {
            'fields': ('carry_forward', 'max_carry_forward_days')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(SimpleHistoryAdmin):
    """Admin for Leave Balances."""

    list_display = [
        'user', 'leave_type', 'year', 'entitled_days',
        'used_days', 'pending_days', 'available_days'
    ]
    list_filter = ['year', 'leave_type']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at', 'available_days']

    fieldsets = (
        ('İstifadəçi Məlumatları', {
            'fields': ('user', 'leave_type', 'year')
        }),
        ('Balans Məlumatları', {
            'fields': ('entitled_days', 'used_days', 'pending_days', 'carried_forward_days', 'available_days')
        }),
        ('Əlavə Məlumat', {
            'fields': ('notes',)
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def available_days(self, obj):
        """Display available days."""
        return obj.available_days
    available_days.short_description = 'Qalan Gün Sayı'


@admin.register(LeaveRequest)
class LeaveRequestAdmin(SimpleHistoryAdmin):
    """Admin for Leave Requests."""

    list_display = [
        'user', 'leave_type', 'start_date', 'end_date',
        'number_of_days', 'status', 'emergency'
    ]
    list_filter = ['status', 'leave_type', 'emergency', 'start_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'reason']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at', 'approved_at']

    fieldsets = (
        ('İstifadəçi Məlumatları', {
            'fields': ('user', 'leave_type')
        }),
        ('Məzuniyyət Məlumatları', {
            'fields': ('start_date', 'end_date', 'number_of_days', 'reason')
        }),
        ('Əlavə Parametrlər', {
            'fields': ('is_half_day_start', 'is_half_day_end', 'emergency', 'attachment')
        }),
        ('Status və Təsdiq', {
            'fields': ('status', 'approved_by', 'approved_at', 'rejection_reason')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        """Approve selected leave requests."""
        for leave_request in queryset.filter(status='pending'):
            leave_request.approve(request.user)
        self.message_user(request, f"{queryset.count()} məzuniyyət sorğusu təsdiqləndi.")
    approve_requests.short_description = "Seçilmiş sorğuları təsdiqlə"

    def reject_requests(self, request, queryset):
        """Reject selected leave requests."""
        for leave_request in queryset.filter(status='pending'):
            leave_request.reject(request.user, "Admin tərəfindən rədd edildi")
        self.message_user(request, f"{queryset.count()} məzuniyyət sorğusu rədd edildi.")
    reject_requests.short_description = "Seçilmiş sorğuları rədd et"


@admin.register(Attendance)
class AttendanceAdmin(SimpleHistoryAdmin):
    """Admin for Attendance."""

    list_display = [
        'user', 'date', 'status', 'check_in', 'check_out',
        'work_hours', 'late_minutes'
    ]
    list_filter = ['status', 'date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'verified_at', 'work_hours']

    fieldsets = (
        ('İstifadəçi Məlumatları', {
            'fields': ('user', 'date', 'status')
        }),
        ('Vaxt Məlumatları', {
            'fields': ('check_in', 'check_out', 'work_hours')
        }),
        ('Gecikmə və Erkən Çıxış', {
            'fields': ('late_minutes', 'early_leave_minutes')
        }),
        ('Əlavə Məlumat', {
            'fields': ('notes', 'leave_request')
        }),
        ('Təsdiq', {
            'fields': ('verified_by', 'verified_at')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Holiday)
class HolidayAdmin(SimpleHistoryAdmin):
    """Admin for Holidays."""

    list_display = ['name', 'date', 'holiday_type', 'is_recurring', 'is_active']
    list_filter = ['holiday_type', 'is_recurring', 'is_active', 'date']
    search_fields = ['name', 'description']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Bayram Məlumatları', {
            'fields': ('name', 'date', 'holiday_type', 'description')
        }),
        ('Parametrlər', {
            'fields': ('is_recurring', 'is_active')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
