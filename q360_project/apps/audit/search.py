"""
Full-text search utilities for audit logs using PostgreSQL.
"""
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from .models import AuditLog


def update_audit_search_vector(audit_log):
    """
    Update search vector for a single audit log entry.

    Args:
        audit_log: AuditLog instance
    """
    AuditLog.objects.filter(pk=audit_log.pk).update(
        search_vector=(
            SearchVector('model_name', weight='A') +
            SearchVector('action', weight='A') +
            SearchVector('request_path', weight='B') +
            SearchVector('actor_role', weight='C') +
            SearchVector('user_agent', weight='D')
        )
    )


def search_audit_logs(search_query, filters=None):
    """
    Search audit logs using PostgreSQL full-text search.

    Args:
        search_query (str): Search query string
        filters (dict): Additional filters (user, action, severity, date_range, etc.)

    Returns:
        QuerySet: Filtered and ranked audit logs
    """
    if not search_query:
        queryset = AuditLog.objects.all()
    else:
        # Create PostgreSQL search query
        query = SearchQuery(search_query, search_type='websearch')

        # Search and rank results
        queryset = AuditLog.objects.annotate(
            rank=SearchRank('search_vector', query)
        ).filter(
            search_vector=query
        ).order_by('-rank', '-created_at')

    # Apply additional filters
    if filters:
        if 'user' in filters and filters['user']:
            queryset = queryset.filter(user=filters['user'])

        if 'action' in filters and filters['action']:
            queryset = queryset.filter(action=filters['action'])

        if 'model_name' in filters and filters['model_name']:
            queryset = queryset.filter(model_name__icontains=filters['model_name'])

        if 'severity' in filters and filters['severity']:
            queryset = queryset.filter(severity=filters['severity'])

        if 'ip_address' in filters and filters['ip_address']:
            queryset = queryset.filter(ip_address=filters['ip_address'])

        if 'date_from' in filters and filters['date_from']:
            queryset = queryset.filter(created_at__gte=filters['date_from'])

        if 'date_to' in filters and filters['date_to']:
            queryset = queryset.filter(created_at__lte=filters['date_to'])

    return queryset


def search_logs_by_user_activity(user, search_query=None, limit=100):
    """
    Search logs related to specific user's activity.

    Args:
        user: User object
        search_query (str): Optional search query
        limit (int): Maximum results

    Returns:
        QuerySet: User's audit logs
    """
    queryset = AuditLog.objects.filter(user=user)

    if search_query:
        query = SearchQuery(search_query, search_type='websearch')
        queryset = queryset.annotate(
            rank=SearchRank('search_vector', query)
        ).filter(
            search_vector=query
        ).order_by('-rank', '-created_at')
    else:
        queryset = queryset.order_by('-created_at')

    return queryset[:limit]


def search_security_events(search_query=None, severity='critical', limit=100):
    """
    Search security-related audit events.

    Args:
        search_query (str): Optional search query
        severity (str): Severity level (info, warning, critical)
        limit (int): Maximum results

    Returns:
        QuerySet: Security audit logs
    """
    # Security-related actions
    security_actions = ['login_failure', 'permission_denied', 'delete']

    queryset = AuditLog.objects.filter(
        Q(action__in=security_actions) | Q(severity=severity)
    )

    if search_query:
        query = SearchQuery(search_query, search_type='websearch')
        queryset = queryset.annotate(
            rank=SearchRank('search_vector', query)
        ).filter(
            search_vector=query
        ).order_by('-rank', '-created_at')
    else:
        queryset = queryset.order_by('-created_at')

    return queryset[:limit]


def rebuild_search_vectors(batch_size=500):
    """
    Rebuild search vectors for all audit logs.
    Useful for bulk updates or when search configuration changes.

    Args:
        batch_size (int): Number of records to process at once

    Returns:
        int: Number of updated records
    """
    from django.db import transaction

    total_updated = 0
    audit_logs = AuditLog.objects.filter(search_vector__isnull=True)

    with transaction.atomic():
        for audit_log in audit_logs.iterator(chunk_size=batch_size):
            update_audit_search_vector(audit_log)
            total_updated += 1

            if total_updated % batch_size == 0:
                print(f"Updated {total_updated} audit logs...")

    # Update existing logs
    AuditLog.objects.filter(search_vector__isnull=False).update(
        search_vector=(
            SearchVector('model_name', weight='A') +
            SearchVector('action', weight='A') +
            SearchVector('request_path', weight='B') +
            SearchVector('actor_role', weight='C') +
            SearchVector('user_agent', weight='D')
        )
    )

    total_count = AuditLog.objects.count()
    print(f"Rebuilt search vectors for {total_count} audit logs")
    return total_count
