#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    # Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UPMS.settings')

    try:
        # Import the execute_from_command_line function from Django's management module.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute Django management commands with the command-line arguments.
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

