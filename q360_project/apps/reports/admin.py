from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.utils.html import format_html
from django.db.models import Count, Avg
from .models import Report, RadarChartData, ReportGenerationLog, SystemKPI
from apps.accounts.models import User


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'campaign', 'generated_for', 'created_at']
    list_filter = ['report_type', 'campaign', 'created_at']
    search_fields = ['title', 'generated_for__username']
    readonly_fields = ['created_at']

    def get_urls(self):
        """Add custom admin URLs."""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('users-report/', self.admin_site.admin_view(self.users_report_view), name='reports_report_users'),
        ]
        return custom_urls + urls

    def users_report_view(self, request):
        """Custom view for user statistics report."""
        from apps.evaluations.models import EvaluationResult

        users = User.objects.filter(is_active=True).select_related('department')

        user_stats = []
        for user in users:
            results = EvaluationResult.objects.filter(evaluatee=user)
            avg_score = results.aggregate(avg=Avg('overall_score'))['avg']

            user_stats.append({
                'user': user,
                'department': user.department,
                'position': user.position,
                'avg_score': avg_score or 0,
                'evaluations_count': results.count(),
            })

        context = {
            **self.admin_site.each_context(request),
            'title': 'İstifadəçi Hesabatları',
            'user_stats': user_stats,
        }

        return render(request, 'admin/reports/users_report.html', context)


@admin.register(RadarChartData)
class RadarChartDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'campaign', 'category', 'self_score', 'others_score']
    list_filter = ['campaign', 'category']
    search_fields = ['user__username']


@admin.register(ReportGenerationLog)
class ReportGenerationLogAdmin(admin.ModelAdmin):
    """Admin for report generation logs."""

    list_display = ['report_type', 'requested_by', 'status_badge', 'created_at', 'download_link']
    list_filter = ['status', 'report_type', 'created_at']
    search_fields = ['requested_by__username']
    readonly_fields = ['created_at', 'completed_at', 'metadata']

    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('report_type', 'requested_by', 'status')
        }),
        ('Fayl', {
            'fields': ('file',)
        }),
        ('Xəta', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata', 'created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        """Display colored status badge."""
        colors = {
            'pending': '#ffc107',
            'processing': '#17a2b8',
            'completed': '#28a745',
            'failed': '#dc3545'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def download_link(self, obj):
        """Display download link for completed reports."""
        if obj.status == 'completed' and obj.file:
            return format_html(
                '<a class="button" href="{}" download>Yüklə</a>',
                obj.file.url
            )
        return '-'
    download_link.short_description = 'Yüklə'


@admin.register(SystemKPI)
class SystemKPIAdmin(admin.ModelAdmin):
    """Admin for system KPI tracking."""

    list_display = [
        'date',
        'total_users',
        'active_users',
        'completion_rate_badge',
        'active_campaigns',
        'login_attempts_today',
        'failed_login_attempts_today'
    ]
    list_filter = ['date']
    readonly_fields = [
        'date', 'total_users', 'active_users', 'new_users_today',
        'users_logged_in_today', 'total_campaigns', 'active_campaigns',
        'total_evaluations', 'completed_evaluations', 'evaluations_completed_today',
        'completion_rate', 'total_departments', 'total_trainings',
        'active_trainings', 'login_attempts_today', 'failed_login_attempts_today',
        'security_threats_detected', 'average_response_time', 'database_size_mb',
        'created_at', 'updated_at'
    ]
    ordering = ['-date']

    fieldsets = (
        ('Tarix', {
            'fields': ('date',)
        }),
        ('İstifadəçi Metrikaları', {
            'fields': (
                'total_users', 'active_users', 'new_users_today',
                'users_logged_in_today'
            )
        }),
        ('Qiymətləndirmə Metrikaları', {
            'fields': (
                'total_campaigns', 'active_campaigns', 'total_evaluations',
                'completed_evaluations', 'evaluations_completed_today',
                'completion_rate'
            )
        }),
        ('Təlim və Şöbə', {
            'fields': ('total_departments', 'total_trainings', 'active_trainings')
        }),
        ('Təhlükəsizlik', {
            'fields': (
                'login_attempts_today', 'failed_login_attempts_today',
                'security_threats_detected'
            )
        }),
        ('Sistem Sağlamlığı', {
            'fields': ('average_response_time', 'database_size_mb')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def completion_rate_badge(self, obj):
        """Display colored completion rate badge."""
        rate = float(obj.completion_rate)
        if rate >= 80:
            color = '#28a745'  # Green
        elif rate >= 60:
            color = '#ffc107'  # Yellow
        else:
            color = '#dc3545'  # Red

        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}%</span>',
            color,
            rate
        )
    completion_rate_badge.short_description = 'Tamamlanma Faizi'

    def has_add_permission(self, request):
        """Disable manual adding - KPIs should be auto-calculated."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of KPI records."""
        return request.user.is_superuser
