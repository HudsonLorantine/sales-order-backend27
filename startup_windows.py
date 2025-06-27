import os
import sys
import subprocess

print("Starting Windows deployment script...")

# Print environment for debugging
print(f"Working directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")
print(f"Python version: {sys.version}")

# Get port from environment or use default
port = os.environ.get('PORT', '8000')
print(f"Using port: {port}")

# Install requirements
print("Installing requirements...")
subprocess.call([sys.executable, "-m", "pip", "install", "-r", "azure_requirements.txt"])

# Run the application
print("Starting application...")
sys.path.insert(0, os.getcwd())
from azure_app import app
app.run(host='0.0.0.0', port=int(port))
