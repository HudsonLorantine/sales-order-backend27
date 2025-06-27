#!/usr/bin/env python3
"""
Ultra simple deployment using Azure CLI only
"""

import subprocess
import sys
import zipfile
import os

def run_command(cmd):
    """Run command and show output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def create_deployment_zip():
    """Create a zip file for deployment"""
    print("📦 Creating deployment package...")
    
    # Files to include in deployment
    files_to_include = [
        'src/',
        'requirements.txt',
        'startup.py',
        'host.json'
    ]
    
    with zipfile.ZipFile('deployment.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in files_to_include:
            if os.path.isfile(item):
                zipf.write(item)
                print(f"Added file: {item}")
            elif os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
                        print(f"Added file: {file_path}")
    
    print("✅ Deployment package created: deployment.zip")
    return True

def main():
    # Simple configuration
    resource_group = "sales-order-rg"
    app_name = "sales-order-backend-simple"
    storage_account = "salesorderstorage27"
    location = "eastus2"
    
    print("🚀 Simple Backend Deployment...")
    
    # Method 1: Try Function App with consumption plan
    print("\n🔄 Trying Function App deployment...")
    
    print("1. Creating storage account...")
    run_command(f"""
        az storage account create \
            --name {storage_account} \
            --resource-group {resource_group} \
            --location {location} \
            --sku Standard_LRS
    """)
    
    print("2. Creating Function App...")
    if run_command(f"""
        az functionapp create \
            --name {app_name} \
            --resource-group {resource_group} \
            --storage-account {storage_account} \
            --consumption-plan-location {location} \
            --runtime python \
            --runtime-version 3.11 \
            --functions-version 4
    """):
        print("✅ Function App created successfully!")
        
        # Get URL
        result = subprocess.run(f"""
            az functionapp show \
                --name {app_name} \
                --resource-group {resource_group} \
                --query "defaultHostName" \
                --output tsv
        """, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            backend_url = f"https://{result.stdout.strip()}"
            print(f"🌐 Backend URL: {backend_url}")
            
            with open("backend_url.txt", "w") as f:
                f.write(backend_url)
            
            return backend_url
    
    print("❌ Function App deployment failed or hit quota limits")
    
    # Method 2: Alternative - suggest manual steps
    print("\n📋 MANUAL DEPLOYMENT STEPS:")
    print("1. Go to Azure Portal (portal.azure.com)")
    print("2. Create a new Function App:")
    print(f"   - Name: {app_name}")
    print(f"   - Resource Group: {resource_group}")
    print(f"   - Runtime: Python 3.11")
    print("   - Plan: Consumption")
    print("3. Once created, note the URL")
    print("4. Upload the code manually or use VS Code Azure extension")
    
    return None

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n🎉 Deployment completed!")
        print(f"📝 Backend URL: {result}")
    else:
        print(f"\n⚠️  Please complete manual deployment steps above")
