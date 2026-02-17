# Deploy this Django app on KloudBean

## AttributeError: module 'platform' has no attribute 'system'

If migration or gunicorn fails with this error, the app used to be named `platform`, which shadowed Python’s built-in `platform` module. **This repo now uses the `core` app** instead, so that error should be resolved. Pull the latest code and redeploy.

## Deployment path (fixes many failures)

- **Application root must be the repository root** — where `manage.py`, `bean.conf`, and `requirements.txt` are.
- In KloudBean’s **Deployment Settings**, set **Deployment Path** to the **root** of the cloned repo (leave empty, or `/`, or the path that points to this folder). Do **not** use `django-src` unless your code actually lives in a subfolder named `django-src`.
- For this repo, the clone root **is** the app root. If KloudBean clones into something like `/home/admin/hosted-sites/yourapp/django-src/`, then "django-src" is correct only if that’s where the files are; otherwise point to the parent so that `manage.py` is in the working directory.

## GLIBC_2.32 / GLIBC_2.34 not found

If deployment fails with:

```text
adm: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.32' not found (required by adm)
adm: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.34' not found (required by adm)
```

**What it means:** The environment where the deploy runs has an older GNU C Library than required. Something (KloudBean’s deployment tool or a dependency) was built for a newer Linux (e.g. Ubuntu 22.04).

**What to do:**

1. **Check Deployment Path** (above). Wrong path can sometimes lead to odd errors.
2. **Use this repo’s pinned dependencies** — `requirements.txt` pins Django 4.2.11 and Gunicorn 21.0.0 for better compatibility.
3. **Contact KloudBean support** — Ask for a Django/Python runtime that uses a **newer base image** (glibc 2.32+), or use their recommended “Django” one-click app. The fix is on the host/image side, not in this app’s code.
4. If KloudBean supports **Docker** or a **custom image**, use a image with newer glibc (e.g. `python:3.11-slim` on Debian Bookworm).

## After a successful deploy

1. SSH or use KloudBean’s terminal and go to the app directory.
2. Run: `python manage.py migrate`
3. Run: `python manage.py createsuperuser` (for admin).
4. Set env vars: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `ALLOWED_HOSTS=your-domain.com`.
