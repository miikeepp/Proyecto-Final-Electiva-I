#!/usr/bin/env bash
set -o errexit

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating roles..."
python manage.py crear_roles

echo "Creating or updating superuser from environment..."
python manage.py crear_superusuario_render

echo "Starting Gunicorn..."
python -m gunicorn config.wsgi:application
