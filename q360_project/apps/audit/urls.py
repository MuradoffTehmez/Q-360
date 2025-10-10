from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SecurityStatsView, AuditLogListView

router = DefaultRouter()

app_name = 'audit'

urlpatterns = [
    path('', include(router.urls)),
    path('security-stats/', SecurityStatsView.as_view(), name='security-stats'),
    path('logs/', AuditLogListView.as_view(), name='audit-logs'),
]
