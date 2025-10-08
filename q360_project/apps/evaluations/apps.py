"""
App configuration for evaluations application.
"""
from django.apps import AppConfig


class EvaluationsConfig(AppConfig):
    """Configuration class for evaluations app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.evaluations'
    verbose_name = '360° Qiymətləndirmə'

    def ready(self):
        """Import signal handlers when app is ready."""
        import apps.evaluations.signals
