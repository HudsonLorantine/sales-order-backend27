import os
import zipfile
import shutil

# Files to include in the deployment package
files_to_include = [
    'app.py',
    'requirements.txt',
    'startup.sh',
    '.deployment'
]

# Create a temporary directory for the deployment package
deploy_dir = 'deploy_temp'
os.makedirs(deploy_dir, exist_ok=True)

# Copy files to the deployment directory
for file in files_to_include:
    if os.path.exists(file):
        shutil.copy2(file, os.path.join(deploy_dir, file))
    else:
        print(f"Warning: {file} not found, skipping")

# Create the deployment zip file
zip_file = 'simple-deploy.zip'
with zipfile.ZipFile(zip_file, 'w') as zipf:
    for root, dirs, files in os.walk(deploy_dir):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, arcname=os.path.relpath(file_path, deploy_dir))

# Clean up
shutil.rmtree(deploy_dir)

print(f"Deployment package created: {zip_file}")
