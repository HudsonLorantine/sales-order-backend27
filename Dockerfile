FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create database directory
RUN mkdir -p src/database

# Port is configurable via environment variable
ENV PORT=8000
ENV PYTHONPATH=/app

# Configure for Azure App Service
ENV WEBSITE_HOSTNAME=0.0.0.0
EXPOSE $PORT

# Start with gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 120 --access-logfile - --error-logfile - src.main:app
