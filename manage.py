#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# KloudBean fix: ensure stdlib 'platform' is used (server may have leftover platform/ dir
# that shadows it and breaks uuid.py -> AttributeError: module 'platform' has no attribute 'system')
_orig_path = list(sys.path)
_shadowing = [p for p in _orig_path if p and (
    os.path.exists(os.path.join(os.path.abspath(p), "platform", "__init__.py"))
    or os.path.isfile(os.path.join(os.path.abspath(p), "platform.py"))
)]
for p in _shadowing:
    sys.path.remove(p)
import platform as _stdlib_platform
sys.modules["platform"] = _stdlib_platform
for p in reversed(_shadowing):
    sys.path.insert(0, p)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
