"""
Security utilities and decorators for Q360 system
"""
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from functools import wraps
from django.conf import settings


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