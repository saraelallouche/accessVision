# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.middleware import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accessVision.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # d'autres protocoles peuvent être ajoutés ici
    }
)
