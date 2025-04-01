from .base import *
import boto3

# Enable debugging for staging
DEBUG = True

# AWS SSM Parameter Store
ssm = boto3.client("ssm", region_name="your-region")

def get_ssm_parameter(name, decrypt=True):
    response = ssm.get_parameter(Name=name, WithDecryption=decrypt)
    return response["Parameter"]["Value"]

# Fetch credentials securely from AWS SSM
SECRET_KEY = get_ssm_parameter("/django/staging/secret_key")  # Different key for staging

# Allow staging domain and local testing
ALLOWED_HOSTS = ["staging.yourdomain.com", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_ssm_parameter("/django/staging/db/name"),
        'USER': get_ssm_parameter("/django/staging/db/user"),
        'PASSWORD': get_ssm_parameter("/django/staging/db/password"),
        'HOST': get_ssm_parameter("/django/staging/db/host"),
        'PORT': get_ssm_parameter("/django/staging/db/port"),
    }
}

# Security settings (relaxed for testing)
SECURE_SSL_REDIRECT = False  # No forced HTTPS in staging
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
