"""App configuration for competencies app."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompetenciesConfig(AppConfig):
    """Configuration for competencies app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.competencies'
    verbose_name = _('Kompetensiya İdarəetməsi')

    def ready(self):
        """Import signals when app is ready."""
        # Import signals here if needed
        pass
