"""
URL Configuration for Q360 Evaluation System.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.views.i18n import set_language
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.throttling import AnonRateThrottle
from apps.accounts.template_views import dashboard_view
from apps.notifications.template_views import get_recent_notifications


# Custom throttle for login endpoint
class LoginThrottle(AnonRateThrottle):
    """Throttle for login attempts - 5 per minute."""
    rate = '5/min'


# Throttled Token Obtain View
class ThrottledTokenObtainPairView(TokenObtainPairView):
    """Token Obtain view with throttling for brute-force protection."""
    throttle_classes = [LoginThrottle]

urlpatterns = [
    # Language switcher (must be outside i18n_patterns)
    path('i18n/setlang/', set_language, name='set_language'),

    # Admin Panel
    path('admin/', admin.site.urls),

    # Main pages
    path('', TemplateView.as_view(template_name='landing.html'), name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('help/', TemplateView.as_view(template_name='base/help.html'), name='help'),
    path('privacy/', TemplateView.as_view(template_name='base/privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='base/terms.html'), name='terms'),

    # Authentication
    path('accounts/', include('apps.accounts.urls')),

    # API Authentication
    path('api/auth/token/', ThrottledTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Template-based app URLs (must come FIRST for HTML pages)
    path('evaluations/', include('apps.evaluations.urls', namespace='evaluations')),
    path('departments/', include('apps.departments.urls', namespace='departments')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
    path('development-plans/', include('apps.development_plans.urls', namespace='development-plans')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('competencies/', include(('apps.competencies.urls', 'competencies'), namespace='competencies')),
    path('training/', include(('apps.training.urls', 'training'), namespace='training')),
    path('audit/', include(('apps.audit.urls', 'audit'), namespace='audit')),
    path('search/', include(('apps.search.urls', 'search'), namespace='search')),
    path('workforce-planning/', include(('apps.workforce_planning.urls', 'workforce_planning'), namespace='workforce-planning')),
    path('feedback/', include(('apps.continuous_feedback.urls', 'continuous_feedback'), namespace='feedback')),

    # API endpoints (all under /api/ prefix)
    path('api/notifications/', get_recent_notifications, name='api-notifications'),
    path('api/', include('config.api_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
