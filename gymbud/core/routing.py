from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat import urls

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            urls.websocket_urlpatterns
        )
    ),
})