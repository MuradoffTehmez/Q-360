"""App configuration for compensation app."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompensationConfig(AppConfig):
    """Configuration for the Compensation & Benefits app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.compensation'
    verbose_name = _('Kompensasiya və Müavinətlər')
