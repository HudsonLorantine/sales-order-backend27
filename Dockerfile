FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements-min.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY minimal_app.py app.py

# Port is configurable via environment variable
ENV PORT=8000

# Configure for Azure App Service
ENV WEBSITE_HOSTNAME=0.0.0.0
EXPOSE $PORT

# Start with increased timeout for Azure cold starts
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 120 --access-logfile - --error-logfile - app:app
