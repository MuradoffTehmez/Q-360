"""App configuration for training app."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TrainingConfig(AppConfig):
    """Configuration for training app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.training'
    verbose_name = _('Təlim və İnkişaf')

    def ready(self):
        """Import signals when app is ready."""
        try:
            import apps.training.signals  # noqa
        except ImportError:
            pass
