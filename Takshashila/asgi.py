import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from classes import consumers
from django.urls import re_path, path

ws_patterns = [
    re_path(r"ws/(?P<room_name>\w+)/(?P<name>\w+)/$", consumers.RoomConsumer.as_asgi()),
    path("<str:room_name>/<str:name>", consumers.RoomConsumer.as_asgi())
]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Takshashila.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ws_patterns
        )
    )
})
