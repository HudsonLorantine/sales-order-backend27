#!/bin/bash
echo "Starting minimal application"
cd /home/site/wwwroot
export PORT=${PORT:-8000}
gunicorn --bind=0.0.0.0:$PORT --timeout 600 minimal_app:app
