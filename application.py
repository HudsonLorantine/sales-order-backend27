import os
import sys
# Add the directory containing src to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app as application

# This is for Azure App Service
app = application

if __name__ == '__main__':
    # Create database directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'database'), exist_ok=True)
    
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    application.run(host='0.0.0.0', port=port)
