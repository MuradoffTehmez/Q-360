"""App configuration for leave and attendance app."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LeaveAttendanceConfig(AppConfig):
    """Configuration for the Leave & Attendance Management app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.leave_attendance'
    verbose_name = _('Məzuniyyət və İştirak')
