"""WSGI entrypoint for the project."""

import os

from django.core.wsgi import get_wsgi_application

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    raise RuntimeError("Define DJANGO_SETTINGS_MODULE explícitamente para WSGI.")

application = get_wsgi_application()
