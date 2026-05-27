#!/bin/bash
python manage.py migrate --noinput
python manage.py createcachetable --noinput 2>/dev/null || true
gunicorn thingstor.wsgi:application --workers 4 --threads 2 --timeout 60 --access-logfile -
