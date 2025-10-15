"""
URL configuration for accounts app.
"""
from django.urls import path
from . import template_views

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

    # User management
    path('users/', template_views.user_list_view, name='user-list'),

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
