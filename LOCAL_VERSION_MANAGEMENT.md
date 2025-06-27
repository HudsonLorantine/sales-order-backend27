# Local Version Management Guide

## Current Project Structure

Your project has the following branches and versions:

### Branches
- **main** - Live deployment branch (auto-deploys to Azure)
- **development** - Integration branch for testing features
- **master** - Protected production branch (stable releases)
- **feature/*** - Feature development branches

### Current Version: v1.0.0
Tagged on the master branch as the first stable release.

## Version Management Commands

### 1. Check Current Version and Status
```powershell
# Check current branch and status
git status

# List all branches (local and remote)
git branch -a

# List all version tags
git tag -l

# Show current version info
git describe --tags
```

### 2. Creating New Versions

#### For Minor Updates (bug fixes)
```powershell
# Create and switch to a feature branch
git checkout -b feature/bug-fix-description

# Make your changes...
# Add and commit changes
git add .
git commit -m "Fix: description of the bug fix"

# Push feature branch
git push origin feature/bug-fix-description

# Merge to development for testing
git checkout development
git pull origin development
git merge feature/bug-fix-description
git push origin development

# After testing, merge to main (triggers deployment)
git checkout main
git pull origin main
git merge development
git push origin main

# Create new patch version tag (e.g., v1.0.1)
git tag -a v1.0.1 -m "Version 1.0.1 - Bug fixes"
git push origin v1.0.1

# Merge to master for stable release
git checkout master
git pull origin master
git merge main
git push origin master
```

#### For Major Features (minor version)
```powershell
# Create feature branch
git checkout -b feature/new-feature-name

# Develop feature...
git add .
git commit -m "Add: new feature description"
git push origin feature/new-feature-name

# Follow same merge process as above
# Tag as v1.1.0 (minor version increment)
git tag -a v1.1.0 -m "Version 1.1.0 - New features"
git push origin v1.1.0
```

#### For Breaking Changes (major version)
```powershell
# Same process but tag as v2.0.0
git tag -a v2.0.0 -m "Version 2.0.0 - Breaking changes"
git push origin v2.0.0
```

### 3. Version Checking Commands
```powershell
# See what changed between versions
git diff v1.0.0..HEAD

# See commit history since last version
git log v1.0.0..HEAD --oneline

# Show specific version details
git show v1.0.0
```

### 4. Working with Versions Locally
```powershell
# Switch to a specific version (read-only)
git checkout v1.0.0

# Create a branch from a specific version
git checkout -b hotfix/urgent-fix v1.0.0

# Return to latest main
git checkout main
```

## Version Naming Convention

We use Semantic Versioning (SemVer): **MAJOR.MINOR.PATCH**

- **MAJOR** (v2.0.0): Breaking changes, incompatible API changes
- **MINOR** (v1.1.0): New features, backward compatible
- **PATCH** (v1.0.1): Bug fixes, backward compatible

## Local Development Best Practices

### 1. Always Start from Latest
```powershell
git checkout main
git pull origin main
git checkout -b feature/your-new-feature
```

### 2. Keep Features Small
- One feature per branch
- Regular commits with clear messages
- Test locally before pushing

### 3. Stay Updated
```powershell
# Update your feature branch with latest main
git checkout feature/your-feature
git pull origin main
git merge main
```

### 4. Clean Up
```powershell
# Delete merged feature branches locally
git branch -d feature/completed-feature

# Delete remote feature branches
git push origin --delete feature/completed-feature
```

## Emergency Hotfix Process

For urgent production fixes:

```powershell
# Create hotfix from master (stable production)
git checkout master
git pull origin master
git checkout -b hotfix/urgent-issue

# Make minimal fix
git add .
git commit -m "Hotfix: critical issue description"

# Deploy hotfix immediately
git checkout main
git merge hotfix/urgent-issue
git push origin main  # This triggers immediate deployment

# Tag the hotfix
git tag -a v1.0.2 -m "Version 1.0.2 - Critical hotfix"
git push origin v1.0.2

# Update master
git checkout master
git merge hotfix/urgent-issue
git push origin master

# Update development
git checkout development
git merge hotfix/urgent-issue
git push origin development

# Clean up
git branch -d hotfix/urgent-issue
```

## Visual Version History
```powershell
# See version history graphically
git log --oneline --graph --all --decorate

# See just tagged versions
git for-each-ref --sort=creatordate --format '%(refname) %(creatordate)' refs/tags
```
