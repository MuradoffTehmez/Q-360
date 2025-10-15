"""
Security utilities and decorators for Q360 system
"""
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from functools import wraps
from django.conf import settings
import re


def rate_limit_api(limit='5/h'):
    """
    Decorator for API rate limiting
    """
    def decorator(view_func):
        @wraps(view_func)
        @ratelimit(key='ip', rate=limit, method='ALL', block=True)
        def _wrapped_view(request, *args, **kwargs):
            # Check if request was limited
            if getattr(request, 'limited', False):
                return JsonResponse({
                    'error': 'Too many requests',
                    'message': 'Please try again later'
                }, status=429)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def login_rate_limit(view_func):
    """
    Decorator for login rate limiting - 5 attempts per hour per IP
    """
    @wraps(view_func)
    @ratelimit(key='ip', rate='5/h', method='POST', block=True)
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'POST' and getattr(request, 'limited', False):
            return JsonResponse({
                'error': 'Too many login attempts',
                'message': 'Account temporarily locked due to multiple failed login attempts. Please try again later.'
            }, status=429)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def api_rate_limit(calls_per_minute=60):
    """
    Rate limit decorator for API endpoints
    """
    def decorator(view_func):
        @wraps(view_func)
        @ratelimit(key='ip', rate=f'{calls_per_minute}/m', method='ALL', block=True)
        def _wrapped_view(request, *args, **kwargs):
            if getattr(request, 'limited', False):
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'message': f'Maximum {calls_per_minute} requests per minute allowed'
                }, status=429)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# Password Strength Validation
class PasswordStrengthValidator:
    """
    Şifrə gücünü yoxlayan validator.

    Tələblər:
    - Minimum 8 simvol
    - Ən az 1 böyük hərf
    - Ən az 1 kiçik hərf
    - Ən az 1 rəqəm
    - Ən az 1 xüsusi simvol (!@#$%^&*()_+-=[]{}|;:,.<>?)
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        """Şifrəni yoxlayır və ValidationError qaytarır."""
        errors = []

        # Minimum uzunluq
        if len(password) < self.min_length:
            errors.append(f'Şifrə ən azı {self.min_length} simvol olmalıdır.')

        # Böyük hərf yoxlaması
        if not re.search(r'[A-Z]', password):
            errors.append('Şifrə ən azı 1 böyük hərf ehtiva etməlidir.')

        # Kiçik hərf yoxlaması
        if not re.search(r'[a-z]', password):
            errors.append('Şifrə ən azı 1 kiçik hərf ehtiva etməlidir.')

        # Rəqəm yoxlaması
        if not re.search(r'\d', password):
            errors.append('Şifrə ən azı 1 rəqəm ehtiva etməlidir.')

        # Xüsusi simvol yoxlaması
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            errors.append('Şifrə ən azı 1 xüsusi simvol ehtiva etməlidir (!@#$%^&* və s.).')

        # Ümumi sözlərin yoxlanması
        common_passwords = ['password', 'qwerty', '12345678', 'admin', 'letmein', 'welcome']
        if password.lower() in common_passwords:
            errors.append('Bu şifrə çox sadədir. Daha güclü bir şifrə seçin.')

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        """Validator üçün kömək mətni qaytarır."""
        return (
            f'Şifrəniz ən azı {self.min_length} simvol uzunluğunda olmalı və '
            'böyük hərf, kiçik hərf, rəqəm və xüsusi simvol ehtiva etməlidir.'
        )


def calculate_password_strength(password):
    """
    Şifrənin gücünü hesablayır və 0-100 arasında bal qaytarır.

    Returns:
        dict: {
            'score': int (0-100),
            'strength': str ('Zəif', 'Orta', 'Güclü', 'Çox Güclü'),
            'feedback': list of str
        }
    """
    score = 0
    feedback = []

    # Uzunluq (max 30 xal)
    length = len(password)
    if length >= 12:
        score += 30
    elif length >= 10:
        score += 20
    elif length >= 8:
        score += 10
    else:
        feedback.append('Şifrə çox qısadır.')

    # Böyük hərflər (max 20 xal)
    uppercase_count = len(re.findall(r'[A-Z]', password))
    if uppercase_count >= 2:
        score += 20
    elif uppercase_count == 1:
        score += 10
    else:
        feedback.append('Böyük hərflər əlavə edin.')

    # Kiçik hərflər (max 20 xal)
    lowercase_count = len(re.findall(r'[a-z]', password))
    if lowercase_count >= 2:
        score += 20
    elif lowercase_count == 1:
        score += 10
    else:
        feedback.append('Kiçik hərflər əlavə edin.')

    # Rəqəmlər (max 15 xal)
    digit_count = len(re.findall(r'\d', password))
    if digit_count >= 2:
        score += 15
    elif digit_count == 1:
        score += 7
    else:
        feedback.append('Rəqəmlər əlavə edin.')

    # Xüsusi simvollar (max 15 xal)
    special_count = len(re.findall(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
    if special_count >= 2:
        score += 15
    elif special_count == 1:
        score += 7
    else:
        feedback.append('Xüsusi simvollar əlavə edin (!@#$% və s.).')

    # Təkrarlanan simvolların cəzası
    if re.search(r'(.)\1{2,}', password):
        score -= 10
        feedback.append('Təkrarlanan simvollardan qaçının.')

    # Ardıcıl simvolların cəzası
    if re.search(r'(abc|bcd|cde|123|234|345|qwe|wer|ert)', password.lower()):
        score -= 10
        feedback.append('Ardıcıl simvollardan qaçının.')

    # Score-u 0-100 arasında saxla
    score = max(0, min(100, score))

    # Güc səviyyəsini müəyyən et
    if score >= 80:
        strength = 'Çox Güclü'
    elif score >= 60:
        strength = 'Güclü'
    elif score >= 40:
        strength = 'Orta'
    else:
        strength = 'Zəif'

    return {
        'score': score,
        'strength': strength,
        'feedback': feedback if score < 80 else ['Əla! Şifrəniz çox güclüdür.']
    }