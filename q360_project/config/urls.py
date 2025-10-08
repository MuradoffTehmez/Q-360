"""
URL Configuration for Q360 Evaluation System.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from apps.accounts.template_views import dashboard_view

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Main pages
    path('', dashboard_view, name='dashboard'),
    path('help/', TemplateView.as_view(template_name='base/help.html'), name='help'),
    path('privacy/', TemplateView.as_view(template_name='base/privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='base/terms.html'), name='terms'),

    # Authentication
    path('accounts/', include('apps.accounts.urls')),

    # API Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API URLs
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/departments/', include('apps.departments.urls')),
    path('api/evaluations/', include('apps.evaluations.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/development-plans/', include('apps.development_plans.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/audit/', include('apps.audit.urls')),

    # Template-based app URLs
    path('evaluations/', include('apps.evaluations.urls', namespace='evaluations')),
    path('departments/', include('apps.departments.urls', namespace='departments')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
    path('development-plans/', include('apps.development_plans.urls', namespace='development-plans')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
