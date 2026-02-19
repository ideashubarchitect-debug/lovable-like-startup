# Deploy this Django app on KloudBean

This project is aligned with [KloudBean Django deployment docs](https://support.kloudbean.com/docs/application-deployment/deploying-django): `bean.conf` format (`APP_NAME=<project-folder>.wsgi:application`, `APP_DIR=/`, `WORKERS`), `.env` variables (`APP_URL`, `DB_HOST`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`), and code in `django-src`.

## Error: class uri 'gthread' invalid ... AttributeError: module 'platform' has no attribute 'system'

Gunicorn can hit this when a leftover **platform/** directory on the server shadows the stdlib. Fix: (1) **Remove the dir** — SSH and run `rm -rf /home/admin/hosted-sites/kb_ulwo8n34lt/django-src/platform`, then restart. (2) **Use the wrapper** — If KloudBean allows a custom start command, run `python3 run_gunicorn.py config.wsgi:application` (see **run_gunicorn.py** in the repo); it patches `platform` before Gunicorn loads.

## AttributeError: module 'platform' has no attribute 'system' (manage.py / migrate)

If migration or gunicorn fails with this error (without the gthread line), the app used to be named `platform`, which shadowed Python’s built-in `platform` module. **This repo now uses the `core` app** instead, so that error should be resolved. In addition, `manage.py` and `config/wsgi.py` now force the stdlib `platform` into `sys.modules` at startup, so a leftover `platform/` dir on the server won't break. Pull the latest code and redeploy. If it still fails, remove the leftover dir via SSH: `rm -rf .../django-src/platform`.

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

## Module not found / Dependency missing from packages

If the build fails with **"Module not found"** or **"Dependency is missing from packages"**:

1. **All required packages are in `requirements.txt`** — Django, gunicorn, asgiref, sqlparse, tzdata. Ensure KloudBean runs **`pip install -r requirements.txt`** from the **app directory** (the folder that contains `requirements.txt` and `manage.py`). If your deploy path is `django-src`, that directory must contain `requirements.txt` and the install must run from there.
2. **If the missing module is `config` or `core`** — The app must run with the **project root as the current working directory** (so that `config` and `core` are importable). In KloudBean, the **Application directory** / **Working directory** for Gunicorn should be the same directory that contains `manage.py`, `config/`, and `core/`. Do not run from a parent or subdirectory.
3. **Clean rebuild** — If a previous deploy left a broken venv, try a clean deploy (or remove the app’s virtualenv on the server and redeploy) so `pip install -r requirements.txt` runs again from scratch.

## 502 Bad Gateway (app URL shows nginx 502)

Nginx returns 502 when it can't get a valid response from Gunicorn. Check: (1) **Process Manager** — Gunicorn/Django process is running; restart if needed. (2) **Application / Error logs** — look for Python tracebacks. (3) Run **migrations** via SSH/terminal: `python manage.py migrate`. (4) **ALLOWED_HOSTS** — this repo now allows `.kloudbeansite.com` by default. (5) **Database** — if using SQLite, app directory must be writable for `db.sqlite3`.

## After a successful deploy

1. SSH or use KloudBean’s terminal and go to the app directory.
2. Go to the app directory (path from deployment logs, e.g. `cd /home/admin/hosted-sites/kb_ulwo8n34lt/django-src`).
3. Use **python3** (not `python`). Run: `python3 manage.py migrate`
4. Run: `python3 manage.py createsuperuser` (for admin).
5. Set env vars: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `ALLOWED_HOSTS=your-domain.com`.
