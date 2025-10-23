from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import template_views

router = DefaultRouter()

app_name = 'reports'

urlpatterns = [
    # Report views
    path('my-reports/', template_views.my_reports, name='my-reports'),
    path('team-reports/', template_views.team_reports, name='team-reports'),
    path('detailed/<int:result_pk>/', template_views.detailed_report, name='detailed-report'),
    path('comparison/', template_views.comparison_report, name='comparison_report'),
    path('analytics/', template_views.analytics_dashboard, name='analytics-dashboard'),
    path('blueprints/', template_views.blueprint_list, name='blueprint-list'),
    path('blueprints/<slug:slug>/', template_views.blueprint_detail, name='blueprint-detail'),
    path('schedules/', template_views.schedule_center, name='schedule-center'),
    path('custom-builder/', template_views.custom_report_builder, name='custom-builder'),

    # Export
    path('export/pdf/<int:result_pk>/', template_views.export_pdf, name='export-pdf'),
    path('export/excel/<int:campaign_pk>/', template_views.export_excel, name='export-excel'),
    path('export/custom/', template_views.export_custom_report, name='export-custom'),

    # API
    path('api/', include(router.urls)),
]
