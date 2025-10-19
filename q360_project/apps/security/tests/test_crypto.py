from django.test import TestCase
from unittest import skipUnless

from apps.security.crypto import (
    CRYPTOGRAPHY_AVAILABLE,
    decrypt_value,
    encrypt_value,
    get_encryption_key,
)


@skipUnless(CRYPTOGRAPHY_AVAILABLE, "cryptography not installed")
class CryptoUtilsTests(TestCase):
    def test_encrypt_decrypt_roundtrip(self):
        key = get_encryption_key("test-key")
        token = encrypt_value("secret-data", key=key)
        self.assertNotEqual(token, "secret-data")
        decrypted = decrypt_value(token, key=key)
        self.assertEqual(decrypted, "secret-data")
