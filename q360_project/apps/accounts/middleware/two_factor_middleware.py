"""
Two-Factor Authentication Middleware.
Enforces 2FA verification for protected endpoints.
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings


class TwoFactorAuthMiddleware:
    """
    Middleware to enforce 2FA for authenticated users.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # URLs that don't require 2FA
        self.exempt_urls = [
            '/accounts/login/',
            '/accounts/logout/',
            '/accounts/2fa/setup/',
            '/accounts/2fa/verify/',
            '/accounts/2fa/backup-code/',
            '/static/',
            '/media/',
            '/health/',
        ]

        # URLs that always require 2FA
        self.protected_urls = [
            '/admin/',
            '/api/',
            '/dashboard/',
        ]

    def __call__(self, request):
        # Skip if user not authenticated
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Skip exempt URLs
        if any(request.path.startswith(url) for url in self.exempt_urls):
            return self.get_response(request)

        # Check if 2FA is required for this user
        if self._is_2fa_required(request.user):
            # Check if 2FA is verified in this session
            if not request.session.get('2fa_verified', False):
                return self._redirect_to_2fa_verification(request)

        response = self.get_response(request)
        return response

    def _is_2fa_required(self, user):
        """
        Check if 2FA is required for user.
        """
        # Check user's 2FA status
        if hasattr(user, 'profile') and user.profile.two_factor_enabled:
            return True

        # Require 2FA for admins and superadmins
        if user.is_superadmin() or user.is_admin():
            require_for_admins = getattr(settings, '2FA_REQUIRED_FOR_ADMINS', True)
            if require_for_admins:
                return True

        return False

    def _redirect_to_2fa_verification(self, request):
        """
        Redirect to 2FA verification page.
        """
        # Store intended URL
        request.session['2fa_next'] = request.path

        # Check if it's an API request
        if request.path.startswith('/api/'):
            return JsonResponse({
                'error': '2FA verification required',
                'message': 'İki faktorlu autentifikasiya tələb olunur',
                'redirect_url': reverse('accounts:2fa_verify')
            }, status=401)
        else:
            return redirect('accounts:2fa_verify')


class Session2FAMiddleware:
    """
    Middleware to manage 2FA session timeout.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout_minutes = getattr(settings, '2FA_SESSION_TIMEOUT', 60)  # 60 minutes default

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if 2FA session has expired
            if request.session.get('2fa_verified'):
                verified_at = request.session.get('2fa_verified_at')

                if verified_at:
                    from django.utils import timezone
                    from datetime import timedelta
                    import datetime

                    # Parse timestamp
                    if isinstance(verified_at, str):
                        verified_at = datetime.datetime.fromisoformat(verified_at)

                    elapsed = timezone.now() - verified_at
                    timeout = timedelta(minutes=self.timeout_minutes)

                    # Session expired
                    if elapsed > timeout:
                        request.session['2fa_verified'] = False
                        request.session.pop('2fa_verified_at', None)

        response = self.get_response(request)
        return response
