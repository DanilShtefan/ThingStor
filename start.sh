#!/bin/bash
python manage.py migrate --noinput
DJANGO_SUPERUSER_PASSWORD=$SUPERUSER_PASSWORD python manage.py createsuperuser \
  --username $SUPERUSER_USERNAME --email $SUPERUSER_EMAIL --noinput 2>/dev/null || true
gunicorn thingstor.wsgi:application --workers 4 --threads 2 --timeout 60 --access-logfile -
