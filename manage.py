#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Load .env from project root so "manage.py migrate" etc. use same DB as the app (MySQL on KloudBean).
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.isfile(_env_path):
    with open(_env_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                k, v = k.strip(), v.strip()
                if k:
                    os.environ.setdefault(k, v)

# KloudBean fix: if a leftover platform/ PACKAGE (dir with __init__.py) shadows stdlib,
# remove only that path so "import platform" gets the real one. Do NOT remove paths
# that only have platform.py (that's the stdlib).
_orig_path = list(sys.path)
_shadowing = [p for p in _orig_path if p and os.path.exists(
    os.path.join(os.path.abspath(p), "platform", "__init__.py")
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
