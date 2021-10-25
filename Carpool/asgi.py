"""
ASGI config for Carpool project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatapp import routing
from .channelsMiddleware import TokenAuthMiddleware
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carpool.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
