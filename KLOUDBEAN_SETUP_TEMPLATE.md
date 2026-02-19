# KloudBean setup template (no secrets)

Copy this to `KLOUDBEAN_FULL_SETUP.md` and fill in your real values from the KloudBean panel. Use that file as the single reference for Cursor and deployment.

---

## Step 1: Credentials and configuration

| Item | Value (fill from KB panel) |
|------|----------------------------|
| **App URL** | https://YOUR-APP.kloudbeansite.com/ |
| **App system user** | your@email.com |
| **DB user** | from KloudBean DB users |
| **DB password** | from KloudBean |
| **DB name** | from KloudBean |
| **KloudBean SSH command** | `ssh user@host` from KB panel |

**App directory on server:** `/home/admin/hosted-sites/YOUR_APP_ID/django-src`  
**Python on KloudBean:** Check in KB panel (e.g. **Python 3.10**). Build and test for this version.

---

## Step 2: Production .env

Set in KloudBean → Environment variables (or server `.env`):

- `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `ALLOWED_HOSTS=your-app.kloudbeansite.com,.kloudbeansite.com`
- `DB_ENGINE=mysql`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

See `.env.example` in the repo.

---

## Step 3: Python version

Use the **exact Python version** shown in the KloudBean panel (e.g. 3.10). The repo has `runtime.txt` with `python-3.10`. When asking Cursor to build or fix things, specify: "This app is deployed on KloudBean with Python 3.10; use that version."

---

## Step 4: bean.conf

The repo `bean.conf` is set for KloudBean: `APP_NAME=config.wsgi:application`, `APP_DIR=/`, `WORKERS=4`. No change unless KB requires different values.
