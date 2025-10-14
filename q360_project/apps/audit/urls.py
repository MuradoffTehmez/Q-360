from django.urls import path
from . import template_views

app_name = 'audit'

# Template-based URLs only - API endpoints would be in config/api_urls.py if needed
urlpatterns = [
    path('security/', template_views.security_dashboard, name='security-dashboard'),
]
