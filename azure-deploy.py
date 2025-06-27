import os
import zipfile
import shutil

# Files to include in the deployment package
files_to_include = [
    'minimal_app.py',
    'requirements-min.txt',
    '.deployment'
]

# Create a temporary directory for the deployment package
deploy_dir = 'deploy_temp'
os.makedirs(deploy_dir, exist_ok=True)

# Create special files for Azure
with open(os.path.join(deploy_dir, 'web.config'), 'w') as f:
    f.write('''<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <appSettings>
    <add key="PYTHONPATH" value="D:\\home\\site\\wwwroot"/>
    <add key="WSGI_HANDLER" value="minimal_app.app"/>
    <add key="WSGI_LOG" value="D:\\home\\LogFiles\\wfastcgi.log"/>
  </appSettings>
  <system.webServer>
    <httpPlatform processPath="%PYTHONPATH%\\python.exe" arguments="-m gunicorn --bind=0.0.0.0:%HTTP_PLATFORM_PORT% minimal_app:app" requestTimeout="00:04:00" startupTimeLimit="120" startupRetryCount="3" stdoutLogEnabled="true" stdoutLogFile="D:\\home\\LogFiles\\python.log"/>
  </system.webServer>
</configuration>''')

# Create startup.sh
with open(os.path.join(deploy_dir, 'startup.sh'), 'w') as f:
    f.write('''#!/bin/bash
echo "Starting application with gunicorn"
cd /home/site/wwwroot
export PORT=${PORT:-8000}
gunicorn --bind=0.0.0.0:$PORT --timeout 120 --access-logfile - --error-logfile - minimal_app:app''')

# Copy or rename files to the deployment directory
for file in files_to_include:
    if os.path.exists(file):
        shutil.copy2(file, os.path.join(deploy_dir, file))
        # Rename minimal_app.py to app.py in the deployment directory
        if file == 'minimal_app.py':
            # Also keep original for web.config reference
            shutil.copy2(file, os.path.join(deploy_dir, 'app.py'))
        if file == 'requirements-min.txt':
            shutil.copy2(file, os.path.join(deploy_dir, 'requirements.txt'))
    else:
        print(f"Warning: {file} not found, skipping")

# Add a readme with deployment instructions
with open(os.path.join(deploy_dir, 'README.md'), 'w') as f:
    f.write('''# Flask API Deployment to Azure App Service

This package contains a simple Flask API for deployment to Azure App Service.

## Deployment Steps

1. Deploy this zip file to Azure App Service using the Azure Portal or CLI
2. Configure the App Service to use Python 3.9
3. Set the startup command to: `gunicorn --bind=0.0.0.0:$PORT minimal_app:app`
4. Enable Application Logging for troubleshooting

## API Endpoints

- `/` - Homepage with API information
- `/api/health` - Health check endpoint with system information
- `/api/orders` - Sample orders data''')

# Create the deployment zip file
zip_file = 'azure-webapp-deploy.zip'
with zipfile.ZipFile(zip_file, 'w') as zipf:
    for root, dirs, files in os.walk(deploy_dir):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, arcname=os.path.relpath(file_path, deploy_dir))

# Clean up
shutil.rmtree(deploy_dir)

print(f"Deployment package created: {zip_file}")
print("To deploy, use the Azure CLI command:")
print(f"az webapp deploy --resource-group My_SalesSystem --name sales-simple-api --src-path {zip_file} --type zip")
