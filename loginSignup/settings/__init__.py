import os

ENVIRONMENT = os.getenv("DJANGO_ENV", "dev")  # Default to dev

if ENVIRONMENT == "prod":
    from .prod import *
elif ENVIRONMENT == "test":
    from .test import *
else:
    from .dev import *
