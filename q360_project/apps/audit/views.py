"""
Views for audit app.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import AuditLog


class SecurityStatsView(APIView):
    """
    Təhlükəsizlik Statistikaları API View.
    Son 7 gündəki uğursuz giriş cəhdlərini və ən çox cəhd edən
    istifadəçilərin IP ünvanlarını qaytarır.

    Read-Only API - Yalnız Admin və Superadmin rolları üçün əlçatandır.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Son 7 gündəki uğursuz giriş statistikalarını qaytarır.

        Returns:
            - total_failures: Ümumi uğursuz giriş sayı
            - failures_by_day: Günlük uğursuz giriş sayları
            - top_failed_ips: Ən çox cəhd edən ilk 3 IP ünvanı
            - top_failed_users: Ən çox uğursuz cəhd edən ilk 3 istifadəçi
        """
        # Check if user has admin permissions
        from apps.accounts.rbac import RoleManager
        if not RoleManager.is_admin(request.user):
            return Response(
                {'detail': 'Bu əməliyyat üçün Admin icazəsi tələb olunur.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Calculate date 7 days ago
        seven_days_ago = timezone.now() - timedelta(days=7)

        # Get all login failures in the last 7 days
        login_failures = AuditLog.objects.filter(
            action='login_failure',
            created_at__gte=seven_days_ago
        )

        # Total failures
        total_failures = login_failures.count()

        # Failures by day (last 7 days)
        failures_by_day = []
        for i in range(7):
            day_start = timezone.now() - timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            day_count = login_failures.filter(
                created_at__gte=day_start,
                created_at__lt=day_end
            ).count()

            failures_by_day.append({
                'date': day_start.strftime('%Y-%m-%d'),
                'count': day_count
            })

        # Top 3 IP addresses with most failures
        top_failed_ips = login_failures.values('ip_address').annotate(
            failure_count=Count('id')
        ).order_by('-failure_count')[:3]

        # Format IP data
        top_ips_data = [
            {
                'ip_address': item['ip_address'] or 'Unknown',
                'failure_count': item['failure_count']
            }
            for item in top_failed_ips
        ]

        # Top 3 users with most failures (if user is not None)
        top_failed_users = login_failures.filter(
            user__isnull=False
        ).values('user__id', 'user__username', 'user__email').annotate(
            failure_count=Count('id')
        ).order_by('-failure_count')[:3]

        # Format user data
        top_users_data = [
            {
                'user_id': item['user__id'],
                'username': item['user__username'],
                'email': item['user__email'],
                'failure_count': item['failure_count']
            }
            for item in top_failed_users
        ]

        # Recent failures (last 10)
        recent_failures = login_failures.select_related('user').order_by('-created_at')[:10]

        recent_failures_data = [
            {
                'id': log.id,
                'user': log.user.username if log.user else None,
                'ip_address': log.ip_address,
                'user_agent': log.user_agent[:100] if log.user_agent else None,  # Truncate
                'timestamp': log.created_at.isoformat()
            }
            for log in recent_failures
        ]

        return Response({
            'success': True,
            'period': 'Son 7 gün',
            'total_failures': total_failures,
            'failures_by_day': failures_by_day,
            'top_failed_ips': top_ips_data,
            'top_failed_users': top_users_data,
            'recent_failures': recent_failures_data,
            'generated_at': timezone.now().isoformat()
        })


class AuditLogListView(APIView):
    """
    Audit Log məlumatlarını qaytaran API View.
    Yalnız Admin və Superadmin rolları üçün əlçatandır.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Audit log qeydlərini qaytarır.
        Query parametrləri:
            - action: Əməliyyat növü (login, logout, create, update, delete, login_failure)
            - days: Neçə gün əvvəlki qeydlər (default: 7)
            - limit: Maksimum qeyd sayı (default: 100)
        """
        from apps.accounts.rbac import RoleManager

        if not RoleManager.is_admin(request.user):
            return Response(
                {'detail': 'Bu əməliyyat üçün Admin icazəsi tələb olunur.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get query parameters
        action_filter = request.query_params.get('action')
        days = int(request.query_params.get('days', 7))
        limit = int(request.query_params.get('limit', 100))

        # Calculate date range
        start_date = timezone.now() - timedelta(days=days)

        # Base queryset
        logs = AuditLog.objects.filter(created_at__gte=start_date)

        # Filter by action if specified
        if action_filter:
            logs = logs.filter(action=action_filter)

        # Order by latest first
        logs = logs.order_by('-created_at')[:limit]

        # Serialize data
        logs_data = [
            {
                'id': log.id,
                'user': log.user.username if log.user else None,
                'action': log.action,
                'model_name': log.model_name,
                'object_id': log.object_id,
                'ip_address': log.ip_address,
                'timestamp': log.created_at.isoformat(),
                'changes': log.changes
            }
            for log in logs
        ]

        return Response({
            'success': True,
            'total': len(logs_data),
            'logs': logs_data
        })


@login_required
def log_search(request):
    """
    Audit log axtarışı səhifəsi
    """
    # Get date filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    user_filter = request.GET.get('user')
    action_filter = request.GET.get('action')
    resource_filter = request.GET.get('resource')
    ip_filter = request.GET.get('ip_address')
    
    # Base queryset
    logs = AuditLog.objects.all()
    
    # Apply filters
    if start_date:
        logs = logs.filter(created_at__date__gte=start_date)
    
    if end_date:
        logs = logs.filter(created_at__date__lte=end_date)
    
    if user_filter:
        logs = logs.filter(user__username__icontains=user_filter)
    
    if action_filter:
        logs = logs.filter(action=action_filter)
    
    if resource_filter:
        logs = logs.filter(resource__icontains=resource_filter)
    
    if ip_filter:
        logs = logs.filter(ip_address__icontains=ip_filter)
    
    # Order by latest first
    logs = logs.order_by('-created_at')
    
    # Get distinct action types for filters
    action_types = AuditLog.objects.values_list('action', flat=True).distinct()
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(logs, 25)  # Show 25 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'logs': page_obj,
        'action_types': action_types,
        'page_obj': page_obj,
    }
    
    return render(request, 'audit/log_search.html', context)
