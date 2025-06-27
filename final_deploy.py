import os
import zipfile
import shutil

# Create a temporary directory for the deployment package
deploy_dir = 'deploy_temp'
os.makedirs(deploy_dir, exist_ok=True)

# Copy the application file and rename it
shutil.copy2('final_app.py', os.path.join(deploy_dir, 'application.py'))

# Create a minimal requirements.txt
with open(os.path.join(deploy_dir, 'requirements.txt'), 'w') as f:
    f.write('flask==2.0.1\ngunicorn==20.1.0\n')

# Create a web.config file for Azure
with open(os.path.join(deploy_dir, 'web.config'), 'w') as f:
    f.write('''<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <appSettings>
    <add key="WSGI_HANDLER" value="application.app"/>
    <add key="PYTHONPATH" value="%D:\\home\\site\\wwwroot"/>
  </appSettings>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="FastCgiModule" scriptProcessor="%D:\\Python39\\python.exe|%D:\\Python39\\Lib\\site-packages\\wfastcgi.py" resourceType="Unspecified" requireAccess="Script"/>
    </handlers>
  </system.webServer>
</configuration>''')

# Create startup.txt for Azure to recognize
with open(os.path.join(deploy_dir, 'startup.txt'), 'w') as f:
    f.write('gunicorn --bind=0.0.0.0:8000 application:app')

# Create the deployment zip file
zip_file = 'final-deploy.zip'
with zipfile.ZipFile(zip_file, 'w') as zipf:
    for root, dirs, files in os.walk(deploy_dir):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, arcname=os.path.relpath(file_path, deploy_dir))

# Clean up
shutil.rmtree(deploy_dir)

print(f"Deployment package created: {zip_file}")
print("To deploy, use the Azure Portal or Azure CLI:")
print(f"az webapp deploy --resource-group My_SalesSystem --name sales-simple-api --src-path {zip_file} --type zip")
