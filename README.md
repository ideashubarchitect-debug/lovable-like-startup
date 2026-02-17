# AppForge — Launch Your Own Lovable. Make Money.

**This is the full product.** A Lovable / Replit-style SaaS: users sign up, create "apps" from descriptions, see previews, and get a clear path to deploy. You deploy **this codebase** on KloudBean, rebrand it as your own no-code/app-builder platform, and start charging. You're the CEO. Revenue is yours.

**Pitch:** *Lovable and Replit are worth billions. Run your own version. Deploy on KloudBean. Start making money. Billionaire idea.*

---

## What this product does

- **Landing page** — Bold headline: "Launch your own Lovable or Replit. Start making money." CTA to sign up and pricing.
- **Auth** — Sign up, log in, log out. Email + username.
- **Dashboard** — List of the user's "apps". Button to create a new app.
- **Create app** — Lovable-style: user enters app name + "What do you want to build?" (description). Saves as an app with status "Building".
- **App detail** — Shows app name, description, status. "Preview" link (placeholder page). "Deploy on KloudBean" CTA.
- **Pricing** — Free, Pro ($29/mo), Billionaire (Custom). Template for when you rebrand and set your own prices.

When you deploy this on KloudBean and point a domain at it, you have a live SaaS that you can rebrand and monetize. Your video can show: build this once, deploy on KloudBean, you're running your own Lovable.

---

## Run locally

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- **Landing:** http://127.0.0.1:8000/
- **Sign up / Dashboard:** Create account, then create apps from the dashboard.
- **Admin:** http://127.0.0.1:8000/admin/

---

## Deploy on KloudBean (your video tutorial)

1. **Push to Git** — Push this repo to GitHub/GitLab.
2. **Create app on KloudBean** — Django (or Python) app, choose plan.
3. **Connect repo & deploy** — Deploy → connect repo, set app root to project root (where `manage.py` and `bean.conf` are). Pull & Deploy.
4. **Migrations & superuser** — SSH/Terminal on KloudBean: `python manage.py migrate` and `python manage.py createsuperuser`.
5. **Env vars** — Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `ALLOWED_HOSTS=your-domain.com`.

The product is live. Rebrand the name (AppForge → your brand), point your domain, set your pricing. You're running your own Lovable on KloudBean.

---

## Project structure

```
kloudbean_django/
├── config/           # Django project (settings, urls, wsgi)
├── platform/         # The SaaS app
│   ├── models.py     # App (user, name, description, status)
│   ├── views.py      # landing, auth, dashboard, create_app, app_detail, pricing
│   ├── forms.py      # SignUp, CreateApp
│   └── templates/    # landing, login, signup, dashboard, create_app, app_detail, pricing, preview
├── manage.py
├── requirements.txt
├── bean.conf         # KloudBean: APP_NAME=config.wsgi:application, etc.
└── README.md
```

---

## Why KloudBean

- **One deploy** — Git + `bean.conf`. No complex pipelines.
- **Django-optimized** — Gunicorn, sensible defaults.
- **Your server, your product** — Rebrand this as your own Lovable. Charge users. Scale when you need to.

**Use this repo in your YouTube tutorial:** show the product, deploy it on KloudBean, and pitch "Launch your own Lovable. Make money. Billionaire idea."

- [KloudBean Django Hosting](https://www.kloudbean.com/django-hosting/)
- [KloudBean Deployment Docs](https://support.kloudbean.com/docs/application-deployment/)
