"""
WSGI config for KloudBean Django project.
Exposed as application for KloudBean (bean.conf APP_NAME).
"""
import os
import sys

# Ensure stdlib 'platform' is used (leftover platform/ on server would break Django)
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

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
