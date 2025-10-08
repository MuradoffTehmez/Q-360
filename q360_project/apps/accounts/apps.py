"""
App configuration for accounts application.
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration class for accounts app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'İstifadəçi İdarəetməsi'

    def ready(self):
        """Import signal handlers when app is ready."""
        import apps.accounts.signals
