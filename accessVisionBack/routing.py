from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path('ws/some_path/$', consumers.YourConsumer.as_asgi()),
]