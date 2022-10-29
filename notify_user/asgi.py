"""
ASGI config for notify_user project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from main.consumers import NotificationConsumer
from user_app.consumers import NotificationConsumers
from django.urls import re_path,path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notify_user.settings')
django.setup() 
# application = get_asgi_application()

from channels.auth import AuthMiddleware, AuthMiddlewareStack
from user_app.routing import websocket_urlpatterns
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
