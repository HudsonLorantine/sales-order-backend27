#!/usr/bin/env python3
"""
Simple deployment of Sales Order Backend as Azure Function App
"""

import subprocess
import sys

def run_command(cmd):
    """Run command and show output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    # Configuration
    resource_group = "sales-order-rg"
    function_app_name = "sales-order-backend-func"
    storage_account = "salesorderbackend27"
    location = "eastus2"
    
    print("🚀 Deploying Sales Order Backend as Azure Function App...")
    
    # Create storage account (required for function apps)
    print("\n1. Creating storage account...")
    if not run_command(f"""
        az storage account create \
            --name {storage_account} \
            --resource-group {resource_group} \
            --location {location} \
            --sku Standard_LRS
    """):
        print("ℹ️  Storage account might already exist, continuing...")
    
    # Create Function App
    print("\n2. Creating Function App...")
    if not run_command(f"""
        az functionapp create \
            --name {function_app_name} \
            --resource-group {resource_group} \
            --storage-account {storage_account} \
            --consumption-plan-location {location} \
            --runtime python \
            --runtime-version 3.11 \
            --functions-version 4
    """):
        print("❌ Failed to create Function App")
        return False
    
    # Deploy the code
    print("\n3. Deploying code...")
    if not run_command(f"""
        func azure functionapp publish {function_app_name}
    """):
        print("❌ Failed to deploy code")
        return False
    
    # Get the Function App URL
    print("\n4. Getting Function App URL...")
    result = subprocess.run(f"""
        az functionapp show \
            --name {function_app_name} \
            --resource-group {resource_group} \
            --query "defaultHostName" \
            --output tsv
    """, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        backend_url = f"https://{result.stdout.strip()}"
        print(f"\n✅ Backend deployed successfully!")
        print(f"🌐 Backend URL: {backend_url}")
        print(f"📊 API Base URL: {backend_url}/api")
        
        # Save URL for frontend
        with open("backend_url.txt", "w") as f:
            f.write(backend_url)
        
        return backend_url
    else:
        print("❌ Failed to get Function App URL")
        return False

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n🎉 Deployment completed!")
        print(f"📝 Next step: Update frontend App.jsx with the backend URL")
    else:
        print(f"\n❌ Deployment failed!")
