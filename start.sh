#!/usr/bin/env bash
set -o errexit
set -o pipefail

PORT="${PORT:-8000}"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating roles..."
python manage.py crear_roles

echo "Creating or updating superuser from environment..."
python manage.py crear_superusuario_render

echo "Starting Gunicorn on port ${PORT}..."
exec python -m gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --log-file - \
  --access-logfile -
