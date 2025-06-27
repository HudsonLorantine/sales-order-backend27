# Development Workflow & Git Branch Strategy

## 🌳 Branch Structure

### Protected Branches
- **`master`** 🔒 - **PRODUCTION VERSION** - Stable, tested, production-ready code
  - Never commit directly to master
  - Only accepts merges from `main` after thorough testing
  - Represents the "golden" version of the application

- **`main`** 🚀 - **DEPLOYMENT BRANCH** - Current live version
  - Connected to Azure Container Apps CI/CD
  - Automatic deployment to production environment
  - Should always be stable and functional

### Development Branches
- **`development`** 🔧 - **INTEGRATION BRANCH** - Active development work
  - Where feature branches are merged for testing
  - Pre-production integration testing
  - Code review staging area

- **`feature/*`** ✨ - **FEATURE BRANCHES** - Individual features/fixes
  - Branch from `development`
  - Merge back to `development` via Pull Request
  - Examples: `feature/user-authentication`, `feature/enhanced-reporting`

## 🔄 Recommended Workflow

### For New Features:
```bash
# 1. Switch to development branch
git checkout development
git pull origin development

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Work on your feature (make commits)
git add .
git commit -m "Add your feature description"

# 4. Push feature branch
git push origin feature/your-feature-name

# 5. Create Pull Request from feature/your-feature-name → development
# 6. After review and approval, merge to development
# 7. Test in development environment
# 8. When ready for production, merge development → main → master
```

### For Hotfixes:
```bash
# 1. Create hotfix branch from main
git checkout main
git checkout -b hotfix/critical-issue

# 2. Fix the issue
git add .
git commit -m "Fix critical issue description"

# 3. Push and create PR to main
git push origin hotfix/critical-issue

# 4. After approval, merge to main (auto-deploys)
# 5. Merge main → master to update production version
# 6. Merge main → development to keep dev up to date
```

## 🛡️ Branch Protection Rules

### Master Branch Rules:
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Restrict pushes to admins only
- ✅ No force pushes allowed

### Main Branch Rules:
- ✅ Require pull request reviews
- ✅ Connected to Azure deployment
- ✅ Auto-deploy on merge
- ✅ Require CI checks to pass

## 📋 Release Process

### Minor Updates (v1.1, v1.2, etc.):
1. Complete feature development in `feature/*` branches
2. Merge features to `development` for integration testing
3. Create Pull Request: `development` → `main`
4. Deploy to production (Azure auto-deploys from `main`)
5. Create Pull Request: `main` → `master`
6. Tag release in `master`: `git tag v1.1.0`

### Major Releases (v2.0, v3.0, etc.):
1. Create release branch: `release/v2.0`
2. Finalize features and testing
3. Merge to `main` for production deployment
4. Merge to `master` and tag: `git tag v2.0.0`
5. Update documentation and changelog

## 🏷️ Tagging Strategy

```bash
# Semantic Versioning: MAJOR.MINOR.PATCH
# MAJOR: Breaking changes
# MINOR: New features (backward compatible)
# PATCH: Bug fixes (backward compatible)

# Examples:
git tag v1.0.0  # Initial production release
git tag v1.1.0  # Added new features
git tag v1.1.1  # Bug fixes
git tag v2.0.0  # Major update with breaking changes
```

## 📝 Commit Message Format

```
<type>(<scope>): <description>

<body>

<footer>
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build process or auxiliary tool changes

### Examples:
```
feat(api): add customer search endpoint

Add GET /api/customers/search with query parameters
for filtering customers by company name and email.

Resolves #123
```

```
fix(orders): resolve 405 error on order creation

Fixed missing POST route handler for /api/orders
endpoint. Added proper request validation and
error handling.

Fixes #456
```

## 🚀 Deployment Pipeline

```
feature/branch → development → main → master
      ↓              ↓         ↓       ↓
   Local Dev    Integration  Azure   Archive
   Testing      Testing      Deploy  Version
```

### Automatic Triggers:
- **Push to `main`** → Azure Container Apps deployment
- **PR to `main`** → CI/CD validation checks
- **Tag creation** → Release notes generation

## 📊 Current Repository State

### Branches:
- ✅ `master` - Production archive (v1.0)
- ✅ `main` - Live deployment branch
- ✅ `development` - Active development
- ✅ `feature/enhanced-data` - Current feature work

### Deployment Status:
- 🟢 Azure Container Apps: **LIVE**
- 🟢 Frontend: **https://orange-bay-0d657f50f.1.azurestaticapps.net**
- 🟢 Backend API: **https://sales-order-backend.blueocean-64f72639.eastus.azurecontainerapps.io**

## 🔧 Quick Commands

```bash
# Switch to development for new features
git checkout development

# Create new feature branch
git checkout -b feature/your-feature

# Update branch with latest changes
git pull origin development

# Check current branch and status
git status && git branch

# View commit history
git log --oneline --graph

# Sync with remote branches
git fetch --all
```

---
**Last Updated**: June 27, 2025  
**Version**: 1.0  
**Workflow Status**: ✅ Active
