"""
Two-Factor Authentication Views.
Handles 2FA setup, verification, and management.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from apps.accounts.two_factor import (
    TwoFactorAuthManager,
    TwoFactorBackupCode,
    generate_2fa_setup_data,
    enable_2fa_for_user,
    disable_2fa_for_user
)
from apps.audit.models import AuditLog


@login_required
@require_http_methods(["GET", "POST"])
def setup_2fa_view(request):
    """
    Setup 2FA for user account.
    GET: Display QR code and manual entry key
    POST: Verify token and enable 2FA
    """
    user = request.user

    # Check if 2FA already enabled
    if hasattr(user, 'profile') and user.profile.two_factor_enabled:
        messages.info(request, 'İki faktorlu autentifikasiya artıq aktiv edilib.')
        return redirect('accounts:profile')

    if request.method == 'POST':
        token = request.POST.get('token', '').strip()
        secret = request.session.get('2fa_setup_secret')
        backup_codes = request.session.get('2fa_setup_backup_codes')

        if not secret or not backup_codes:
            messages.error(request, 'Sessiya müddəti bitib. Yenidən cəhd edin.')
            return redirect('accounts:2fa_setup')

        # Verify token
        if TwoFactorAuthManager.verify_token(secret, token):
            # Enable 2FA
            enable_2fa_for_user(user, secret, backup_codes)

            # Clear session data
            request.session.pop('2fa_setup_secret', None)
            request.session.pop('2fa_setup_backup_codes', None)

            # Mark 2FA as verified in session
            request.session['2fa_verified'] = True
            request.session['2fa_verified_at'] = timezone.now().isoformat()

            messages.success(request, 'İki faktorlu autentifikasiya uğurla aktiv edildi!')

            # Store backup codes to show once
            request.session['show_backup_codes'] = backup_codes

            return redirect('accounts:2fa_backup_codes')
        else:
            messages.error(request, 'Yanlış kod. Zəhmət olmasa yenidən cəhd edin.')
            AuditLog.objects.create(
                user=user,
                action='2fa_setup_failed',
                model_name='Profile',
                severity='warning',
                context={'reason': 'invalid_token'}
            )

    # GET request - generate setup data
    setup_data = generate_2fa_setup_data(request.user)

    # Store in session for verification
    request.session['2fa_setup_secret'] = setup_data['secret']
    request.session['2fa_setup_backup_codes'] = setup_data['backup_codes']

    context = {
        'qr_code': setup_data['qr_code'],
        'manual_entry_key': setup_data['manual_entry_key'],
        'company_name': getattr(settings, 'COMPANY_NAME', 'Q360'),
    }

    return render(request, 'accounts/2fa/setup.html', context)


@require_http_methods(["GET", "POST"])
def verify_2fa_view(request):
    """
    Verify 2FA token during login.
    """
    # Check if user is authenticated but 2FA not verified
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = request.user

    # Check if 2FA already verified
    if request.session.get('2fa_verified'):
        next_url = request.session.pop('2fa_next', None)
        return redirect(next_url or 'dashboard:index')

    # Check if 2FA is required
    if not TwoFactorAuthManager.is_2fa_required(user):
        return redirect('dashboard:index')

    if request.method == 'POST':
        token = request.POST.get('token', '').strip()
        use_backup_code = request.POST.get('use_backup_code') == 'true'

        # Rate limiting
        allowed, attempts_left = TwoFactorAuthManager.rate_limit_2fa_attempts(user.id)

        if not allowed:
            messages.error(
                request,
                'Çox sayda uğursuz cəhd. 15 dəqiqə gözləyib yenidən cəhd edin.'
            )
            AuditLog.objects.create(
                user=user,
                action='2fa_rate_limited',
                model_name='Profile',
                severity='warning',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return render(request, 'accounts/2fa/verify.html', {
                'rate_limited': True,
                'attempts_left': 0
            })

        verified = False

        if use_backup_code:
            # Verify backup code
            verified = TwoFactorBackupCode.verify_and_consume(user, token)
            method = 'backup_code'
        else:
            # Verify TOTP token
            if hasattr(user, 'profile') and user.profile.two_factor_secret:
                verified = TwoFactorAuthManager.verify_token(
                    user.profile.two_factor_secret,
                    token
                )
            method = 'totp'

        if verified:
            # Mark session as 2FA verified
            request.session['2fa_verified'] = True
            request.session['2fa_verified_at'] = timezone.now().isoformat()

            # Reset rate limit attempts
            TwoFactorAuthManager.reset_2fa_attempts(user.id)

            # Log success
            AuditLog.objects.create(
                user=user,
                action='2fa_verified',
                model_name='Profile',
                severity='info',
                context={'method': method},
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, 'İki faktorlu autentifikasiya uğurla təsdiqləndi!')

            # Redirect to intended page
            next_url = request.session.pop('2fa_next', None)
            return redirect(next_url or 'dashboard:index')
        else:
            messages.error(
                request,
                f'Yanlış kod. {attempts_left} cəhd qalıb.'
            )
            AuditLog.objects.create(
                user=user,
                action='2fa_verify_failed',
                model_name='Profile',
                severity='warning',
                context={'method': method, 'attempts_left': attempts_left},
                ip_address=request.META.get('REMOTE_ADDR')
            )

    # GET request or failed POST
    remaining_codes = TwoFactorBackupCode.get_remaining_count(user)

    context = {
        'remaining_backup_codes': remaining_codes,
    }

    return render(request, 'accounts/2fa/verify.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def disable_2fa_view(request):
    """
    Disable 2FA for user account.
    Requires password confirmation.
    """
    user = request.user

    # Check if 2FA is enabled
    if not hasattr(user, 'profile') or not user.profile.two_factor_enabled:
        messages.info(request, 'İki faktorlu autentifikasiya aktiv deyil.')
        return redirect('accounts:profile')

    if request.method == 'POST':
        password = request.POST.get('password')

        # Verify password
        if not user.check_password(password):
            messages.error(request, 'Yanlış şifrə.')
            return render(request, 'accounts/2fa/disable.html')

        # Disable 2FA
        disable_2fa_for_user(user)

        # Clear 2FA session
        request.session.pop('2fa_verified', None)
        request.session.pop('2fa_verified_at', None)

        messages.success(request, 'İki faktorlu autentifikasiya deaktiv edildi.')
        return redirect('accounts:profile')

    return render(request, 'accounts/2fa/disable.html')


@login_required
@require_http_methods(["GET", "POST"])
def backup_codes_view(request):
    """
    Display or regenerate backup codes.
    """
    user = request.user

    # Check if 2FA is enabled
    if not hasattr(user, 'profile') or not user.profile.two_factor_enabled:
        messages.error(request, 'İki faktorlu autentifikasiya aktiv deyil.')
        return redirect('accounts:profile')

    # Check if showing codes from setup
    show_codes = request.session.pop('show_backup_codes', None)

    if request.method == 'POST':
        # Regenerate backup codes
        password = request.POST.get('password')

        # Verify password
        if not user.check_password(password):
            messages.error(request, 'Yanlış şifrə.')
            return render(request, 'accounts/2fa/backup_codes.html', {
                'regenerate': True
            })

        # Generate new backup codes
        new_codes = TwoFactorBackupCode.generate_for_user(user)

        AuditLog.objects.create(
            user=user,
            action='2fa_backup_codes_regenerated',
            model_name='Profile',
            severity='info',
            ip_address=request.META.get('REMOTE_ADDR')
        )

        messages.success(request, 'Yeni backup kodlar yaradıldı.')

        context = {
            'backup_codes': new_codes,
            'show_codes': True,
            'remaining_codes': len(new_codes)
        }
    else:
        # Show existing backup codes info
        remaining_codes = TwoFactorBackupCode.get_remaining_count(user)

        context = {
            'backup_codes': show_codes,
            'show_codes': show_codes is not None,
            'remaining_codes': remaining_codes,
            'regenerate': False
        }

    return render(request, 'accounts/2fa/backup_codes.html', context)


@login_required
@require_http_methods(["GET"])
def check_2fa_status(request):
    """
    API endpoint to check 2FA status.
    """
    user = request.user

    if hasattr(user, 'profile'):
        enabled = user.profile.two_factor_enabled
        enabled_at = user.profile.two_factor_enabled_at
        remaining_backup_codes = TwoFactorBackupCode.get_remaining_count(user)
    else:
        enabled = False
        enabled_at = None
        remaining_backup_codes = 0

    return JsonResponse({
        'enabled': enabled,
        'enabled_at': enabled_at.isoformat() if enabled_at else None,
        'remaining_backup_codes': remaining_backup_codes,
        'required': TwoFactorAuthManager.is_2fa_required(user),
        'session_verified': request.session.get('2fa_verified', False)
    })
