# Developer Setup Guide

This guide shows you how to set up GitHub repository and PyPI publishing for the first time.

> **Note:** This guide is for project maintainers only. Regular users should see the [Getting Started](../user-guide/getting-started.md) guide.

## Prerequisites

- Python 3.8 or higher
- Git installed
- GitHub account
- PyPI account

## 1. GitHub Repository Setup

### Option A: Using SSH Key (Recommended)

```bash
# 1. Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. Add SSH key to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 3. Copy public key
cat ~/.ssh/id_ed25519.pub
# Copy the output and add to GitHub:
# https://github.com/settings/keys

# 4. Set up remote
git remote add origin git@github.com:tflink-tmpfile/tflink.git

# 5. Push code
git push -u origin main
```

### Option B: Using Personal Access Token

```bash
# 1. Create token at: https://github.com/settings/tokens
# Select scopes: repo, workflow

# 2. Set up remote with token
git remote add origin https://YOUR_TOKEN@github.com/tflink-tmpfile/tflink.git

# 3. Push code
git push -u origin main
```

## 2. PyPI Account Setup

### Create PyPI Account

1. Visit https://pypi.org/account/register/
2. Verify your email
3. Enable 2FA (recommended)

### Create API Token

1. Visit https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `tflink-github-actions`
4. Scope: "Entire account" (or specific to tflink project after first upload)
5. Copy the token (starts with `pypi-`)

**⚠️ Important:** Save this token immediately! You won't be able to see it again.

## 3. GitHub Secrets Setup

Add PyPI token to GitHub repository secrets:

1. Go to: https://github.com/tflink-tmpfile/tflink/settings/secrets/actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: Paste your PyPI token
5. Click "Add secret"

## 4. Verify GitHub Actions

The repository includes two GitHub Actions workflows:

### test.yml - Continuous Integration

**Triggers:** Every push to main/develop branches

**What it does:**
- Runs tests on Python 3.8-3.12
- Tests on Ubuntu, macOS, Windows
- Generates coverage reports

**Location:** `.github/workflows/test.yml`

### publish.yml - PyPI Publishing

**Triggers:** When you create a GitHub Release

**What it does:**
- Builds the package
- Publishes to PyPI using `PYPI_API_TOKEN`

**Location:** `.github/workflows/publish.yml`

### Test the Workflows

```bash
# Make a small change and push
git commit --allow-empty -m "Test CI workflow"
git push

# Check workflow status:
# https://github.com/tflink-tmpfile/tflink/actions
```

## 5. First Release to PyPI

### Option A: Manual First Release (Recommended)

For the first release, it's recommended to publish manually to ensure everything works:

```bash
# 1. Build the package
python -m build

# 2. Check the package
twine check dist/*

# 3. Upload to PyPI
twine upload dist/*
# Enter your PyPI username and password
# Or use: twine upload -u __token__ -p YOUR_PYPI_TOKEN dist/*

# 4. Verify on PyPI
# Visit: https://pypi.org/project/tflink/

# 5. Create GitHub Release to mark the version
# Visit: https://github.com/tflink-tmpfile/tflink/releases/new
# Tag: v0.1.0
# Title: v0.1.0 - Initial Release
# Click "Publish release"
```

### Option B: Automated First Release

```bash
# 1. Create a git tag
git tag -a v0.1.0 -m "Release 0.1.0"
git push origin v0.1.0

# 2. Create GitHub Release
# Visit: https://github.com/tflink-tmpfile/tflink/releases/new?tag=v0.1.0
# Click "Publish release"
# GitHub Actions will automatically publish to PyPI

# 3. Monitor the workflow
# Visit: https://github.com/tflink-tmpfile/tflink/actions
```

## 6. Development Environment Setup

### Clone Repository

```bash
git clone git@github.com:tflink-tmpfile/tflink.git
cd tflink
```

### Install Development Dependencies

```bash
# Install package in development mode with dev dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Quick functionality test
make quick-test
```

### Code Quality Tools

```bash
# Format code
make format

# Run linters
make lint
```

## 7. Git Configuration

Set up git with correct author information:

```bash
git config user.name "tfLink"
git config user.email "pypi@tmpfile.link"
```

## 8. Verify Everything Works

```bash
# Check Python version
python --version

# Check git status
git status

# Check installed packages
pip list | grep tflink

# Run tests
make test

# Verify you can build
make build
```

## Makefile Commands Reference

```bash
# Development
make install        # Install library
make install-dev    # Install with dev dependencies
make test          # Run tests
make test-cov      # Run tests with coverage
make quick-test    # Quick functionality test
make format        # Format code
make lint          # Check code quality

# Version Management
make version-patch  # Bump patch version (0.1.0 -> 0.1.1)
make version-minor  # Bump minor version (0.1.0 -> 0.2.0)
make version-major  # Bump major version (0.1.0 -> 1.0.0)
make release       # Push code and tags

# Building
make clean         # Clean build files
make build         # Build distribution packages
```

## Common Issues

### SSH Permission Denied

**Solution:**
```bash
# Test SSH connection
ssh -T git@github.com

# If it fails, check SSH key:
ssh-add -l

# Add key if needed:
ssh-add ~/.ssh/id_ed25519
```

### PYPI_API_TOKEN Not Working

**Solution:**
1. Check token hasn't expired
2. Verify secret name is exactly `PYPI_API_TOKEN`
3. Ensure token has correct permissions
4. Create a new token if needed

### GitHub Actions Failing

**Solution:**
1. Check workflow logs: https://github.com/tflink-tmpfile/tflink/actions
2. Verify all secrets are set correctly
3. Ensure requirements are properly defined in pyproject.toml

## Next Steps

Once setup is complete:

1. See [Release Guide](release.md) for publishing new versions
2. See [Getting Started](../user-guide/getting-started.md) for user documentation
3. Update [CHANGELOG.md](../../CHANGELOG.md) when making changes

## Resources

- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)
