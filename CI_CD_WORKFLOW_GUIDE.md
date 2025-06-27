# CI/CD Workflow Guide

## Overview
Your sales-order system uses **GitHub Actions** for Continuous Integration and Continuous Deployment (CI/CD). This means every code change automatically triggers builds, tests, and deployments.

## Current CI/CD Setup

### Backend (sales-order-backend)
- **Repository**: Your current repo
- **Trigger**: Push to `main` branch
- **Deployment Target**: Azure Container Apps
- **Workflow File**: `.github/workflows/main_sales-order-backend.yml`

### Frontend (sales-order-frontend)
- **Repository**: In your Project 1 folder
- **Trigger**: Push to `main` branch  
- **Deployment Target**: Azure Static Web Apps
- **Workflow File**: `.github/workflows/azure-static-web-apps-*.yml`

## How CI/CD Works Step-by-Step

### 1. Code Change Trigger
```
Developer → Local Code Change → Git Push → GitHub → GitHub Actions
```

### 2. Automatic Build Process
When you push code to the `main` branch:

```yaml
# What happens automatically:
1. GitHub receives your push
2. GitHub Actions starts a virtual machine (runner)
3. Runner downloads your code
4. Runner installs dependencies
5. Runner builds your application
6. Runner runs tests (if configured)
7. Runner packages your app
8. Runner deploys to Azure
9. Runner reports success/failure
```

### 3. Deployment Flow

#### Backend Deployment Flow
```
Local Code → GitHub → GitHub Actions → Azure Container Registry → Azure Container Apps
```

#### Frontend Deployment Flow  
```
Local Code → GitHub → GitHub Actions → Build React App → Azure Static Web Apps
```

## Current Workflow Files

### Backend Workflow (`.github/workflows/main_sales-order-backend.yml`)
```yaml
name: Build and deploy Python app to Azure Container Apps

on:
  push:
    branches: [ main ]  # Only deploys when you push to main
  workflow_dispatch:     # Allows manual trigger

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python version
      uses: actions/setup-python@v1
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Build and deploy to Azure Container Apps
      uses: azure/container-apps-deploy-action@v1
      with:
        # Deployment configuration...
```

## Monitoring Your CI/CD

### 1. Check Deployment Status
```powershell
# View recent workflow runs
gh workflow list

# View specific workflow run details
gh run list --workflow="Build and deploy Python app"

# View logs for a specific run
gh run view [RUN_ID] --log
```

### 2. GitHub Actions Dashboard
1. Go to your GitHub repository
2. Click **Actions** tab
3. See all workflow runs, their status, and logs

### 3. Azure Deployment Status
```powershell
# Check Azure Container Apps status
az containerapp show --name sales-order-backend --resource-group sales-order-rg

# View deployment logs
az containerapp logs show --name sales-order-backend --resource-group sales-order-rg
```

## Deployment Branches and Environments

### Current Setup:
- **main** → Automatic deployment to Azure (Production)
- **development** → No automatic deployment (Staging/Testing)
- **feature/*** → No automatic deployment (Development)

### Recommended Environment Setup:
```yaml
# You could set up multiple environments:

main branch → Production Azure environment
development branch → Staging Azure environment  
feature branches → No deployment (local testing only)
```

## Manual Deployment Controls

### 1. Trigger Manual Deployment
```powershell
# Trigger workflow manually via GitHub CLI
gh workflow run "Build and deploy Python app"

# Or via GitHub web interface:
# Repository → Actions → Select workflow → Run workflow
```

### 2. Stop/Rollback Deployment
```powershell
# Stop a running deployment
gh run cancel [RUN_ID]

# Rollback by deploying previous version
git checkout v1.0.0
git checkout -b hotfix/rollback
git push origin hotfix/rollback
# Then merge to main to deploy the previous version
```

## CI/CD Best Practices

### 1. Branch Protection
```powershell
# Set up branch protection (recommended)
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["continuous-integration"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}'
```

### 2. Environment Secrets
Your CI/CD uses these secrets (already configured):
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET` 
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_TENANT_ID`

### 3. Deployment Verification
After each deployment, verify:
```powershell
# Check if backend is running
curl https://your-backend-url.azurecontainerapps.io/health

# Check if frontend is accessible
curl https://your-frontend-url.azurestaticapps.net
```

## Troubleshooting CI/CD Issues

### 1. Deployment Failures
```powershell
# Check workflow logs
gh run view --log

# Common issues:
# - Missing secrets
# - Azure quota exceeded
# - Build failures
# - Dependency conflicts
```

### 2. Azure Resource Issues
```powershell
# Check Azure resource status
az group show --name sales-order-rg
az containerapp list --resource-group sales-order-rg
```

### 3. GitHub Actions Debugging
Add debugging to your workflow:
```yaml
- name: Debug Environment
  run: |
    echo "Current directory: $(pwd)"
    echo "Python version: $(python --version)"
    echo "Pip version: $(pip --version)"
    ls -la
```

## Development Workflow Integration

### Daily Development Process:
```powershell
# 1. Start new feature
git checkout main
git pull origin main
git checkout -b feature/new-feature

# 2. Develop locally
# Make changes...
python app.py  # Test locally

# 3. Commit changes
git add .
git commit -m "Add: new feature description"
git push origin feature/new-feature

# 4. Create Pull Request (no deployment yet)
gh pr create --title "Add new feature" --body "Description"

# 5. Merge to main (triggers automatic deployment)
gh pr merge --merge
```

### Testing Before Production:
```powershell
# Option 1: Test locally first
python app.py
# Test your changes

# Option 2: Use development branch for staging
git checkout development
git merge feature/new-feature
git push origin development
# Manually deploy development branch to staging environment
```

## CI/CD Monitoring Commands

### Real-time Monitoring:
```powershell
# Watch workflow runs
gh run list --limit 5

# Follow live deployment logs
gh run view [RUN_ID] --log --follow

# Check Azure container status
az containerapp show --name sales-order-backend --resource-group sales-order-rg --query "properties.provisioningState"
```

### Performance Monitoring:
```powershell
# Check deployment times
gh run list --workflow="Build and deploy Python app" --json startedAt,conclusion,url

# Monitor Azure app performance
az monitor metrics list --resource [RESOURCE_ID] --metric "Requests" --interval PT1M
```

This CI/CD setup ensures that every code change you make is automatically tested, built, and deployed to Azure, providing a seamless development experience.
