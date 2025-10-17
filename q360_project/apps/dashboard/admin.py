from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import SystemKPI, DashboardWidget, AnalyticsReport, TrendData, ForecastData, RealTimeStat


@admin.register(SystemKPI)
class SystemKPIAdmin(admin.ModelAdmin):
    list_display = ['name', 'kpi_type', 'value', 'unit', 'period_start', 'period_end', 'created_at']
    list_filter = ['kpi_type', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'widget_type', 'title', 'is_active', 'order', 'created_at']
    list_filter = ['widget_type', 'is_active', 'created_at']
    search_fields = ['name', 'title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'generated_by', 'is_published', 'start_date', 'end_date', 'created_at']
    list_filter = ['report_type', 'is_published', 'created_at']
    search_fields = ['name', 'generated_by__username']
    readonly_fields = ['created_at', 'file_path']

    def view_report(self, obj):
        if obj.file_path:
            url = reverse('dashboard:view_report', args=[obj.pk])
            return format_html('<a href="{}" target="_blank">View Report</a>', url)
        return "No report file"
    view_report.short_description = 'Report'


@admin.register(TrendData)
class TrendDataAdmin(admin.ModelAdmin):
    list_display = ['data_type', 'period', 'value', 'department', 'organization', 'created_at']
    list_filter = ['data_type', 'department', 'organization', 'created_at']
    search_fields = ['data_type', 'department__name', 'organization__name']
    date_hierarchy = 'period'


@admin.register(ForecastData)
class ForecastDataAdmin(admin.ModelAdmin):
    list_display = ['forecast_type', 'forecast_date', 'predicted_value', 'confidence_level', 'department', 'organization', 'created_at']
    list_filter = ['forecast_type', 'department', 'organization', 'created_at']
    search_fields = ['forecast_type', 'department__name', 'organization__name']
    date_hierarchy = 'forecast_date'


@admin.register(RealTimeStat)
class RealTimeStatAdmin(admin.ModelAdmin):
    list_display = ['stat_type', 'current_value', 'unit', 'organization', 'last_updated']
    list_filter = ['stat_type', 'organization', 'last_updated']
    search_fields = ['stat_type', 'organization__name']