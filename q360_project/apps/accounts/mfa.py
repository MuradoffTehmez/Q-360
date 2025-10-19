"""
Utility helpers for Time-based One-Time Password (TOTP) verification.
"""
from __future__ import annotations

import base64
import hmac
import hashlib
import secrets
import time
from typing import Iterable, List


def generate_base32_secret(length: int = 20) -> str:
    """
    Generate a random base32 secret key.
    """
    random_bytes = secrets.token_bytes(length)
    return base64.b32encode(random_bytes).decode("utf-8").rstrip("=")


def _normalise_secret(secret: str) -> bytes:
    padding = "=" * ((8 - len(secret) % 8) % 8)
    return base64.b32decode(secret.upper() + padding, casefold=True)


def generate_totp_code(secret: str, timestamp: float | None = None, *, interval: int = 30, digits: int = 6) -> str:
    """
    Generate a TOTP code using RFC 6238 (SHA1).
    """
    timestamp = timestamp or time.time()
    counter = int(timestamp // interval)
    key = _normalise_secret(secret)
    msg = counter.to_bytes(8, "big")
    hmac_digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = hmac_digest[-1] & 0x0F
    code = (
        int.from_bytes(hmac_digest[offset : offset + 4], "big") & 0x7FFFFFFF
    ) % (10**digits)
    return str(code).zfill(digits)


def verify_totp_code(secret: str, code: str, *, interval: int = 30, digits: int = 6, window: int = 1) -> bool:
    """
    Validate an incoming TOTP code.
    """
    code = str(code or "").strip()
    if not code.isdigit():
        return False

    timestamp = time.time()
    for offset in range(-window, window + 1):
        candidate_time = timestamp + (offset * interval)
        if generate_totp_code(secret, candidate_time, interval=interval, digits=digits) == code:
            return True
    return False


def generate_backup_codes(*, count: int = 5, length: int = 10) -> List[str]:
    """
    Generate human-friendly backup codes.
    """
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    codes: List[str] = []
    for _ in range(count):
        codes.append("".join(secrets.choice(alphabet) for _ in range(length)))
    return codes
