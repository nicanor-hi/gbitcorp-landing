"""ASGI entrypoint for the project."""

import os

from django.core.asgi import get_asgi_application

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    raise RuntimeError("Define DJANGO_SETTINGS_MODULE explícitamente para ASGI.")

application = get_asgi_application()
