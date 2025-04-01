#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginSignup.settings.prod')
    try:
        from loginSignup.settings.prod import BASE_DIR
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # print("BASE_DIR:", BASE_DIR)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
