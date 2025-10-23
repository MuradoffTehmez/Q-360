"""
Two-Factor Authentication (2FA) Implementation.
TOTP-based authentication with QR codes and backup codes.
"""
import pyotp
import qrcode
from io import BytesIO
import base64
import secrets
import hashlib
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta


class TwoFactorAuthManager:
    """
    Manager for 2FA operations: setup, verification, backup codes.
    """

    @staticmethod
    def generate_secret():
        """
        Generate a new TOTP secret for user.

        Returns:
            str: Base32 encoded secret
        """
        return pyotp.random_base32()

    @staticmethod
    def generate_provisioning_uri(user, secret):
        """
        Generate provisioning URI for QR code.

        Args:
            user: User instance
            secret: TOTP secret

        Returns:
            str: Provisioning URI
        """
        totp = pyotp.TOTP(secret)
        issuer_name = getattr(settings, 'COMPANY_NAME', 'Q360')

        return totp.provisioning_uri(
            name=user.email,
            issuer_name=issuer_name
        )

    @staticmethod
    def generate_qr_code(provisioning_uri):
        """
        Generate QR code image for TOTP setup.

        Args:
            provisioning_uri: URI for QR code

        Returns:
            str: Base64 encoded QR code image
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{img_str}"

    @staticmethod
    def verify_token(secret, token):
        """
        Verify TOTP token.

        Args:
            secret: User's TOTP secret
            token: 6-digit token from authenticator app

        Returns:
            bool: True if token is valid
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)  # Allow 1 window (30 seconds)

    @staticmethod
    def generate_backup_codes(count=10):
        """
        Generate backup codes for account recovery.

        Args:
            count: Number of backup codes to generate

        Returns:
            list: List of backup codes
        """
        codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = secrets.token_hex(4).upper()
            # Format as XXXX-XXXX
            formatted_code = f"{code[:4]}-{code[4:]}"
            codes.append(formatted_code)

        return codes

    @staticmethod
    def hash_backup_code(code):
        """
        Hash backup code for secure storage.

        Args:
            code: Plain backup code

        Returns:
            str: Hashed code
        """
        # Remove dashes and convert to lowercase
        clean_code = code.replace('-', '').lower()
        return hashlib.sha256(clean_code.encode()).hexdigest()

    @staticmethod
    def verify_backup_code(stored_hash, provided_code):
        """
        Verify backup code against stored hash.

        Args:
            stored_hash: Stored hash of backup code
            provided_code: User-provided code

        Returns:
            bool: True if code matches
        """
        provided_hash = TwoFactorAuthManager.hash_backup_code(provided_code)
        return secrets.compare_digest(stored_hash, provided_hash)

    @staticmethod
    def is_2fa_required(user):
        """
        Check if 2FA is required for user.

        Args:
            user: User instance

        Returns:
            bool: True if 2FA required
        """
        # Check user's 2FA status
        if hasattr(user, 'two_factor_enabled') and user.two_factor_enabled:
            return True

        # Check if role requires 2FA
        if user.is_superadmin() or user.is_admin():
            return getattr(settings, '2FA_REQUIRED_FOR_ADMINS', True)

        return False

    @staticmethod
    def create_2fa_session(user, request):
        """
        Create temporary 2FA verification session.

        Args:
            user: User instance
            request: HTTP request

        Returns:
            str: Session token
        """
        session_token = secrets.token_urlsafe(32)
        cache_key = f'2fa_session:{session_token}'

        session_data = {
            'user_id': user.id,
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'created_at': timezone.now().isoformat()
        }

        # Store for 10 minutes
        cache.set(cache_key, session_data, 600)

        return session_token

    @staticmethod
    def verify_2fa_session(session_token):
        """
        Verify 2FA session token.

        Args:
            session_token: Session token

        Returns:
            dict or None: Session data if valid
        """
        cache_key = f'2fa_session:{session_token}'
        return cache.get(cache_key)

    @staticmethod
    def complete_2fa_session(session_token):
        """
        Mark 2FA session as completed and remove from cache.

        Args:
            session_token: Session token
        """
        cache_key = f'2fa_session:{session_token}'
        cache.delete(cache_key)

    @staticmethod
    def rate_limit_2fa_attempts(user_id, max_attempts=5, window_minutes=15):
        """
        Rate limit 2FA verification attempts.

        Args:
            user_id: User ID
            max_attempts: Maximum attempts allowed
            window_minutes: Time window in minutes

        Returns:
            tuple: (allowed: bool, attempts_left: int)
        """
        cache_key = f'2fa_attempts:{user_id}'
        attempts = cache.get(cache_key, 0)

        if attempts >= max_attempts:
            return False, 0

        # Increment attempts
        cache.set(cache_key, attempts + 1, window_minutes * 60)

        return True, max_attempts - attempts - 1

    @staticmethod
    def reset_2fa_attempts(user_id):
        """Reset 2FA attempt counter."""
        cache_key = f'2fa_attempts:{user_id}'
        cache.delete(cache_key)


