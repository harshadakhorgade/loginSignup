from .base import *
import os
import boto3
from botocore.exceptions import ClientError
# Allowed Hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'your-eb-domain.elasticbeanstalk.com,production.eba-nmpz8iig.us-west-2.elasticbeanstalk.com').split(',')


DEBUG = False

def get_ssm_parameter(name):
    """Retrieves a parameter from AWS SSM Parameter Store."""
    client = boto3.client('ssm', region_name=os.getenv('AWS_REGION', 'us-west-2'))
    try:
        response = client.get_parameter(Name=name, WithDecryption=True)
        return response['Parameter']['Value']
    except ClientError as e:
        raise Exception(f"Error retrieving {name} from SSM: {e}")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_ssm_parameter('/myapp/DB_NAME'),
        "USER": get_ssm_parameter('/myapp/DB_USER'),
        "PASSWORD": get_ssm_parameter('/myapp/DB_PASSWORD'),
        "HOST": get_ssm_parameter('/myapp/DB_HOST'),
        "PORT": get_ssm_parameter('/myapp/DB_PORT'),
    }
}





# Fetch region and S3 bucket name from SSM
AWS_REGION = get_ssm_parameter('/myapp/AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = get_ssm_parameter('/myapp/AWS_STORAGE_BUCKET_NAME')

# AWS S3 Configuration
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# Static and Media File Storage
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Security Settings
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True




