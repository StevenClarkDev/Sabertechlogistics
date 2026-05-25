# Saber Tech Logistics

Django 6.0.5 rebuild of the Saber Tech Logistics website with CMS-managed pages, navigation, team members, site settings, and contact submissions through Django Admin.

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata cms/fixtures/initial_content.json
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the website and `http://127.0.0.1:8000/admin/` for the CMS admin panel.

## Deployment Settings

Set these environment variables on the server:

```text
DJANGO_SECRET_KEY=replace-with-a-secure-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=sabertechlogistics.com,www.sabertechlogistics.com,.appdomain.cloud
DJANGO_CSRF_TRUSTED_ORIGINS=https://sabertechlogistics.com,https://www.sabertechlogistics.com,https://*.appdomain.cloud
```

Run `python manage.py collectstatic` during deployment.
