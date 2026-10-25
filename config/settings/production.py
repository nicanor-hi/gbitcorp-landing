"""Production settings; deployment must select this module explicitly."""

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403


def required_list(name: str) -> list[str]:
    values = [value.strip() for value in os.getenv(name, "").split(",") if value.strip()]
    if not values:
        raise ImproperlyConfigured(f"Define {name} con valores explícitos para producción.")
    return values


DEBUG = False
ALLOWED_HOSTS = required_list("ALLOWED_HOSTS")
if any(
    host == "*" or host.lower() in {"localhost", "127.0.0.1", "::1", "0.0.0.0"}
    for host in ALLOWED_HOSTS
):
    raise ImproperlyConfigured("ALLOWED_HOSTS debe contener únicamente hosts productivos explícitos.")

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
if any(not origin.startswith("https://") for origin in CSRF_TRUSTED_ORIGINS):
    raise ImproperlyConfigured("CSRF_TRUSTED_ORIGINS debe usar orígenes HTTPS en producción.")

# El proxy frontal debe sobrescribir X-Forwarded-Proto y X-Forwarded-Host;
# aceptar estas cabeceras solo es seguro detrás de un proxy de confianza.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "3600"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
