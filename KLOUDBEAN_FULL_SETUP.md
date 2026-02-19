# KloudBean – Full deployment setup and credentials

**⚠️ SECURITY:** This file contains live credentials. Do not commit it to a public repository. Add to `.gitignore` or store in a secure place.

---

## Step 1: Credentials and configuration (reference for Cursor / deployment)

Use these when configuring the app, `.env`, or KloudBean panel. **Build and deploy this project for KloudBean with Python 3.10** (see Step 3).

| Item | Value |
|------|--------|
| **App URL** | https://django-642200409.kloudbeansite.com/ |
| **App system user** | ideashubarchitect@gmail.com |
| **DB user** | kb_ulwo8n34lt |
| **DB password** | 9RK3FXh8jSoazDq5T7 |
| **DB name** | kb_ulwo8n34lt |
| **KloudBean SSH command** | `ssh admin_0ls3z4o3bndb@52.14.249.148` |

**App directory on server (after SSH):**  
`/home/admin/hosted-sites/kb_ulwo8n34lt/django-src`

**Python on KloudBean (from KB panel):** **Python 3.10** — all dependencies and tooling must target Python 3.10.

---

## Step 2: Production environment (.env)

Set these in **KloudBean → Application → Environment variables** (or in a `.env` file on the server, if supported). Do not commit `.env` with real values.

```env
# Django
DJANGO_SECRET_KEY=your-strong-secret-key-min-50-chars
DJANGO_DEBUG=False
ALLOWED_HOSTS=django-642200409.kloudbeansite.com,.kloudbeansite.com,localhost,127.0.0.1

# Database (KloudBean MySQL – use values from Step 1)
DB_ENGINE=mysql
DB_NAME=kb_ulwo8n34lt
DB_USER=kb_ulwo8n34lt
DB_PASSWORD=9RK3FXh8jSoazDq5T7
DB_HOST=localhost
DB_PORT=3306
```

If KloudBean provides a single **DATABASE_URL**, set that instead and ensure `config/settings.py` reads it (see project settings).

---

## Step 3: Python and dependency versions (critical for KloudBean)

- **Python:** KloudBean hosts this app with **Python 3.10** (confirm in KloudBean panel). The project must run on **Python 3.10**.
- **Cursor / local build:** When editing or building this project for KloudBean, assume **Python 3.10**. Use `runtime.txt` (e.g. `python-3.10`) and ensure all packages support Python 3.10.
- **Dependencies:** Keep `requirements.txt` compatible with Python 3.10. Test with `python3.10 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`.

---

## Step 4: bean.conf (KloudBean)

The repo’s `bean.conf` is set for KloudBean:

- **APP_NAME** = `config.wsgi:application` (Django WSGI entry point)
- **APP_DIR** = `/` (app root where `manage.py` lives)
- **WORKERS** = 4 (Gunicorn workers)

No change needed unless KloudBean or your plan requires different values.

---

## Step 5: After deploy – SSH and commands

1. Connect:
   ```bash
   ssh admin_0ls3z4o3bndb@52.14.249.148
   ```
2. Go to app directory:
   ```bash
   cd /home/admin/hosted-sites/kb_ulwo8n34lt/django-src
   ```
3. Use **python3** (or the venv Python). Run migrations:
   ```bash
   python3 manage.py migrate
   python3 manage.py createsuperuser
   ```

---

## Prompt for Cursor / AI

When asking Cursor (or any AI) to work on this project for KloudBean:

- **Host:** KloudBean; **App URL:** https://django-642200409.kloudbeansite.com/
- **Python:** 3.10 (from KloudBean panel) – build and validate for Python 3.10.
- **Credentials and paths:** Use the values in **Step 1** and **Step 2** of this file for configuration and `.env`.
- **Deployment:** Use `bean.conf` in the repo; app directory on server is `django-src` under the hosted-sites path above.
