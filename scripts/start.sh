#!/usr/bin/env sh
set -eu

python manage.py migrate --noinput

python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model
from django.core.management import call_command
from cms.models import SiteSetting

if not SiteSetting.objects.exists():
    call_command("loaddata", "cms/fixtures/initial_content.json")

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if username and password:
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "is_staff": True, "is_superuser": True},
    )
    if not created and (not user.is_staff or not user.is_superuser):
        user.is_staff = True
        user.is_superuser = True
        user.email = email or user.email
    user.set_password(password)
    user.save()
PY

python manage.py collectstatic --noinput

exec gunicorn sabertech_site.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${WEB_CONCURRENCY:-2}" \
    --timeout "${GUNICORN_TIMEOUT:-60}"
