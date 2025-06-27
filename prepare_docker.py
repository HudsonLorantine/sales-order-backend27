import os
import shutil

# Create a temporary directory for Docker context
docker_dir = 'docker_context'
os.makedirs(docker_dir, exist_ok=True)

# Copy the files needed for the Docker build
shutil.copy2('ultra_minimal.py', os.path.join(docker_dir, 'ultra_minimal.py'))
shutil.copy2('ultra_requirements.txt', os.path.join(docker_dir, 'ultra_requirements.txt'))
shutil.copy2('Dockerfile-azure', os.path.join(docker_dir, 'Dockerfile'))

print(f"Docker context prepared in '{docker_dir}' directory.")
print("To build and deploy the Docker image, you can use Azure Portal or Docker commands:")
print("1. Navigate to the docker_context directory")
print("2. Build the image: docker build -t sales-api:latest .")
print("3. Tag the image for Azure: docker tag sales-api:latest <your-container-registry>.azurecr.io/sales-api:latest")
print("4. Push to Azure: docker push <your-container-registry>.azurecr.io/sales-api:latest")
print("5. Configure your Azure App Service to use this container image")
