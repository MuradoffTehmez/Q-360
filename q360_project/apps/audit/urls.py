from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SecurityStatsView, AuditLogListView
from . import template_views

router = DefaultRouter()

app_name = 'audit'

urlpatterns = [
    # Template URLs
    path('security/', template_views.security_dashboard, name='security-dashboard'),

    # API URLs
    path('', include(router.urls)),
    path('api/security-stats/', SecurityStatsView.as_view(), name='api-security-stats'),
    path('api/logs/', AuditLogListView.as_view(), name='api-audit-logs'),
]
