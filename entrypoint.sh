#!/bin/sh
set -e

# Run migrations and collect static files, then start Gunicorn.
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Listen on PORT env var (Back4App sets this); default to 8000
: ${PORT:=8000}

exec gunicorn jobportal.wsgi:application --bind 0.0.0.0:${PORT} --workers 3
