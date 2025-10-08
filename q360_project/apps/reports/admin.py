from django.contrib import admin
from .models import Report, RadarChartData


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'campaign', 'generated_for', 'created_at']
    list_filter = ['report_type', 'campaign', 'created_at']
    search_fields = ['title', 'generated_for__username']


@admin.register(RadarChartData)
class RadarChartDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'campaign', 'category', 'self_score', 'others_score']
    list_filter = ['campaign', 'category']
    search_fields = ['user__username']
