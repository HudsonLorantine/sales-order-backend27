#!/bin/bash
echo "Starting deployment script..."

# Print environment for debugging
echo "Working directory: $(pwd)"
echo "Directory contents: $(ls -la)"
echo "Python version: $(python --version)"

# Change to the application directory
cd /home/site/wwwroot
echo "Changed to wwwroot directory: $(pwd)"

# Create database directory if it doesn't exist
mkdir -p src/database
echo "Created database directory"

# Debug: List environment variables
echo "Environment variables:"
env | sort

# Get port from environment or use default
export PORT=${PORT:-8000}
echo "Using port: $PORT"

# Install requirements
echo "Installing requirements..."
pip install -r azure_requirements.txt

# Start the application
echo "Starting application..."
gunicorn --bind=0.0.0.0:$PORT --timeout 600 azure_app:app
