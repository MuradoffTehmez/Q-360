"""
Encryption helpers built on top of Fernet.
"""
from __future__ import annotations

import base64
import hashlib
from typing import Optional

from django.conf import settings

try:
    from cryptography.fernet import Fernet, InvalidToken  # type: ignore

    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    Fernet = None  # type: ignore
    InvalidToken = Exception  # type: ignore
    CRYPTOGRAPHY_AVAILABLE = False


class EncryptionUnavailable(RuntimeError):
    """Raised when cryptography dependency is missing."""


def get_encryption_key(raw_key: Optional[str | bytes] = None) -> bytes:
    """
    Produce a Fernet-compatible key derived from the provided raw key or settings.
    """
    if raw_key is None:
        raw_key = getattr(settings, "DATA_ENCRYPTION_KEY", None) or settings.SECRET_KEY

    if isinstance(raw_key, str):
        raw_key = raw_key.encode("utf-8")

    digest = hashlib.sha256(raw_key).digest()
    return base64.urlsafe_b64encode(digest)


def _get_fernet(key: Optional[str | bytes] = None):
    if not CRYPTOGRAPHY_AVAILABLE:
        raise EncryptionUnavailable(
            "cryptography package is required for encryption utilities. "
            "Install with `pip install cryptography` or set DATA_ENCRYPTION_KEY to disable usage."
        )
    return Fernet(get_encryption_key(key))


def encrypt_value(value: str, *, key: Optional[str | bytes] = None) -> str:
    """
    Encrypt a string and return a token.
    """
    value_bytes = value.encode("utf-8")
    token = _get_fernet(key).encrypt(value_bytes)
    return token.decode("utf-8")


def decrypt_value(token: str, *, key: Optional[str | bytes] = None) -> str:
    """
    Decrypt a token previously produced by ``encrypt_value``.
    """
    decrypted = _get_fernet(key).decrypt(token.encode("utf-8"))
    return decrypted.decode("utf-8")
