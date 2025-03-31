#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.conf import settings

from IAS.utils.general import deep_update, get_settings_from_environment


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IAS.ias.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
    """
        This takes env variables with matching prefix, strips out the prefix, and adds it to global settings.

        For example:
            export PORTFOLIO_SETTINGS_IN_DOCKER=true (environment variable)
            could then be reffered as a global as:
            IN_DOCKER (where then value would be True)
    """
    # global() is a dictionary of global variables
    deep_update(globals(), get_settings_from_environment(settings.ENVVAR_SETTINGS_PREFIX))
