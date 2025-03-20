#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -o errexit  

# Upgrade pip
pip install --upgrade pip  

# Install dependencies
pip install -r requirements.txt  

# Run Django migrations
python manage.py makemigrations  
python manage.py migrate  

# Collect static files
python manage.py collectstatic --no-input  

# Create a superuser if the environment variable is set
if [[ $CREATE_SUPERUSER ]]; then
  python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi
