"""
ASGI config for Q360 Evaluation System.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.notifications.routing
import apps.audit.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Combine all WebSocket URL patterns
websocket_urlpatterns = (
    apps.notifications.routing.websocket_urlpatterns +
    apps.audit.routing.websocket_urlpatterns
)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})