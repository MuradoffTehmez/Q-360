"""
App configuration for departments application.
"""
from django.apps import AppConfig


class DepartmentsConfig(AppConfig):
    """Configuration class for departments app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.departments'
    verbose_name = 'Təşkilat Strukturu'
