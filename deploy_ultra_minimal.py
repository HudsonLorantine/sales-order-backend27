import os
import zipfile
import shutil

# Create a temporary directory for the deployment package
deploy_dir = 'deploy_temp'
os.makedirs(deploy_dir, exist_ok=True)

# Copy the application file
shutil.copy2('ultra_minimal.py', os.path.join(deploy_dir, 'app.py'))
shutil.copy2('ultra_requirements.txt', os.path.join(deploy_dir, 'requirements.txt'))

# Create startup.sh
with open(os.path.join(deploy_dir, 'startup.sh'), 'w') as f:
    f.write('''#!/bin/bash
echo "Starting ultra minimal application"
cd /home/site/wwwroot
export PORT=${PORT:-8000}
python -m gunicorn --bind=0.0.0.0:$PORT app:app
''')

# Create the deployment zip file
zip_file = 'ultra-minimal-deploy.zip'
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
