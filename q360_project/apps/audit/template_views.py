"""Template views for audit app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
import json
from collections import defaultdict
from .models import AuditLog


def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
    """
    Detect potential brute force attacks.

    Args:
        login_failures: QuerySet of login failure logs
        time_window: Time window in minutes (default: 5)
        threshold: Number of failures to trigger alert (default: 5)

    Returns:
        List of threats with IP address, username, count, and time span
    """
    threats = []

    # Group by IP address
    ip_grouped = defaultdict(list)
    for log in login_failures.order_by('-created_at'):
        if log.ip_address:
            ip_grouped[log.ip_address].append(log)

    # Analyze each IP for brute force patterns
    for ip, logs in ip_grouped.items():
        if len(logs) < threshold:
            continue

        # Check if threshold failures occurred within time_window minutes
        for i in range(len(logs) - threshold + 1):
            time_span = logs[i].created_at - logs[i + threshold - 1].created_at

            if time_span <= timedelta(minutes=time_window):
                # Brute force attack detected!
                usernames = set()
                for log in logs[i:i + threshold]:
                    if log.user:
                        usernames.add(log.user.username)
                    elif log.changes and 'username' in log.changes:
                        usernames.add(log.changes.get('username', 'Unknown'))

                threats.append({
                    'ip_address': ip,
                    'usernames': list(usernames),
                    'failure_count': threshold,
                    'time_span': time_span.total_seconds() / 60,  # in minutes
                    'first_attempt': logs[i + threshold - 1].created_at,
                    'last_attempt': logs[i].created_at,
                    'severity': 'critical' if threshold >= 10 else 'high'
                })
                break  # Only report once per IP

    # Sort by last attempt (most recent first)
    threats.sort(key=lambda x: x['last_attempt'], reverse=True)

    return threats


@login_required
def security_dashboard(request):
    """Security dashboard with full backend data and threat detection."""
    if not request.user.is_admin():
        return render(request, '403.html', status=403)

    # Get data for last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)

    # Total login failures in last 7 days
    login_failures = AuditLog.objects.filter(
        action='login_failure',
        created_at__gte=seven_days_ago
    )

    total_failures = login_failures.count()

    # Failures by day (last 7 days)
    failures_by_day = []
    for i in range(6, -1, -1):
        day_date = timezone.now() - timedelta(days=i)
        day_start = day_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        count = login_failures.filter(
            created_at__gte=day_start,
            created_at__lt=day_end
        ).count()

        failures_by_day.append({
            'date': day_date.strftime('%d %b'),
            'count': count
        })

    # Top failed IPs
    top_failed_ips = login_failures.values('ip_address').annotate(
        failure_count=Count('id')
    ).order_by('-failure_count')[:10]

    # Top failed users (by username from changes field or user field)
    top_failed_users_raw = login_failures.filter(
        user__isnull=False
    ).values('user__username').annotate(
        failure_count=Count('id')
    ).order_by('-failure_count')[:10]

    top_failed_users = [
        {'username': item['user__username'], 'failure_count': item['failure_count']}
        for item in top_failed_users_raw
    ]

    # Recent failures (last 20)
    recent_failures = login_failures.select_related('user').order_by('-created_at')[:20]
    recent_failures_data = [
        {
            'user': f.user.username if f.user else f.changes.get('username', 'Unknown'),
            'ip_address': f.ip_address or 'N/A',
            'timestamp': f.created_at.isoformat()
        }
        for f in recent_failures
    ]

    # *** NEW: THREAT DETECTION ***
    # Detect brute force attacks (5+ failures in 5 minutes)
    recent_failures_for_analysis = login_failures.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).select_related('user').prefetch_related()

    detected_threats = detect_brute_force_attacks(
        recent_failures_for_analysis,
        time_window=5,
        threshold=5
    )

    # Format threats for template
    threats_data = []
    for threat in detected_threats[:10]:  # Show top 10 threats
        threats_data.append({
            'ip_address': threat['ip_address'],
            'usernames': ', '.join(threat['usernames']) if threat['usernames'] else 'Unknown',
            'failure_count': threat['failure_count'],
            'time_span_minutes': round(threat['time_span'], 2),
            'last_attempt': threat['last_attempt'].strftime('%d %b %Y, %H:%M'),
            'severity': threat['severity']
        })

    context = {
        'total_failures': total_failures,
        'failures_by_day': json.dumps(failures_by_day),
        'top_failed_ips': list(top_failed_ips),
        'top_failed_users': top_failed_users,
        'recent_failures': recent_failures_data,
        'detected_threats': threats_data,  # NEW
        'threat_count': len(threats_data),  # NEW
    }

    return render(request, 'audit/security_dashboard.html', context)
