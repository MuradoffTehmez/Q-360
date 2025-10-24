"""
URL configuration for accounts app.
"""
from django.urls import path
from . import template_views, two_factor_views

app_name = 'accounts'

# Template-based URLs only - API endpoints are in config/api_urls.py
urlpatterns = [
    # Authentication
    path('login/', template_views.login_view, name='login'),
    path('logout/', template_views.logout_view, name='logout'),
    path('register/', template_views.register_view, name='register'),

    # Profile
    path('profile/', template_views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', template_views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('settings/', template_views.ProfileUpdateView.as_view(), name='settings'),
    path('security/', template_views.security_settings, name='security'),
    path('mfa-verify/', template_views.mfa_verify, name='mfa-verify'),
    path('mfa-initiate/', template_views.mfa_initiate, name='mfa-initiate'),
    path('mfa-disable/', template_views.mfa_disable, name='mfa-disable'),
    path('mfa-backup-regenerate/', template_views.mfa_backup_regenerate, name='mfa-backup-regenerate'),
    path('sessions-terminate-all/', template_views.sessions_terminate_all, name='sessions-terminate-all'),

    # Two-Factor Authentication (2FA)
    path('2fa/setup/', two_factor_views.setup_2fa_view, name='2fa_setup'),
    path('2fa/verify/', two_factor_views.verify_2fa_view, name='2fa_verify'),
    path('2fa/disable/', two_factor_views.disable_2fa_view, name='2fa_disable'),
    path('2fa/backup-codes/', two_factor_views.backup_codes_view, name='2fa_backup_codes'),
    path('2fa/status/', two_factor_views.check_2fa_status, name='2fa_status'),

    # User management
    path('users/', template_views.user_list_view, name='user-list'),
    path('users/create/', template_views.user_create_view, name='user-create'),
    path('rbac/', template_views.rbac_matrix_view, name='rbac-matrix'),

    # Password reset
    path('password-reset/', template_views.password_reset_request, name='password-reset'),
    path('password-reset/done/', template_views.password_reset_done, name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', template_views.password_reset_confirm, name='password-reset-confirm'),
    path('password-reset/complete/', template_views.password_reset_complete, name='password-reset-complete'),

    # Password change (for logged in users)
    path('change-password/', template_views.change_password, name='change-password'),

    # Setup wizard
    path('setup-wizard/', template_views.setup_wizard_view, name='setup-wizard'),
    path('complete-setup/', template_views.complete_setup, name='complete-setup'),
]
