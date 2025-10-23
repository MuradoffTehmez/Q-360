"""
Advanced Rate Limiting Middleware for Q360.
IP-based, user-based, and endpoint-specific rate limiting.
"""
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
import time
import hashlib
from functools import wraps


class RateLimitMiddleware:
    """
    Global rate limiting middleware.
    Applies different rate limits based on endpoint and user status.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Rate limit configurations
        self.rate_limits = {
            'login': {'limit': 5, 'window': 300},  # 5 attempts per 5 minutes
            'api': {'limit': 60, 'window': 60},  # 60 requests per minute
            'general': {'limit': 100, 'window': 60},  # 100 requests per minute
        }

    def __call__(self, request):
        # Skip rate limiting for authenticated superusers
        if request.user.is_authenticated and request.user.is_superuser:
            return self.get_response(request)

        # Determine rate limit type
        limit_type = self._get_limit_type(request.path)

        # Check rate limit
        if not self._check_rate_limit(request, limit_type):
            return self._rate_limit_exceeded_response(request)

        response = self.get_response(request)
        return response

    def _get_limit_type(self, path):
        """Determine which rate limit to apply based on path."""
        if '/accounts/login' in path or '/api/token' in path:
            return 'login'
        elif path.startswith('/api/'):
            return 'api'
        else:
            return 'general'

    def _get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _get_cache_key(self, request, limit_type):
        """Generate cache key for rate limiting."""
        ip = self._get_client_ip(request)
        user_id = request.user.id if request.user.is_authenticated else 'anon'
        key_parts = [
            'ratelimit',
            limit_type,
            str(user_id),
            ip,
            str(int(time.time() // self.rate_limits[limit_type]['window']))
        ]
        return hashlib.md5(':'.join(key_parts).encode()).hexdigest()

    def _check_rate_limit(self, request, limit_type):
        """Check if request exceeds rate limit."""
        config = self.rate_limits[limit_type]
        cache_key = self._get_cache_key(request, limit_type)

        # Get current count
        current_count = cache.get(cache_key, 0)

        if current_count >= config['limit']:
            return False

        # Increment counter
        cache.set(cache_key, current_count + 1, config['window'])
        return True

    def _rate_limit_exceeded_response(self, request):
        """Return rate limit exceeded response."""
        if request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'Rate limit exceeded',
                'message': 'Çox sayda sorğu göndərildi. Zəhmət olmasa bir az gözləyin.',
                'retry_after': 60
            }, status=429)
        else:
            return HttpResponse(
                '<h1>429 - Çox Sayda Sorğu</h1>'
                '<p>Siz çox sayda sorğu göndərmisiniz. Zəhmət olmasa bir neçə dəqiqə gözləyin.</p>',
                status=429
            )


def rate_limit_exempt(view_func):
    """
    Decorator to exempt a view from rate limiting.
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.rate_limit_exempt = True
    return wrapped_view


class AdvancedRateLimiter:
    """
    Advanced rate limiter with sliding window algorithm.
    """

    @staticmethod
    def check_rate_limit(identifier, max_requests, window_seconds):
        """
        Check rate limit using sliding window algorithm.

        Args:
            identifier: Unique identifier (user_id, ip, etc.)
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds

        Returns:
            tuple: (allowed: bool, remaining: int, reset_time: int)
        """
        cache_key = f'rate_limit:sliding:{identifier}'
        current_time = time.time()
        window_start = current_time - window_seconds

        # Get timestamps from cache
        timestamps = cache.get(cache_key, [])

        # Remove old timestamps
        timestamps = [ts for ts in timestamps if ts > window_start]

        # Check if limit exceeded
        allowed = len(timestamps) < max_requests
        remaining = max(0, max_requests - len(timestamps))

        if allowed:
            # Add new timestamp
            timestamps.append(current_time)
            cache.set(cache_key, timestamps, window_seconds)

        # Calculate reset time
        if timestamps:
            oldest_timestamp = min(timestamps)
            reset_time = int(oldest_timestamp + window_seconds)
        else:
            reset_time = int(current_time + window_seconds)

        return allowed, remaining, reset_time


# Decorators for specific endpoints
def login_rate_limit(func):
    """Rate limit for login endpoints - 5 attempts per 5 minutes."""
    @wraps(func)
    @ratelimit(key='ip', rate='5/5m', method=['POST'], block=True)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def api_rate_limit(func):
    """Rate limit for API endpoints - 60 requests per minute."""
    @wraps(func)
    @ratelimit(key='user_or_ip', rate='60/m', method=['GET', 'POST', 'PUT', 'DELETE'], block=True)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def strict_rate_limit(func):
    """Strict rate limit - 10 requests per minute."""
    @wraps(func)
    @ratelimit(key='ip', rate='10/m', method=['POST'], block=True)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class TokenBucketRateLimiter:
    """
    Token bucket algorithm implementation for rate limiting.
    More flexible than fixed windows.
    """

    def __init__(self, capacity, refill_rate):
        """
        Initialize token bucket.

        Args:
            capacity: Maximum number of tokens (requests)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate

    def consume(self, identifier, tokens=1):
        """
        Try to consume tokens from bucket.

        Args:
            identifier: Unique identifier
            tokens: Number of tokens to consume

        Returns:
            bool: True if tokens consumed successfully
        """
        cache_key = f'token_bucket:{identifier}'
        bucket_data = cache.get(cache_key)

        current_time = time.time()

        if bucket_data is None:
            # Initialize bucket
            bucket_data = {
                'tokens': self.capacity,
                'last_update': current_time
            }
        else:
            # Refill tokens based on time elapsed
            time_elapsed = current_time - bucket_data['last_update']
            new_tokens = time_elapsed * self.refill_rate
            bucket_data['tokens'] = min(
                self.capacity,
                bucket_data['tokens'] + new_tokens
            )
            bucket_data['last_update'] = current_time

        # Try to consume tokens
        if bucket_data['tokens'] >= tokens:
            bucket_data['tokens'] -= tokens
            cache.set(cache_key, bucket_data, 3600)  # Cache for 1 hour
            return True
        else:
            return False


# Rate limit handler for django-ratelimit
def ratelimit_handler(request, exception):
    """
    Custom handler for rate limit exceeded.
    """
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Rate limit exceeded',
            'message': 'Çox sayda sorğu göndərildi. Zəhmət olmasa gözləyin.',
            'details': {
                'limit': exception.rate,
                'method': exception.method
            }
        }, status=429)
    else:
        from django.shortcuts import render
        return render(request, 'errors/429.html', status=429)
