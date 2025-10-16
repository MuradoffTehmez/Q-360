"""
Q360 - Professional Logging Utilities
Advanced logging helpers, custom formatters, and monitoring tools
"""
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from django.conf import settings


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    Outputs logs in JSON format for easy parsing by log aggregation tools.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
            'process': record.process,
            'thread': record.thread,
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }

        # Add extra fields if present
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data

        # Add request info if available (Django-specific)
        if hasattr(record, 'request'):
            request = record.request
            log_data['request'] = {
                'method': request.method,
                'path': request.path,
                'user': str(request.user) if hasattr(request, 'user') else 'Anonymous',
                'ip': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            }

        return json.dumps(log_data, ensure_ascii=False)

    @staticmethod
    def get_client_ip(request) -> str:
        """Extract client IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ContextLogger:
    """
    Context-aware logger that adds request/user context to all logs.
    Usage:
        logger = ContextLogger('apps.myapp', request=request)
        logger.info('User logged in', extra={'user_id': user.id})
    """

    def __init__(self, name: str, request=None, user=None, extra_context: Optional[Dict] = None):
        """Initialize context logger."""
        self.logger = logging.getLogger(name)
        self.request = request
        self.user = user or (request.user if request and hasattr(request, 'user') else None)
        self.extra_context = extra_context or {}

    def _add_context(self, extra: Optional[Dict] = None) -> Dict:
        """Add context information to extra data."""
        context = {}

        # Add user context
        if self.user and hasattr(self.user, 'username'):
            context['user_id'] = self.user.id
            context['username'] = self.user.username
            context['user_email'] = self.user.email

        # Add request context
        if self.request:
            context['request_path'] = self.request.path
            context['request_method'] = self.request.method
            context['request_ip'] = JSONFormatter.get_client_ip(self.request)

        # Merge with extra context
        context.update(self.extra_context)

        # Merge with provided extra
        if extra:
            context.update(extra)

        return {'extra_data': context}

    def debug(self, message: str, extra: Optional[Dict] = None):
        """Log debug message with context."""
        self.logger.debug(message, extra=self._add_context(extra))

    def info(self, message: str, extra: Optional[Dict] = None):
        """Log info message with context."""
        self.logger.info(message, extra=self._add_context(extra))

    def warning(self, message: str, extra: Optional[Dict] = None):
        """Log warning message with context."""
        self.logger.warning(message, extra=self._add_context(extra))

    def error(self, message: str, extra: Optional[Dict] = None, exc_info: bool = False):
        """Log error message with context."""
        self.logger.error(message, extra=self._add_context(extra), exc_info=exc_info)

    def critical(self, message: str, extra: Optional[Dict] = None, exc_info: bool = False):
        """Log critical message with context."""
        self.logger.critical(message, extra=self._add_context(extra), exc_info=exc_info)


class LogAnalyzer:
    """
    Analyze log files and extract insights.
    Useful for monitoring and alerting.
    """

    def __init__(self, log_file_path: Path):
        """Initialize log analyzer."""
        self.log_file = log_file_path

    def get_error_count(self, hours: int = 24) -> int:
        """Get count of errors in last N hours."""
        count = 0
        cutoff_time = datetime.now().timestamp() - (hours * 3600)

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if '[ERROR]' in line or '[CRITICAL]' in line:
                        # Try to extract timestamp
                        try:
                            # Example: [ERROR] 2025-01-16 12:34:56 | ...
                            parts = line.split('|')
                            if len(parts) > 0:
                                timestamp_str = parts[0].split(']')[1].strip()
                                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').timestamp()
                                if timestamp >= cutoff_time:
                                    count += 1
                        except (ValueError, IndexError):
                            # If parsing fails, count anyway (better safe than sorry)
                            count += 1
        except FileNotFoundError:
            pass

        return count

    def get_latest_errors(self, limit: int = 10) -> list:
        """Get latest N errors from log file."""
        errors = []

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Process lines in reverse to get latest first
            for line in reversed(lines):
                if '[ERROR]' in line or '[CRITICAL]' in line:
                    errors.append(line.strip())
                    if len(errors) >= limit:
                        break
        except FileNotFoundError:
            pass

        return errors

    def analyze_log_patterns(self) -> Dict[str, Any]:
        """Analyze log file and return statistics."""
        stats = {
            'total_lines': 0,
            'debug_count': 0,
            'info_count': 0,
            'warning_count': 0,
            'error_count': 0,
            'critical_count': 0,
            'unique_modules': set(),
            'common_errors': {},
        }

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    stats['total_lines'] += 1

                    # Count by level
                    if '[DEBUG]' in line:
                        stats['debug_count'] += 1
                    elif '[INFO]' in line:
                        stats['info_count'] += 1
                    elif '[WARNING]' in line:
                        stats['warning_count'] += 1
                    elif '[ERROR]' in line:
                        stats['error_count'] += 1
                        # Extract error message
                        try:
                            error_msg = line.split('|')[-1].strip()[:100]
                            stats['common_errors'][error_msg] = stats['common_errors'].get(error_msg, 0) + 1
                        except IndexError:
                            pass
                    elif '[CRITICAL]' in line:
                        stats['critical_count'] += 1

                    # Extract module name
                    try:
                        parts = line.split('|')
                        if len(parts) > 1:
                            module = parts[1].strip().split(':')[0]
                            stats['unique_modules'].add(module)
                    except (IndexError, ValueError):
                        pass

        except FileNotFoundError:
            pass

        # Convert set to list for JSON serialization
        stats['unique_modules'] = list(stats['unique_modules'])

        # Sort common errors by frequency
        if stats['common_errors']:
            stats['common_errors'] = dict(
                sorted(stats['common_errors'].items(), key=lambda x: x[1], reverse=True)[:10]
            )

        return stats


class LogMonitor:
    """
    Monitor log files and send alerts when thresholds are exceeded.
    """

    def __init__(self):
        """Initialize log monitor."""
        self.logs_dir = settings.BASE_DIR / 'logs'

    def check_error_threshold(self, threshold: int = 100, hours: int = 1) -> Dict[str, Any]:
        """Check if error count exceeds threshold."""
        error_log = self.logs_dir / 'error.log'
        analyzer = LogAnalyzer(error_log)
        error_count = analyzer.get_error_count(hours)

        result = {
            'threshold_exceeded': error_count > threshold,
            'error_count': error_count,
            'threshold': threshold,
            'hours': hours,
            'timestamp': datetime.now().isoformat(),
        }

        if result['threshold_exceeded']:
            # Get latest errors for alert
            result['latest_errors'] = analyzer.get_latest_errors(5)

        return result

    def get_all_logs_summary(self) -> Dict[str, Any]:
        """Get summary of all log files."""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'logs': {}
        }

        log_files = {
            'main': 'q360.log',
            'error': 'error.log',
            'security': 'security.log',
            'api': 'api.log',
            'database': 'database.log',
            'performance': 'performance.log',
            'celery': 'celery.log',
        }

        for log_type, filename in log_files.items():
            log_path = self.logs_dir / filename
            if log_path.exists():
                analyzer = LogAnalyzer(log_path)
                stats = analyzer.analyze_log_patterns()
                summary['logs'][log_type] = {
                    'file_size_mb': round(log_path.stat().st_size / (1024 * 1024), 2),
                    'last_modified': datetime.fromtimestamp(log_path.stat().st_mtime).isoformat(),
                    'stats': stats
                }
            else:
                summary['logs'][log_type] = {'exists': False}

        return summary

    def cleanup_old_logs(self, days: int = 30):
        """Delete log files older than N days."""
        cutoff_time = datetime.now().timestamp() - (days * 86400)
        deleted_files = []

        for log_file in self.logs_dir.glob('*.log.*'):  # Backup files with extensions
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                    deleted_files.append(str(log_file))
                except Exception as e:
                    logging.error(f"Failed to delete old log file {log_file}: {e}")

        return {
            'deleted_count': len(deleted_files),
            'deleted_files': deleted_files,
            'cutoff_days': days
        }


# Convenience function for getting a context logger
def get_logger(name: str, request=None, **kwargs) -> ContextLogger:
    """
    Get a context-aware logger.

    Usage:
        logger = get_logger('apps.accounts', request=request)
        logger.info('User logged in successfully')
    """
    return ContextLogger(name, request=request, **kwargs)


# Convenience function for security logging
def log_security_event(event_type: str, user, description: str, request=None, severity: str = 'INFO', **extra):
    """
    Log security-related events.

    Args:
        event_type: Type of security event (login, logout, permission_denied, etc.)
        user: User object or username
        description: Event description
        request: HTTP request object
        severity: Log level (INFO, WARNING, ERROR, CRITICAL)
        **extra: Additional context data
    """
    logger = logging.getLogger('apps.audit')

    context = {
        'event_type': event_type,
        'user': str(user),
        'description': description,
        **extra
    }

    if request:
        context['ip'] = JSONFormatter.get_client_ip(request)
        context['path'] = request.path
        context['method'] = request.method

    message = f"[SECURITY] {event_type.upper()}: {description}"

    if severity.upper() == 'DEBUG':
        logger.debug(message, extra={'extra_data': context})
    elif severity.upper() == 'INFO':
        logger.info(message, extra={'extra_data': context})
    elif severity.upper() == 'WARNING':
        logger.warning(message, extra={'extra_data': context})
    elif severity.upper() == 'ERROR':
        logger.error(message, extra={'extra_data': context})
    elif severity.upper() == 'CRITICAL':
        logger.critical(message, extra={'extra_data': context})


# Convenience function for performance logging
def log_performance(operation: str, duration_ms: float, request=None, **extra):
    """
    Log performance metrics.

    Args:
        operation: Name of the operation
        duration_ms: Duration in milliseconds
        request: HTTP request object
        **extra: Additional context data
    """
    logger = logging.getLogger('apps.reports')

    context = {
        'operation': operation,
        'duration_ms': duration_ms,
        **extra
    }

    if request:
        context['path'] = request.path
        context['method'] = request.method

    # Log as WARNING if slow (> 1000ms)
    message = f"[PERFORMANCE] {operation}: {duration_ms:.2f}ms"

    if duration_ms > 1000:
        logger.warning(message, extra={'extra_data': context})
    else:
        logger.info(message, extra={'extra_data': context})
