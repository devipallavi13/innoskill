#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -o errexit  

# Create and activate a virtual environment
python -m venv venv  
source venv/bin/activate  # Use 'venv/Scripts/activate' for Windows

# Install dependencies
pip install --upgrade pip 
pip install gunicorn 
pip install -r requirements.txt 


# Run Django migrations
python manage.py makemigrations  
python manage.py migrate  

# Collect static files (Render serves them separately)
python manage.py collectstatic --noinput  
