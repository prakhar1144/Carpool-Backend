#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# This command is needed only once.
# python manage.py createsuperuser --email prakhar1144@gmail.com --no-input
