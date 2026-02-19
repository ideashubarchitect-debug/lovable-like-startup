#!/usr/bin/env python3
"""
KloudBean: start Gunicorn after fixing stdlib 'platform'.
Run this instead of 'gunicorn' when a leftover platform/ dir shadows the stdlib
and causes: class uri 'gthread' invalid ... AttributeError: module 'platform' has no attribute 'system'

Usage (from app root, e.g. django-src):
  python3 run_gunicorn.py config.wsgi:application
  python3 run_gunicorn.py config.wsgi:application --workers 4 --bind 0.0.0.0:8000
"""
import os
import sys

# Must run before ANY other imports (so gunicorn's workertmp gets the real platform)
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

# Now safe to run Gunicorn
if __name__ == "__main__":
    sys.argv[0] = "gunicorn"
    from gunicorn.app.wsgiapp import run
    sys.exit(run())
