"""
WebSocket consumers for real-time audit and threat monitoring.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from datetime import timedelta


class ThreatMonitorConsumer(AsyncWebsocketConsumer):
    """
    Real-time threat monitoring WebSocket consumer.
    Sends threat updates to connected clients.
    """

    async def connect(self):
        """WebSocket connection handler."""
        self.user = self.scope['user']

        # Only allow authenticated admins
        if not self.user.is_authenticated or not (self.user.is_admin() or self.user.is_superadmin()):
            await self.close()
            return

        # Join threat monitoring room
        self.room_group_name = 'threat_monitor'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send initial threat data
        threat_data = await self.get_current_threat_stats()
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'data': threat_data
        }))

    async def disconnect(self, close_code):
        """WebSocket disconnection handler."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'get_stats':
            # Client requests current stats
            threat_data = await self.get_current_threat_stats()
            await self.send(text_data=json.dumps({
                'type': 'stats_update',
                'data': threat_data
            }))

        elif message_type == 'get_recent_threats':
            # Client requests recent high-threat logs
            hours = data.get('hours', 1)
            recent_threats = await self.get_recent_threats(hours)
            await self.send(text_data=json.dumps({
                'type': 'recent_threats',
                'data': recent_threats
            }))

    async def threat_alert(self, event):
        """
        Broadcast threat alert to all connected clients.
        Called when a new high-threat event is logged.
        """
        await self.send(text_data=json.dumps({
            'type': 'threat_alert',
            'data': event['data']
        }))

    async def stats_update(self, event):
        """
        Broadcast stats update to all connected clients.
        """
        await self.send(text_data=json.dumps({
            'type': 'stats_update',
            'data': event['data']
        }))

    @database_sync_to_async
    def get_current_threat_stats(self):
        """Get current threat statistics."""
        from apps.audit.models import AuditLog
        from collections import defaultdict

        # Last 24 hours stats
        start_time = timezone.now() - timedelta(hours=24)

        # Threat level distribution
        threat_distribution = {
            'critical': AuditLog.objects.filter(
                created_at__gte=start_time,
                threat_level='critical'
            ).count(),
            'high': AuditLog.objects.filter(
                created_at__gte=start_time,
                threat_level='high'
            ).count(),
            'medium': AuditLog.objects.filter(
                created_at__gte=start_time,
                threat_level='medium'
            ).count(),
            'low': AuditLog.objects.filter(
                created_at__gte=start_time,
                threat_level='low'
            ).count(),
        }

        # Failed login attempts per hour (last 24 hours)
        failed_logins_hourly = []
        for i in range(24):
            hour_start = timezone.now() - timedelta(hours=i+1)
            hour_end = timezone.now() - timedelta(hours=i)
            count = AuditLog.objects.filter(
                action='login_failure',
                created_at__gte=hour_start,
                created_at__lt=hour_end
            ).count()
            failed_logins_hourly.append({
                'hour': (timezone.now() - timedelta(hours=i)).strftime('%H:00'),
                'count': count
            })

        # Top threat users
        high_threat_logs = AuditLog.objects.filter(
            created_at__gte=start_time,
            threat_score__gte=60
        ).select_related('user')

        user_threats = defaultdict(lambda: {'count': 0, 'max_score': 0})
        for log in high_threat_logs:
            if log.user:
                user_threats[log.user.username]['count'] += 1
                user_threats[log.user.username]['max_score'] = max(
                    user_threats[log.user.username]['max_score'],
                    log.threat_score
                )

        top_users = sorted(
            [
                {'username': username, 'count': data['count'], 'max_score': data['max_score']}
                for username, data in user_threats.items()
            ],
            key=lambda x: x['max_score'],
            reverse=True
        )[:5]

        return {
            'timestamp': timezone.now().isoformat(),
            'threat_distribution': threat_distribution,
            'failed_logins_hourly': list(reversed(failed_logins_hourly)),
            'top_threat_users': top_users,
            'total_threats': sum(threat_distribution.values())
        }

    @database_sync_to_async
    def get_recent_threats(self, hours=1):
        """Get recent high-threat logs."""
        from apps.audit.models import AuditLog

        start_time = timezone.now() - timedelta(hours=hours)

        threats = AuditLog.objects.filter(
            created_at__gte=start_time,
            threat_score__gte=60
        ).select_related('user').order_by('-threat_score')[:20]

        return [
            {
                'id': log.id,
                'user': log.user.username if log.user else 'N/A',
                'action': log.action,
                'threat_level': log.threat_level,
                'threat_score': log.threat_score,
                'ip_address': log.ip_address,
                'timestamp': log.created_at.isoformat(),
                'severity': log.severity
            }
            for log in threats
        ]


class AuditLogConsumer(AsyncWebsocketConsumer):
    """
    Real-time audit log stream consumer.
    Broadcasts new audit logs to connected admins.
    """

    async def connect(self):
        """WebSocket connection handler."""
        self.user = self.scope['user']

        # Only allow authenticated admins
        if not self.user.is_authenticated or not (self.user.is_admin() or self.user.is_superadmin()):
            await self.close()
            return

        self.room_group_name = 'audit_logs'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """WebSocket disconnection handler."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def new_audit_log(self, event):
        """
        Broadcast new audit log to all connected clients.
        """
        await self.send(text_data=json.dumps({
            'type': 'new_log',
            'data': event['data']
        }))
