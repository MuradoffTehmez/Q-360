from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SecurityStatsView, AuditLogListView
from . import template_views

app_name = 'audit'

# DRF Router for API endpoints
router = DefaultRouter()

urlpatterns = router.urls + [
    # API Views
    path('security-stats/', SecurityStatsView.as_view(), name='security-stats'),
    path('logs/', AuditLogListView.as_view(), name='audit-logs'),

    # Template-based URLs
    path('security/', template_views.security_dashboard, name='security-dashboard'),
]
