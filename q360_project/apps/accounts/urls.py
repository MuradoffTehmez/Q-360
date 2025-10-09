"""
URL configuration for accounts app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet, RoleViewSet
from . import template_views

router = DefaultRouter()
router.register(r'api/users', UserViewSet, basename='user')
router.register(r'api/profiles', ProfileViewSet, basename='profile')
router.register(r'api/roles', RoleViewSet, basename='role')

app_name = 'accounts'

urlpatterns = [
    # Template views
    path('login/', template_views.login_view, name='login'),
    path('logout/', template_views.logout_view, name='logout'),
    path('register/', template_views.register_view, name='register'),
    path('profile/', template_views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', template_views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('users/', template_views.user_list_view, name='user-list'),
    path('settings/', template_views.ProfileUpdateView.as_view(), name='settings'),
    path('security/', template_views.security_settings, name='security'),

    # Password reset
    path('password-reset/', template_views.password_reset_request, name='password-reset'),
    path('password-reset/done/', template_views.password_reset_done, name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', template_views.password_reset_confirm, name='password-reset-confirm'),
    path('password-reset/complete/', template_views.password_reset_complete, name='password-reset-complete'),

    # API routes
    path('', include(router.urls)),
]