class TwoFactorBackupCode:
    """
    Model-like helper for backup codes.
    Stores hashed backup codes in user profile.
    """

    @staticmethod
    def generate_for_user(user):
        """
        Generate and save backup codes for user.

        Args:
            user: User instance

        Returns:
            list: Plain text backup codes (show once!)
        """
        codes = TwoFactorAuthManager.generate_backup_codes()

        # Hash codes for storage
        hashed_codes = [
            {
                'code': TwoFactorAuthManager.hash_backup_code(code),
                'used': False,
                'created_at': timezone.now().isoformat()
            }
            for code in codes
        ]

        # Store in user profile
        if hasattr(user, 'profile'):
            user.profile.two_factor_backup_codes = hashed_codes
            user.profile.save()

        return codes  # Return plain codes (show only once!)

    @staticmethod
    def verify_and_consume(user, code):
        """
        Verify backup code and mark as used.

        Args:
            user: User instance
            code: Backup code

        Returns:
            bool: True if valid and unused
        """
        if not hasattr(user, 'profile') or not user.profile.two_factor_backup_codes:
            return False

        backup_codes = user.profile.two_factor_backup_codes

        for backup in backup_codes:
            if backup['used']:
                continue

            if TwoFactorAuthManager.verify_backup_code(backup['code'], code):
                # Mark as used
                backup['used'] = True
                backup['used_at'] = timezone.now().isoformat()
                user.profile.two_factor_backup_codes = backup_codes
                user.profile.save()
                return True

        return False

    @staticmethod
    def get_remaining_count(user):
        """
        Get count of unused backup codes.

        Args:
            user: User instance

        Returns:
            int: Count of unused codes
        """
        if not hasattr(user, 'profile') or not user.profile.two_factor_backup_codes:
            return 0

        return sum(1 for code in user.profile.two_factor_backup_codes if not code['used'])


# Utility functions
def generate_2fa_setup_data(user):
    """
    Generate all data needed for 2FA setup.

    Args:
        user: User instance

    Returns:
        dict: Setup data including QR code, secret, backup codes
    """
    secret = TwoFactorAuthManager.generate_secret()
    provisioning_uri = TwoFactorAuthManager.generate_provisioning_uri(user, secret)
    qr_code = TwoFactorAuthManager.generate_qr_code(provisioning_uri)
    backup_codes = TwoFactorAuthManager.generate_backup_codes()

    return {
        'secret': secret,
        'qr_code': qr_code,
        'provisioning_uri': provisioning_uri,
        'backup_codes': backup_codes,
        'manual_entry_key': secret
    }


def enable_2fa_for_user(user, secret, backup_codes):
    """
    Enable 2FA for user after verification.

    Args:
        user: User instance
        secret: TOTP secret
        backup_codes: List of backup codes
    """
    # Update user profile
    if hasattr(user, 'profile'):
        user.profile.two_factor_enabled = True
        user.profile.two_factor_secret = secret

        # Hash and store backup codes
        hashed_codes = [
            {
                'code': TwoFactorAuthManager.hash_backup_code(code),
                'used': False,
                'created_at': timezone.now().isoformat()
            }
            for code in backup_codes
        ]
        user.profile.two_factor_backup_codes = hashed_codes
        user.profile.save()

    # Log this security event
    from apps.audit.models import AuditLog
    AuditLog.objects.create(
        user=user,
        action='2fa_enabled',
        model_name='Profile',
        severity='info',
        context={'method': 'TOTP'}
    )


def disable_2fa_for_user(user):
    """
    Disable 2FA for user.

    Args:
        user: User instance
    """
    if hasattr(user, 'profile'):
        user.profile.two_factor_enabled = False
        user.profile.two_factor_secret = None
        user.profile.two_factor_backup_codes = []
        user.profile.save()

    # Log this security event
    from apps.audit.models import AuditLog
    AuditLog.objects.create(
        user=user,
        action='2fa_disabled',
        model_name='Profile',
        severity='warning',
        context={'method': 'manual'}
    )
