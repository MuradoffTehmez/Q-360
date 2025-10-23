"""
Session Tracking Service - İstifadəçi sessiyalarının izlənməsi və idarə edilməsi.
"""
from typing import Optional, Dict, Any, List
from datetime import timedelta
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.db import models
from apps.audit.models import AuditLog


class UserSessionManager:
    """
    İstifadəçi sessiyalarının idarə edilməsi və izlənməsi.
    """

    @staticmethod
    def get_active_sessions(user) -> List[Dict[str, Any]]:
        """
        İstifadəçinin aktiv sessiyalarını gətirir.

        Returns:
            list: Session information dicts
        """
        from django.contrib.sessions.backends.db import SessionStore

        active_sessions = []
        current_time = timezone.now()

        # Get all non-expired sessions
        sessions = Session.objects.filter(expire_date__gt=current_time)

        for session in sessions:
            session_data = session.get_decoded()
            session_user_id = session_data.get('_auth_user_id')

            if session_user_id and str(session_user_id) == str(user.pk):
                # Get session metadata from audit logs
                session_audit = AuditLog.objects.filter(
                    user=user,
                    action='login',
                    context__session_key=session.session_key
                ).order_by('-created_at').first()

                session_info = {
                    'session_key': session.session_key,
                    'expire_date': session.expire_date,
                    'created_at': session_audit.created_at if session_audit else None,
                    'ip_address': session_audit.ip_address if session_audit else None,
                    'user_agent': session_audit.user_agent if session_audit else None,
                    'last_activity': session_data.get('last_activity'),
                    'is_current': session_data.get('is_current', False),
                }

                active_sessions.append(session_info)

        return active_sessions

    @staticmethod
    def get_session_count(user) -> int:
        """
        İstifadəçinin aktiv sessiya sayını qaytarır.

        Returns:
            int: Active session count
        """
        return len(UserSessionManager.get_active_sessions(user))

    @staticmethod
    def terminate_session(session_key: str) -> bool:
        """
        Müəyyən sessiyanı dayandırır.

        Args:
            session_key: Session key to terminate

        Returns:
            bool: Success status
        """
        try:
            session = Session.objects.get(session_key=session_key)
            session.delete()
            return True
        except Session.DoesNotExist:
            return False

    @staticmethod
    def terminate_all_sessions(user, except_current: Optional[str] = None) -> int:
        """
        İstifadəçinin bütün sessiyalarını dayandırır.

        Args:
            user: User object
            except_current: Session key to keep (current session)

        Returns:
            int: Number of terminated sessions
        """
        terminated_count = 0
        sessions = UserSessionManager.get_active_sessions(user)

        for session_info in sessions:
            session_key = session_info['session_key']
            if session_key != except_current:
                if UserSessionManager.terminate_session(session_key):
                    terminated_count += 1

        return terminated_count

    @staticmethod
    def check_session_timeout(session_data: Dict[str, Any], policies: Dict[str, Any]) -> Dict[str, Any]:
        """
        Session timeout-larını yoxlayır.

        Args:
            session_data: Session data dict
            policies: Timeout policies

        Returns:
            dict: {
                'is_expired': bool,
                'reason': str,
                'idle_time_minutes': int,
                'total_time_hours': float
            }
        """
        current_time = timezone.now()
        last_activity = session_data.get('last_activity')
        session_start = session_data.get('session_start')

        if not last_activity or not session_start:
            return {
                'is_expired': False,
                'reason': None,
                'idle_time_minutes': 0,
                'total_time_hours': 0
            }

        # Parse datetime if string
        if isinstance(last_activity, str):
            from django.utils.dateparse import parse_datetime
            last_activity = parse_datetime(last_activity)
        if isinstance(session_start, str):
            from django.utils.dateparse import parse_datetime
            session_start = parse_datetime(session_start)

        # Calculate idle time
        idle_time = current_time - last_activity
        idle_minutes = idle_time.total_seconds() / 60

        # Calculate total session time
        total_time = current_time - session_start
        total_hours = total_time.total_seconds() / 3600

        # Check idle timeout
        idle_timeout = policies.get('session_idle_timeout_minutes', 30)
        if idle_minutes > idle_timeout:
            return {
                'is_expired': True,
                'reason': f'Session {idle_minutes:.0f} dəqiqədir aktiv deyil (limit: {idle_timeout} dəqiqə)',
                'idle_time_minutes': int(idle_minutes),
                'total_time_hours': round(total_hours, 2)
            }

        # Check absolute timeout
        absolute_timeout = policies.get('session_absolute_timeout_hours', 8)
        if total_hours > absolute_timeout:
            return {
                'is_expired': True,
                'reason': f'Session {total_hours:.1f} saatdır davam edir (limit: {absolute_timeout} saat)',
                'idle_time_minutes': int(idle_minutes),
                'total_time_hours': round(total_hours, 2)
            }

        return {
            'is_expired': False,
            'reason': None,
            'idle_time_minutes': int(idle_minutes),
            'total_time_hours': round(total_hours, 2)
        }

    @staticmethod
    def update_session_activity(request):
        """
        Session aktivliyini yeniləyir.

        Args:
            request: Django request object
        """
        if request.user.is_authenticated and hasattr(request, 'session'):
            request.session['last_activity'] = timezone.now().isoformat()
            request.session.modified = True

    @staticmethod
    def get_session_analytics(user, days: int = 30) -> Dict[str, Any]:
        """
        İstifadəçi sessiya analitikası.

        Args:
            user: User object
            days: Number of days to analyze

        Returns:
            dict: Analytics data
        """
        start_date = timezone.now() - timedelta(days=days)

        # Get login events
        logins = AuditLog.objects.filter(
            user=user,
            action='login',
            created_at__gte=start_date
        )

        # Get logout events
        logouts = AuditLog.objects.filter(
            user=user,
            action='logout',
            created_at__gte=start_date
        )

        # Get unique IPs
        unique_ips = logins.values('ip_address').distinct().count()

        # Get unique devices (based on user agent)
        unique_devices = logins.values('user_agent').distinct().count()

        # Calculate average session duration (if we have logout times)
        avg_session_duration = None
        if logouts.exists():
            # This is simplified - in real scenario you'd match login/logout pairs
            session_durations = []
            for logout in logouts:
                matching_login = logins.filter(
                    created_at__lt=logout.created_at,
                    ip_address=logout.ip_address
                ).order_by('-created_at').first()

                if matching_login:
                    duration = (logout.created_at - matching_login.created_at).total_seconds() / 60
                    session_durations.append(duration)

            if session_durations:
                avg_session_duration = sum(session_durations) / len(session_durations)

        # Get login times distribution
        login_hours = logins.extra(
            select={'hour': "EXTRACT(hour FROM created_at)"}
        ).values('hour').annotate(count=models.Count('id'))

        # Get most used IPs
        top_ips = logins.values('ip_address').annotate(
            count=models.Count('id')
        ).order_by('-count')[:5]

        return {
            'total_logins': logins.count(),
            'total_logouts': logouts.count(),
            'active_sessions': UserSessionManager.get_session_count(user),
            'unique_ips': unique_ips,
            'unique_devices': unique_devices,
            'avg_session_duration_minutes': round(avg_session_duration, 2) if avg_session_duration else None,
            'login_hours_distribution': list(login_hours),
            'top_ips': list(top_ips),
            'period_days': days
        }

    @staticmethod
    def detect_suspicious_sessions(user) -> List[Dict[str, Any]]:
        """
        Şübhəli sessiyaları aşkarlayır.

        Returns:
            list: Suspicious session information
        """
        suspicious_sessions = []
        active_sessions = UserSessionManager.get_active_sessions(user)

        # Get user's typical IP addresses (from last 30 days)
        typical_ips = set(
            AuditLog.objects.filter(
                user=user,
                action='login',
                created_at__gte=timezone.now() - timedelta(days=30)
            ).values_list('ip_address', flat=True)
        )

        for session in active_sessions:
            suspicious_factors = []

            # Check if IP is new/unusual
            if session['ip_address'] and session['ip_address'] not in typical_ips:
                suspicious_factors.append('Yeni IP ünvanı')

            # Check if session has been idle for a long time but still active
            if session['last_activity']:
                idle_time = timezone.now() - session['last_activity']
                if idle_time > timedelta(hours=2):
                    suspicious_factors.append(f'{idle_time.total_seconds() / 3600:.1f} saat idle')

            # Check for concurrent sessions from different locations
            if len(active_sessions) > 3:
                suspicious_factors.append(f'{len(active_sessions)} eyni zamanlı sessiya')

            if suspicious_factors:
                suspicious_sessions.append({
                    'session_key': session['session_key'],
                    'ip_address': session['ip_address'],
                    'user_agent': session['user_agent'],
                    'created_at': session['created_at'],
                    'factors': suspicious_factors,
                    'risk_level': 'high' if len(suspicious_factors) > 2 else 'medium'
                })

        return suspicious_sessions

    @staticmethod
    def create_session_snapshot(user, request) -> Dict[str, Any]:
        """
        Session snapshot yaradır (audit üçün).

        Returns:
            dict: Session snapshot data
        """
        return {
            'session_key': request.session.session_key if hasattr(request, 'session') else None,
            'user_id': user.pk,
            'ip_address': _get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500],
            'session_start': request.session.get('session_start', timezone.now().isoformat()) if hasattr(request, 'session') else None,
            'last_activity': timezone.now().isoformat(),
            'is_current': True,
            'timestamp': timezone.now().isoformat()
        }


def _get_client_ip(request) -> Optional[str]:
    """Get client IP address from request."""
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


# Middleware integration helper
class SessionTrackingMiddleware:
    """
    Middleware for automatic session tracking.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Update session activity before processing request
        if request.user.is_authenticated:
            UserSessionManager.update_session_activity(request)

            # Initialize session start time if not set
            if hasattr(request, 'session') and 'session_start' not in request.session:
                request.session['session_start'] = timezone.now().isoformat()

        response = self.get_response(request)

        return response
