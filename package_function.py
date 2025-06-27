import os
import zipfile
import shutil

# Create a temporary directory for the deployment package
deploy_dir = 'function_temp'
os.makedirs(deploy_dir, exist_ok=True)

# Copy the required files
shutil.copy2('function_app.py', os.path.join(deploy_dir, 'function_app.py'))
shutil.copy2('function_requirements.txt', os.path.join(deploy_dir, 'requirements.txt'))
shutil.copy2('host.json', os.path.join(deploy_dir, 'host.json'))

# Create the deployment zip file
zip_file = 'function-deploy.zip'
with zipfile.ZipFile(zip_file, 'w') as zipf:
    for root, dirs, files in os.walk(deploy_dir):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, arcname=os.path.relpath(file_path, deploy_dir))

# Clean up
shutil.rmtree(deploy_dir)

print(f"Azure Function deployment package created: {zip_file}")
print("To deploy, create an Azure Function App and upload this zip package.")
