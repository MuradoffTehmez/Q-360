"""Template views for audit app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json
from .models import AuditLog

@login_required
def security_dashboard(request):
    """Security dashboard with full backend data."""
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

    context = {
        'total_failures': total_failures,
        'failures_by_day': json.dumps(failures_by_day),
        'top_failed_ips': list(top_failed_ips),
        'top_failed_users': top_failed_users,
        'recent_failures': recent_failures_data,
    }

    return render(request, 'audit/security_dashboard.html', context)
