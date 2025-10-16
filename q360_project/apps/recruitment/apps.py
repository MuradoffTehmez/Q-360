"""App configuration for recruitment app."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecruitmentConfig(AppConfig):
    """Configuration for the Recruitment & ATS app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.recruitment'
    verbose_name = _('İşə Qəbul və İzləmə')
