from .base import *
import os
from pathlib import Path  # Ensure you import Path

# ✅ Move BASE_DIR to the top
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Development-specific settings
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Now it works because BASE_DIR is defined first
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Make sure your static folder is at this path
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
