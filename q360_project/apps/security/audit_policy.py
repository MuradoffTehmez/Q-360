"""
Audit Policy Service - Təhlükəsizlik siyasətlərinin idarə edilməsi.
"""
from typing import Optional, Dict, Any, List
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from apps.audit.models import AuditLog


class AuditPolicyViolation(Exception):
    """Audit policy pozuntusu istisna."""
    pass


class AuditPolicy:
    """
    Audit policy siyasətlərinin tətbiqi və monitorinqi.
    """

    # Default siyasətlər
    DEFAULT_POLICIES = {
        'max_failed_logins': 5,  # Maksimum uğursuz giriş cəhdi
        'failed_login_window_minutes': 30,  # Zaman pəncərəsi
        'account_lockout_duration_minutes': 60,  # Hesab bloklanma müddəti
        'max_permission_denials': 10,  # Maksimum icazə rəddi
        'permission_denial_window_minutes': 60,
        'max_critical_actions': 20,  # Maksimum kritik əməliyyat
        'critical_action_window_minutes': 60,
        'suspicious_ip_threshold': 15,  # Şübhəli IP aktivlik həddi
        'require_mfa_for_critical': True,  # Kritik əməliyyatlar üçün MFA tələb et
        'enable_geo_blocking': False,  # Geo-blocking aktiv
        'allowed_countries': ['AZ', 'TR', 'US', 'GB'],  # İcazə verilən ölkələr
        'enable_rate_limiting': True,  # Rate limiting aktiv
        'api_rate_limit_per_minute': 100,  # Dəqiqədə API sorğu limiti
        'enable_session_timeout': True,  # Session timeout aktiv
        'session_idle_timeout_minutes': 30,  # Session idle timeout
        'session_absolute_timeout_hours': 8,  # Session absolute timeout
    }

    def __init__(self, custom_policies: Optional[Dict[str, Any]] = None):
        """
        Initialize audit policy with custom or default settings.

        Args:
            custom_policies: Custom policy overrides
        """
        self.policies = self.DEFAULT_POLICIES.copy()
        if custom_policies:
            self.policies.update(custom_policies)

    def check_failed_login_policy(self, user=None, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """
        Uğursuz giriş cəhdlərini yoxlayır.

        Returns:
            dict: {
                'is_violation': bool,
                'failed_attempts': int,
                'lockout_until': datetime or None,
                'reason': str
            }
        """
        window_start = timezone.now() - timedelta(
            minutes=self.policies['failed_login_window_minutes']
        )

        # User-based failed logins
        user_failed_attempts = 0
        if user:
            user_failed_attempts = AuditLog.objects.filter(
                user=user,
                action='login_failure',
                created_at__gte=window_start
            ).count()

        # IP-based failed logins
        ip_failed_attempts = 0
        if ip_address:
            ip_failed_attempts = AuditLog.objects.filter(
                ip_address=ip_address,
                action='login_failure',
                created_at__gte=window_start
            ).count()

        max_attempts = self.policies['max_failed_logins']
        total_attempts = max(user_failed_attempts, ip_failed_attempts)

        is_violation = total_attempts >= max_attempts
        lockout_until = None

        if is_violation:
            lockout_until = timezone.now() + timedelta(
                minutes=self.policies['account_lockout_duration_minutes']
            )

        return {
            'is_violation': is_violation,
            'failed_attempts': total_attempts,
            'user_attempts': user_failed_attempts,
            'ip_attempts': ip_failed_attempts,
            'lockout_until': lockout_until,
            'reason': f'Çox sayda uğursuz giriş cəhdi: {total_attempts}/{max_attempts}' if is_violation else None
        }

    def check_permission_denial_policy(self, user) -> Dict[str, Any]:
        """
        İcazə rədd edilmələri yoxlayır.

        Returns:
            dict: {
                'is_violation': bool,
                'denial_count': int,
                'reason': str
            }
        """
        window_start = timezone.now() - timedelta(
            minutes=self.policies['permission_denial_window_minutes']
        )

        denial_count = AuditLog.objects.filter(
            user=user,
            action='permission_denied',
            created_at__gte=window_start
        ).count()

        max_denials = self.policies['max_permission_denials']
        is_violation = denial_count >= max_denials

        return {
            'is_violation': is_violation,
            'denial_count': denial_count,
            'max_denials': max_denials,
            'reason': f'Çox sayda icazə rəddi: {denial_count}/{max_denials}' if is_violation else None
        }

    def check_critical_action_policy(self, user) -> Dict[str, Any]:
        """
        Kritik əməliyyatları yoxlayır.

        Returns:
            dict: {
                'is_violation': bool,
                'critical_count': int,
                'reason': str
            }
        """
        window_start = timezone.now() - timedelta(
            minutes=self.policies['critical_action_window_minutes']
        )

        critical_count = AuditLog.objects.filter(
            user=user,
            severity='critical',
            created_at__gte=window_start
        ).count()

        max_critical = self.policies['max_critical_actions']
        is_violation = critical_count >= max_critical

        return {
            'is_violation': is_violation,
            'critical_count': critical_count,
            'max_critical': max_critical,
            'reason': f'Çox sayda kritik əməliyyat: {critical_count}/{max_critical}' if is_violation else None
        }

    def check_suspicious_ip_activity(self, ip_address: str) -> Dict[str, Any]:
        """
        Şübhəli IP aktivliyini yoxlayır.

        Returns:
            dict: {
                'is_suspicious': bool,
                'activity_count': int,
                'reason': str
            }
        """
        window_start = timezone.now() - timedelta(minutes=60)

        # Get all activities from this IP
        activity_count = AuditLog.objects.filter(
            ip_address=ip_address,
            created_at__gte=window_start
        ).count()

        # Get failed attempts
        failed_attempts = AuditLog.objects.filter(
            ip_address=ip_address,
            action__in=['login_failure', 'permission_denied'],
            created_at__gte=window_start
        ).count()

        threshold = self.policies['suspicious_ip_threshold']
        is_suspicious = failed_attempts >= threshold

        return {
            'is_suspicious': is_suspicious,
            'activity_count': activity_count,
            'failed_attempts': failed_attempts,
            'threshold': threshold,
            'reason': f'Şübhəli IP aktivliyi: {failed_attempts} uğursuz cəhd' if is_suspicious else None
        }

    def validate_user_action(
        self,
        user,
        action: str,
        severity: str = 'info',
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        İstifadəçi əməliyyatını bütün siyasətlərə görə yoxlayır.

        Args:
            user: User object
            action: Action type
            severity: Severity level
            ip_address: IP address

        Returns:
            dict: {
                'allowed': bool,
                'violations': list,
                'warnings': list
            }
        """
        violations = []
        warnings = []

        # Check failed login policy
        if action == 'login' and user:
            login_check = self.check_failed_login_policy(user, ip_address)
            if login_check['is_violation']:
                violations.append({
                    'type': 'failed_login',
                    'details': login_check
                })

        # Check permission denial policy
        if user:
            denial_check = self.check_permission_denial_policy(user)
            if denial_check['is_violation']:
                violations.append({
                    'type': 'permission_denial',
                    'details': denial_check
                })

        # Check critical action policy
        if severity == 'critical' and user:
            critical_check = self.check_critical_action_policy(user)
            if critical_check['is_violation']:
                warnings.append({
                    'type': 'critical_action',
                    'details': critical_check
                })

        # Check suspicious IP
        if ip_address:
            ip_check = self.check_suspicious_ip_activity(ip_address)
            if ip_check['is_suspicious']:
                warnings.append({
                    'type': 'suspicious_ip',
                    'details': ip_check
                })

        return {
            'allowed': len(violations) == 0,
            'violations': violations,
            'warnings': warnings
        }

    def get_user_risk_score(self, user) -> Dict[str, Any]:
        """
        İstifadəçinin risk skorunu hesablayır.

        Returns:
            dict: {
                'risk_score': int (0-100),
                'risk_level': str (low, medium, high, critical),
                'factors': list
            }
        """
        risk_score = 0
        factors = []

        # Failed login attempts (max 30 points)
        login_check = self.check_failed_login_policy(user)
        if login_check['failed_attempts'] > 0:
            login_risk = min(login_check['failed_attempts'] * 10, 30)
            risk_score += login_risk
            factors.append({
                'factor': 'failed_logins',
                'score': login_risk,
                'details': f"{login_check['failed_attempts']} uğursuz giriş"
            })

        # Permission denials (max 25 points)
        denial_check = self.check_permission_denial_policy(user)
        if denial_check['denial_count'] > 0:
            denial_risk = min(denial_check['denial_count'] * 5, 25)
            risk_score += denial_risk
            factors.append({
                'factor': 'permission_denials',
                'score': denial_risk,
                'details': f"{denial_check['denial_count']} icazə rəddi"
            })

        # Critical actions (max 25 points)
        critical_check = self.check_critical_action_policy(user)
        if critical_check['critical_count'] > 0:
            critical_risk = min(critical_check['critical_count'] * 2, 25)
            risk_score += critical_risk
            factors.append({
                'factor': 'critical_actions',
                'score': critical_risk,
                'details': f"{critical_check['critical_count']} kritik əməliyyat"
            })

        # Recent threat level (max 20 points)
        recent_logs = AuditLog.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).order_by('-threat_score').first()

        if recent_logs and recent_logs.threat_score > 0:
            threat_risk = min(recent_logs.threat_score // 5, 20)
            risk_score += threat_risk
            factors.append({
                'factor': 'threat_level',
                'score': threat_risk,
                'details': f"Təhlükə skoru: {recent_logs.threat_score}"
            })

        # Determine risk level
        if risk_score >= 75:
            risk_level = 'critical'
        elif risk_score >= 50:
            risk_level = 'high'
        elif risk_score >= 25:
            risk_level = 'medium'
        else:
            risk_level = 'low'

        return {
            'risk_score': min(risk_score, 100),
            'risk_level': risk_level,
            'factors': factors
        }

    def get_security_recommendations(self, user) -> List[Dict[str, str]]:
        """
        İstifadəçi üçün təhlükəsizlik tövsiyələri.

        Returns:
            list: Recommendation objects
        """
        recommendations = []
        risk_assessment = self.get_user_risk_score(user)

        if risk_assessment['risk_level'] in ['high', 'critical']:
            recommendations.append({
                'severity': 'high',
                'title': 'Şifrəni dəyişdirin',
                'description': 'Hesabınızda şübhəli aktivlik aşkarlandı. Təhlükəsizlik üçün şifrənizi dərhal dəyişdirin.',
                'action': 'change_password'
            })

        # Check if MFA is enabled
        if not getattr(user, 'mfa_enabled', False):
            recommendations.append({
                'severity': 'medium',
                'title': 'İki faktorlu autentifikasiya aktivləşdirin',
                'description': 'Hesabınızın təhlükəsizliyini artırmaq üçün 2FA-nı aktivləşdirin.',
                'action': 'enable_mfa'
            })

        # Check for old sessions
        if hasattr(user, 'sessions'):
            active_sessions = user.sessions.filter(expire_date__gt=timezone.now()).count()
            if active_sessions > 3:
                recommendations.append({
                    'severity': 'low',
                    'title': 'Aktiv sessiyaları yoxlayın',
                    'description': f'{active_sessions} aktiv sessiyanız var. Tanımadığınız cihazları silin.',
                    'action': 'review_sessions'
                })

        return recommendations


# Global instance
default_audit_policy = AuditPolicy()
