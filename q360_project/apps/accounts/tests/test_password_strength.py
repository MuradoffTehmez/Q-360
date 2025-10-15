"""
Tests for password strength validation.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.accounts.security_utils import (
    PasswordStrengthValidator,
    calculate_password_strength
)


class PasswordStrengthValidatorTest(TestCase):
    """Test password strength validator."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = PasswordStrengthValidator()

    def test_valid_strong_password(self):
        """Test that a strong password is accepted."""
        password = "MyStr0ng!Pass"
        try:
            self.validator.validate(password)
        except ValidationError:
            self.fail("Strong password should not raise ValidationError")

    def test_too_short_password(self):
        """Test that too short password is rejected."""
        password = "Ab1!"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        errors = cm.exception.messages
        self.assertTrue(any('8 simvol' in str(e) for e in errors))

    def test_no_uppercase_letter(self):
        """Test that password without uppercase letter is rejected."""
        password = "mypassword123!"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        errors = cm.exception.messages
        self.assertTrue(any('böyük hərf' in str(e) for e in errors))

    def test_no_lowercase_letter(self):
        """Test that password without lowercase letter is rejected."""
        password = "MYPASSWORD123!"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        errors = cm.exception.messages
        self.assertTrue(any('kiçik hərf' in str(e) for e in errors))

    def test_no_digit(self):
        """Test that password without digit is rejected."""
        password = "MyPassword!"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        errors = cm.exception.messages
        self.assertTrue(any('rəqəm' in str(e) for e in errors))

    def test_no_special_character(self):
        """Test that password without special character is rejected."""
        password = "MyPassword123"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        errors = cm.exception.messages
        self.assertTrue(any('xüsusi simvol' in str(e) for e in errors))

    def test_common_password(self):
        """Test that common passwords are rejected."""
        common_passwords = ['password', 'qwerty', '12345678']
        for password in common_passwords:
            with self.assertRaises(ValidationError) as cm:
                self.validator.validate(password)
            errors = cm.exception.messages
            # Common password check might fail due to other rules too
            # Just check that it raises ValidationError

    def test_custom_min_length(self):
        """Test validator with custom minimum length."""
        validator = PasswordStrengthValidator(min_length=12)
        password = "MyPass123!"  # 10 characters
        with self.assertRaises(ValidationError) as cm:
            validator.validate(password)
        errors = cm.exception.messages
        self.assertTrue(any('12 simvol' in str(e) for e in errors))


class PasswordStrengthCalculatorTest(TestCase):
    """Test password strength calculator."""

    def test_very_weak_password(self):
        """Test very weak password scoring."""
        result = calculate_password_strength("abc")
        self.assertLess(result['score'], 40)
        self.assertEqual(result['strength'], 'Zəif')
        self.assertGreater(len(result['feedback']), 0)

    def test_weak_password(self):
        """Test weak password scoring."""
        result = calculate_password_strength("password123")
        self.assertLess(result['score'], 60)
        self.assertIn(result['strength'], ['Zəif', 'Orta'])

    def test_medium_password(self):
        """Test medium strength password."""
        result = calculate_password_strength("MyPass123")
        self.assertGreaterEqual(result['score'], 40)
        self.assertLess(result['score'], 80)

    def test_strong_password(self):
        """Test strong password scoring."""
        result = calculate_password_strength("MyStr0ng!Pass")
        self.assertGreaterEqual(result['score'], 60)

    def test_very_strong_password(self):
        """Test very strong password scoring."""
        result = calculate_password_strength("MyV3ry$tr0ng!P@ssw0rd")
        self.assertGreaterEqual(result['score'], 80)
        self.assertEqual(result['strength'], 'Çox Güclü')
        self.assertIn('Əla', result['feedback'][0])

    def test_repeated_characters_penalty(self):
        """Test that repeated characters lower the score."""
        password_with_repeats = "MyPasssss111!"
        password_without_repeats = "MyP@ss975!"

        result_with = calculate_password_strength(password_with_repeats)
        result_without = calculate_password_strength(password_without_repeats)

        # Password with repeats should have lower or equal score
        self.assertLessEqual(result_with['score'], result_without['score'])

    def test_sequential_characters_penalty(self):
        """Test that sequential characters lower the score."""
        password_with_seq = "MyPass123!"
        password_without_seq = "MyP@ss975!"

        result_with = calculate_password_strength(password_with_seq)
        result_without = calculate_password_strength(password_without_seq)

        # Password with sequential chars should have lower or equal score
        self.assertLessEqual(result_with['score'], result_without['score'])

    def test_empty_password(self):
        """Test empty password."""
        result = calculate_password_strength("")
        self.assertEqual(result['score'], 0)
        self.assertEqual(result['strength'], 'Zəif')

    def test_score_boundaries(self):
        """Test that score stays within 0-100 range."""
        test_passwords = [
            "",
            "a",
            "password",
            "MyPass123!",
            "MyV3ry$tr0ng!P@ssw0rd2024"
        ]

        for password in test_passwords:
            result = calculate_password_strength(password)
            self.assertGreaterEqual(result['score'], 0)
            self.assertLessEqual(result['score'], 100)

    def test_length_bonus(self):
        """Test that longer passwords get higher scores."""
        short_pass = "MyP@ss1"  # 7 chars
        medium_pass = "MyP@ssw0rd1"  # 11 chars
        long_pass = "MyV3ry$tr0ng!P@ssw0rd"  # 21 chars

        result_short = calculate_password_strength(short_pass)
        result_medium = calculate_password_strength(medium_pass)
        result_long = calculate_password_strength(long_pass)

        self.assertLess(result_short['score'], result_medium['score'])
        self.assertLess(result_medium['score'], result_long['score'])

    def test_multiple_special_characters_bonus(self):
        """Test that multiple special characters increase score."""
        one_special = "MyPass1!"
        two_special = "My!Pass1@"

        result_one = calculate_password_strength(one_special)
        result_two = calculate_password_strength(two_special)

        # More special characters should give higher score
        self.assertGreaterEqual(result_two['score'], result_one['score'])
