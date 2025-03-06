#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Create a superuser if not already created
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true


