from django.urls import path
from . import views
from . import api_views
from . import export_views
from . import api

app_name = 'dashboard'

urlpatterns = [
    # Dashboard səhifələri
    path('', views.dashboard_home, name='dashboard_home'),
    path('kpi/', views.kpi_dashboard, name='kpi_dashboard'),
    path('trend/', views.trend_analysis, name='trend_analysis'),
    path('forecast/', views.forecasting_dashboard, name='forecasting_dashboard'),

    # Real-time API endpoints
    path('api/stats/', api.dashboard_stats, name='api_stats'),
    path('api/trends/', api.dashboard_trends, name='api_trends'),
    path('api/forecasting/', api.dashboard_forecasting, name='api_forecasting'),

    # Export endpointləri
    path('export/analytics/excel/', export_views.export_analytics_excel, name='export_analytics_excel'),
    path('export/analytics/pdf/', export_views.export_analytics_pdf, name='export_analytics_pdf'),

    # Əsas API endpointlər
    path('api/realtime-stats/', views.real_time_stats_api, name='realtime_stats_api'),
    path('api/update-stats/', views.update_real_time_stats, name='update_realtime_stats'),
    path('api/trend/<str:data_type>/', views.get_trend_data, name='get_trend_data'),
    path('api/forecast/<str:forecast_type>/', views.get_forecast_data, name='get_forecast_data'),
    path('api/generate-report/', views.generate_analytics_report, name='generate_report'),

    # Yeni genişləndirilmiş API endpointlər
    path('api/data/<str:endpoint>/', api_views.dashboard_api_endpoint, name='dashboard_api'),
    path('api/widget-config/', api_views.dashboard_widget_config, name='widget_config'),
    path('api/department-analytics/', api_views.department_analytics, name='department_analytics'),

    # AI model idarəetmə səhifələri
    path('ai-management/', views.ai_management, name='ai_management'),
    path('train-model/', views.train_model, name='train_model'),
    path('export-model/', views.export_model, name='export_model'),
]
