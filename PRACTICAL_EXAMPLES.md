# Practical Examples - Version Management & CI/CD

## Your Current Setup Status

### ✅ What's Already Working:
- **Repository**: sales-order-backend with GitHub Actions
- **Current Version**: v1.0.0 (tagged on master branch)
- **Branches**: main, development, master, feature branches
- **CI/CD**: Automatic deployment on push to main branch
- **Deployed**: Azure Container Apps with live backend URL

### 📊 Recent Activity:
```
Latest commits:
* a8dda2f (v1.0.0) 📚 Add comprehensive documentation
* 3c492d7 Fix sample data import 
* 59c90d6 🎉 PRODUCTION RELEASE v1.0 - Enhanced sample data
```

## Example 1: Adding a New Feature (Complete Process)

Let's say you want to add a new API endpoint for order analytics.

### Step 1: Create Feature Branch
```powershell
# Start from latest main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/order-analytics
```

### Step 2: Make Changes Locally
```powershell
# Edit your code (example: add new route to app.py)
# Add analytics endpoint...

# Test locally
python app.py
# Test at http://localhost:5000/api/analytics

# Verify it works locally first
```

### Step 3: Commit and Push Feature
```powershell
git add .
git commit -m "Add: order analytics endpoint with sales summaries"
git push origin feature/order-analytics
```
**Result**: Feature branch created, **NO deployment happens yet** ✅

### Step 4: Create Pull Request
```powershell
gh pr create --title "Add Order Analytics Endpoint" --body "Adds /api/analytics endpoint for sales summaries and customer metrics"
```
**Result**: Pull request created for code review, **still NO deployment** ✅

### Step 5: Merge and Deploy
```powershell
# After review, merge to main
gh pr merge --merge

# Alternative: merge manually
git checkout main
git pull origin main
git merge feature/order-analytics  
git push origin main
```
**Result**: 🚀 **Automatic deployment triggered!** GitHub Actions runs and deploys to Azure.

### Step 6: Create Version Tag
```powershell
# Tag the new version
git tag -a v1.1.0 -m "Version 1.1.0 - Add order analytics endpoint"
git push origin v1.1.0

# Update master branch (production stable)
git checkout master
git pull origin master
git merge main
git push origin master
```

## Example 2: Emergency Hotfix (Fast Process)

Production is down! Customer authentication is broken.

### Step 1: Hotfix from Stable Version
```powershell
# Start from current production (master)
git checkout master
git pull origin master

# Create hotfix branch
git checkout -b hotfix/auth-fix
```

### Step 2: Make Critical Fix
```powershell
# Fix the auth issue quickly
# Edit auth.py or app.py...

# Test the fix locally
python app.py

# Commit fix
git add .
git commit -m "Hotfix: fix JWT token validation breaking authentication"
```

### Step 3: Deploy Immediately
```powershell
# Merge directly to main for immediate deployment
git checkout main
git merge hotfix/auth-fix
git push origin main
```
**Result**: 🚨 **Emergency deployment starts immediately!**

### Step 4: Update All Branches
```powershell
# Create hotfix version
git tag -a v1.0.1 -m "Version 1.0.1 - Critical auth fix"
git push origin v1.0.1

# Update master
git checkout master
git merge hotfix/auth-fix
git push origin master

# Update development
git checkout development  
git merge hotfix/auth-fix
git push origin development

# Clean up
git branch -d hotfix/auth-fix
git push origin --delete hotfix/auth-fix
```

## Example 3: Monitoring Your CI/CD

### Check Current Deployment Status
```powershell
# See recent deployments
gh run list --limit 3

# Example output:
# STATUS  TITLE                WORKFLOW           BRANCH  EVENT  ID           
# ✓       Add order analytics  Build and Deploy   main    push   15920612850
# X       Fix auth bug         Build and Deploy   main    push   15920612849  
# ✓       Update frontend      Build and Deploy   main    push   15920612848
```

### View Deployment Logs
```powershell
# Get logs for latest deployment
gh run view --log

# Or specific deployment
gh run view 15920612850 --log
```

### Check Azure Status
```powershell
# Check your container app status
az containerapp show --name sales-order-backend --resource-group sales-order-rg --query "properties.provisioningState"

# Check if app is responding
curl https://sales-order-backend.something.azurecontainerapps.io/health
```

## Example 4: Version Comparison

### See What Changed Between Versions
```powershell
# Compare current main with last version
git diff v1.0.0..HEAD

# See commit history since last version
git log v1.0.0..HEAD --oneline

# Example output:
# a8dda2f Add order analytics endpoint
# 3c492d7 Fix sample data import bug
# 59c90d6 Update documentation
```

### Compare Two Specific Versions
```powershell
# See changes between v1.0.0 and v1.1.0
git diff v1.0.0..v1.1.0

# List files changed
git diff --name-only v1.0.0..v1.1.0
```

## Example 5: Rollback Strategy

Production deployment failed! Need to rollback.

### Quick Rollback Method
```powershell
# Method 1: Deploy previous version
git checkout v1.0.0
git checkout -b rollback/emergency-v1.0.0
git push origin rollback/emergency-v1.0.0

# Merge to main (triggers deployment of old version)
git checkout main
git merge rollback/emergency-v1.0.0
git push origin main
```

### Cancel Running Deployment
```powershell
# Stop current deployment
gh run list --limit 1  # Get latest run ID
gh run cancel 15920612850  # Cancel specific run
```

## Example 6: Local Testing Before Deployment

### Test Changes Locally
```powershell
# Run your Flask app locally
python app.py

# Test all endpoints
curl http://localhost:5000/api/customers
curl http://localhost:5000/api/products  
curl http://localhost:5000/api/orders

# Test new features before pushing
curl http://localhost:5000/api/analytics
```

### Validate Before Push
```powershell
# Check your changes
git status
git diff

# Run any tests (if you have them)
python -m pytest tests/

# Only push when confident
git push origin feature/your-feature
```

## Current Workflow Summary

**Your typical development process**:

1. **Feature Development**: `feature/branch` → Test locally → Push (no deployment)
2. **Integration**: Create PR → Review → Merge to `main` → **Automatic deployment**
3. **Versioning**: Tag stable releases → Update `master` branch
4. **Hotfixes**: `hotfix/branch` → Merge to `main` → **Immediate deployment** → Update all branches

**Deployment Triggers**:
- ✅ Push to `main` → Automatic deployment to Azure
- ❌ Push to `development` → No deployment  
- ❌ Push to `feature/*` → No deployment
- ❌ Push to `master` → No deployment (stable archive only)

**Monitoring**:
- GitHub Actions tab for build logs
- `gh run list` for command-line monitoring  
- Azure portal for runtime monitoring
- Your app URLs for functional testing

This setup gives you professional-grade version control with automated deployments!
