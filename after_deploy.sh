#!/bin/bash
source /opt/python/run/venv/bin/activate
source /opt/python/current/env
cd /opt/python/current/app
echo "Current directory: $PWD"
echo "Running Django migrations..."
python manage.py migrate 
echo "Migrations complete!"
