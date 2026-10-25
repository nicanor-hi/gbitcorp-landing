"""Windows-friendly local development settings."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

from .base import *  # noqa: F403,E402

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "[::1]"]
WAGTAILADMIN_BASE_URL = os.getenv("WAGTAILADMIN_BASE_URL", "http://127.0.0.1:8000")
