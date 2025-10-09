from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import template_views

router = DefaultRouter()

app_name = 'notifications'

urlpatterns = [
    # Notification views
    path('inbox/', template_views.inbox, name='inbox'),
    path('<int:pk>/', template_views.notification_detail, name='notification-detail'),
    path('<int:pk>/read/', template_views.mark_as_read, name='mark-as-read'),
    path('mark-all-read/', template_views.mark_all_as_read, name='mark-all-as-read'),
    path('<int:pk>/delete/', template_views.delete_notification, name='delete-notification'),
    path('settings/', template_views.notification_settings, name='settings'),

    # Email template management (admin only)
    path('templates/', template_views.EmailTemplateListView.as_view(), name='email-templates'),
    path('templates/create/', template_views.EmailTemplateCreateView.as_view(), name='email-template-create'),
    path('templates/<int:pk>/', template_views.EmailTemplateDetailView.as_view(), name='email-template-detail'),
    path('templates/<int:pk>/edit/', template_views.EmailTemplateUpdateView.as_view(), name='email-template-edit'),

    # AJAX endpoints
    path('api/unread-count/', template_views.get_unread_count, name='api-unread-count'),
    path('api/recent/', template_views.get_recent_notifications, name='api-recent'),
    path('api/notifications/', template_views.get_recent_notifications, name='api-notifications-list'),

    # API (Router-based endpoints)
    path('api/', include(router.urls)),
]
