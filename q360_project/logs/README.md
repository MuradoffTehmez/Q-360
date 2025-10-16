# Q360 Logging System

## 📋 Overview

Professional multi-level logging system with automatic rotation, structured logging, and monitoring capabilities.

## 📁 Log Files

### Main Logs
- **q360.log** - Main application log (15 MB, 10 backups) a
- **error.log** - Errors and critical issues only (10 MB, 10 backups)

### Specialized Logs
- **security.log** - Authentication, permissions, audit trail (10 MB, 15 backups)
- **database.log** - SQL queries and database operations (10 MB, 5 backups)
- **performance.log** - Slow requests and performance metrics (10 MB, 7 backups)
- **api.log** - REST API calls and responses (10 MB, 7 backups)
- **celery.log** - Background tasks and async operations (10 MB, 7 backups)

## 🎯 Log Levels

- **DEBUG** - Detailed diagnostic information (development only)
- **INFO** - General informational messages
- **WARNING** - Warning messages for potentially problematic situations
- **ERROR** - Error messages for serious problems
- **CRITICAL** - Critical issues that require immediate attention

## 🔧 Usage

### Basic Logging

```python
import logging

logger = logging.getLogger('apps.myapp')
logger.info('Application started')
logger.error('Something went wrong', exc_info=True)
```

### Context-Aware Logging

```python
from config.log_utils import get_logger

# In a Django view
def my_view(request):
    logger = get_logger('apps.myapp', request=request)
    logger.info('User accessed view', extra={'action': 'view_dashboard'})
    return Response()
```

### Security Event Logging

```python
from config.log_utils import log_security_event

# Log authentication attempts
log_security_event(
    event_type='login_attempt',
    user=user,
    description='User logged in successfully',
    request=request,
    severity='INFO'
)

# Log permission denied
log_security_event(
    event_type='permission_denied',
    user=request.user,
    description='Attempted to access admin panel',
    request=request,
    severity='WARNING',
    resource='/admin/users/'
)
```

### Performance Logging

```python
from config.log_utils import log_performance
import time

start = time.time()
# ... perform operation ...
duration = (time.time() - start) * 1000

log_performance(
    operation='generate_report',
    duration_ms=duration,
    request=request,
    report_type='analytics'
)
```

## 📊 Monitoring

### Command Line Monitoring

```bash
# Quick summary
python manage.py monitor_logs

# Detailed summary of all logs
python manage.py monitor_logs --summary

# Check error threshold
python manage.py monitor_logs --check-errors --threshold 100 --hours 1

# Cleanup old logs (30 days)
python manage.py monitor_logs --cleanup --days 30

# JSON output
python manage.py monitor_logs --summary --json
```

### Programmatic Monitoring

```python
from config.log_utils import LogMonitor

monitor = LogMonitor()

# Get summary of all logs
summary = monitor.get_all_logs_summary()

# Check error threshold
result = monitor.check_error_threshold(threshold=100, hours=1)

# Cleanup old logs
deleted = monitor.cleanup_old_logs(days=30)
```

### Log Analysis

```python
from config.log_utils import LogAnalyzer
from pathlib import Path

analyzer = LogAnalyzer(Path('logs/error.log'))

# Get error count in last 24 hours
error_count = analyzer.get_error_count(hours=24)

# Get latest errors
latest_errors = analyzer.get_latest_errors(limit=10)

# Analyze patterns
stats = analyzer.analyze_log_patterns()
```

## 🎨 Custom JSON Formatter

For production monitoring and log aggregation (e.g., ELK Stack, Splunk):

```python
# Add to settings.py handlers
'json_file': {
    'level': 'INFO',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': BASE_DIR / 'logs' / 'q360.json',
    'maxBytes': 1024 * 1024 * 10,
    'backupCount': 10,
    'formatter': 'json',  # Use JSON formatter
}
```

Example JSON output:
```json
{
  "timestamp": "2025-10-16 12:34:56",
  "level": "ERROR",
  "logger": "apps.accounts",
  "module": "views",
  "function": "login_view",
  "line": 42,
  "message": "Login failed",
  "request": {
    "method": "POST",
    "path": "/accounts/login/",
    "user": "john_doe",
    "ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0..."
  },
  "exception": {
    "type": "ValidationError",
    "message": "Invalid credentials",
    "traceback": ["..."]
  }
}
```

## ⚙️ Configuration

### Log Rotation Settings

Edit `config/settings.py` to adjust rotation settings:

```python
'file': {
    'maxBytes': 1024 * 1024 * 15,  # 15 MB
    'backupCount': 10,  # Keep 10 backup files
}
```

### Environment-Specific Settings

- **Development**: DEBUG logs enabled, console output verbose
- **Production**: INFO level, errors emailed to admins, JSON formatting

### Email Alerts (Production)

Configure `ADMINS` in settings.py to receive error emails:

```python
ADMINS = [
    ('Admin Name', 'admin@example.com'),
]
```

## 🔍 Best Practices

1. **Use appropriate log levels**
   - DEBUG: Development diagnostics
   - INFO: Normal operation events
   - WARNING: Unexpected but handled situations
   - ERROR: Serious problems
   - CRITICAL: System failures

2. **Include context**
   ```python
   logger.info('User action', extra={
       'user_id': user.id,
       'action': 'delete_record',
       'record_id': 123
   })
   ```

3. **Log exceptions properly**
   ```python
   try:
       dangerous_operation()
   except Exception as e:
       logger.error('Operation failed', exc_info=True)
   ```

4. **Don't log sensitive data**
   - Avoid logging passwords, tokens, API keys
   - Mask credit card numbers, personal data

5. **Use structured logging**
   - Add meaningful context
   - Use consistent field names
   - Enable easy searching and filtering

## 🔒 Security Considerations

- Log files contain sensitive information
- Restrict file permissions: `chmod 640 logs/*.log`
- Regular cleanup of old logs
- Consider log encryption for highly sensitive data
- Use log aggregation services for centralized monitoring

## 📈 Performance Tips

- Avoid excessive DEBUG logging in production
- Use asynchronous logging for high-traffic applications
- Monitor log file sizes and rotation
- Consider log sampling for very high-volume logs

## 🆘 Troubleshooting

### Log files not created
- Check directory permissions
- Verify `logs/` directory exists
- Check disk space

### Logs not rotating
- Verify `maxBytes` and `backupCount` settings
- Check file permissions
- Ensure application has write access

### Missing logs
- Check logger names match configuration
- Verify propagate settings
- Review log level filtering

## 📚 Additional Resources

- [Django Logging Documentation](https://docs.djangoproject.com/en/stable/topics/logging/)
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Log Aggregation Best Practices](https://www.elastic.co/guide/en/ecs/current/ecs-logging.html)

---

**Q360 Performance Management System © 2025**
