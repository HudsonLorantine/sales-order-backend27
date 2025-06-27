FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY ultra_requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ultra_minimal.py /app/app.py

# Configure for Azure App Service
ENV PORT=8000
ENV WEBSITES_PORT=8000

# Expose the port
EXPOSE 8000

# Start the application with gunicorn
CMD gunicorn --bind 0.0.0.0:8000 app:app
