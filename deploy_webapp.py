#!/usr/bin/env python3
"""
Deploy Sales Order Backend as Azure Web App
"""

import subprocess
import sys
import json

def run_command(cmd, check=True):
    """Run command and return result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def main():
    # Configuration
    resource_group = "sales-order-rg"
    app_name = "sales-order-backend-app"
    location = "eastus2"
    sku = "B1"  # Basic plan for cost efficiency
    
    print("Deploying Sales Order Backend as Azure Web App...")
    
    # Create App Service Plan
    print("\n1. Creating App Service Plan...")
    run_command(f"""
        az appservice plan create \
            --name {app_name}-plan \
            --resource-group {resource_group} \
            --location {location} \
            --sku {sku} \
            --is-linux
    """)
    
    # Create Web App
    print("\n2. Creating Web App...")
    run_command(f"""
        az webapp create \
            --name {app_name} \
            --resource-group {resource_group} \
            --plan {app_name}-plan \
            --runtime "PYTHON:3.11"
    """)
    
    # Configure startup command
    print("\n3. Configuring startup command...")
    run_command(f"""
        az webapp config set \
            --name {app_name} \
            --resource-group {resource_group} \
            --startup-file "python startup.py"
    """)
    
    # Set application settings
    print("\n4. Setting application settings...")
    run_command(f"""
        az webapp config appsettings set \
            --name {app_name} \
            --resource-group {resource_group} \
            --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true ENABLE_ORYX_BUILD=true
    """)
    
    # Deploy code
    print("\n5. Deploying code...")
    run_command(f"""
        az webapp up \
            --name {app_name} \
            --resource-group {resource_group} \
            --plan {app_name}-plan \
            --runtime "PYTHON:3.11" \
            --sku {sku}
    """)
    
    # Get the URL
    print("\n6. Getting application URL...")
    result = run_command(f"""
        az webapp show \
            --name {app_name} \
            --resource-group {resource_group} \
            --query "defaultHostName" \
            --output tsv
    """)
    
    backend_url = f"https://{result.stdout.strip()}"
    print(f"\n✅ Backend deployed successfully!")
    print(f"🌐 Backend URL: {backend_url}")
    print(f"📊 API Base URL: {backend_url}/api")
    print(f"\nTest endpoints:")
    print(f"  - {backend_url}/api/orders")
    print(f"  - {backend_url}/api/customers")
    print(f"  - {backend_url}/api/products")
    
    return backend_url

if __name__ == "__main__":
    backend_url = main()
    
    # Save backend URL for frontend configuration
    with open("backend_url.txt", "w") as f:
        f.write(backend_url)
    
    print(f"\n🔗 Backend URL saved to backend_url.txt")
    print(f"📝 Next step: Update frontend to use {backend_url}/api")
