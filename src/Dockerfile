# Python FastAPI/Flask backend Dockerfile example
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose port (adjust if your app uses a different port)
EXPOSE 80

# Start the backend (adjust the command for your framework)
CMD ["python", "main.py"]
