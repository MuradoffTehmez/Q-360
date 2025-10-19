import time

from django.db.models.signals import post_save
from django.test import TestCase

from apps.accounts.mfa import generate_base32_secret, generate_totp_code, generate_backup_codes, verify_totp_code
from apps.accounts.models import User
from apps.onboarding.signals import ensure_onboarding_process


class MFATests(TestCase):
    def setUp(self):
        post_save.disconnect(ensure_onboarding_process, sender=User)
        self.addCleanup(lambda: post_save.connect(ensure_onboarding_process, sender=User))

        self.user = User.objects.create_user(
            username="mfa-user",
            password="pass1234",
            role="employee",
        )

    def test_totp_generation_and_verification(self):
        secret = generate_base32_secret()
        config = self.user.ensure_mfa_config()
        config.secret = secret
        config.save(update_fields=["secret", "updated_at"])

        code = generate_totp_code(secret, timestamp=time.time())
        self.assertTrue(verify_totp_code(secret, code))
        self.assertFalse(verify_totp_code(secret, "000000"))

    def test_backup_codes_storage_and_validation(self):
        config = self.user.ensure_mfa_config()
        codes = generate_backup_codes(count=3, length=6)
        config.set_backup_codes(codes)
        config.save()

        self.assertTrue(config.verify_backup_code(codes[0]))
        self.assertFalse(config.verify_backup_code(codes[0]))  # Already used
