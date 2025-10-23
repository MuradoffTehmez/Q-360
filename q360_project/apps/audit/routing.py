"""
WebSocket routing for audit app.
"""
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/audit/threat-monitor/', consumers.ThreatMonitorConsumer.as_asgi()),
    path('ws/audit/logs/', consumers.AuditLogConsumer.as_asgi()),
]
