#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn Djoker.wsgi:application --bind 0.0.0.0:8000