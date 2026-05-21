#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py makemigrations --check --dry-run
python manage.py check --deploy --fail-level ERROR
python manage.py collectstatic --noinput
