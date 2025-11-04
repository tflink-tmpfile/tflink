# Quick Deploy Guide - tflink

Fast track to get your package from GitHub to PyPI.

## Prerequisites

- ✅ GitHub account: `tflink-tmpfile`
- ✅ Repository created: https://github.com/tflink-tmpfile/tflink
- ✅ Local git configured with correct author info
- ✅ Code pushed to GitHub (using SSH or HTTPS)

## 🚀 Quick Steps

### 1. Push to GitHub ✅ COMPLETED

**Using SSH (Recommended):**
```bash
git remote set-url origin git@github.com:tflink-tmpfile/tflink.git
git push -u origin main
```

**Or using HTTPS with token:**
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/tflink-tmpfile/tflink.git
git push -u origin main
```

**Status**: ✅ Your code is now on GitHub!

### 2. Register PyPI Accounts (3 minutes)

**TestPyPI** (for testing): https://test.pypi.org/account/register/
- Email: pypi@tmpfile.link
- Username: Choose one (e.g., tflink-tmpfile)

**PyPI** (production): https://pypi.org/account/register/
- Use the same email and username

### 3. Get PyPI Tokens (2 minutes)

After registration, create API tokens:

**TestPyPI**: https://test.pypi.org/manage/account/token/
**PyPI**: https://pypi.org/manage/account/token/

For each:
1. Click "Add API token"
2. Token name: `tflink-upload`
3. Scope: "Entire account" (first time)
4. **COPY AND SAVE THE TOKEN!** (starts with `pypi-...`)

### 4. First Upload to PyPI (5 minutes)

```bash
# Install tools
pip install build twine

# Build
python -m build

# Upload to TestPyPI (test first!)
twine upload --repository testpypi -u __token__ -p YOUR_TESTPYPI_TOKEN dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ tflink

# If OK, upload to production PyPI
twine upload -u __token__ -p YOUR_PYPI_TOKEN dist/*
```

### 5. Setup Auto-Publish (2 minutes)

1. Go to: https://github.com/tflink-tmpfile/tflink/settings/secrets/actions
2. Click **"New repository secret"**
3. Name: `PYPI_API_TOKEN`
4. Value: [Your production PyPI token]
5. Click **"Add secret"**

### 6. Create First Release (2 minutes)

1. Go to: https://github.com/tflink-tmpfile/tflink/releases
2. Click **"Create a new release"**
3. Tag: `v0.1.0` (create new tag)
4. Title: `v0.1.0 - Initial Release`
5. Description: Brief description
6. Click **"Publish release"**

**Done!** GitHub Actions will automatically publish to PyPI.

## 🎯 Future Releases (Simple!)

1. Update version in code:
   ```python
   # tflink/__init__.py
   __version__ = '0.2.0'
   ```

2. Commit and push:
   ```bash
   git add .
   git commit -m "Release v0.2.0"
   git push
   ```

3. Create GitHub Release with tag `v0.2.0`

4. **Automatic**: GitHub Actions publishes to PyPI!

## 📝 Command Reference

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Create git tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| Permission denied (GitHub) | Create Personal Access Token, use in remote URL |
| Invalid credentials (PyPI) | Use `__token__` as username, token as password |
| File already exists | Increment version number |
| GitHub Actions fails | Check `PYPI_API_TOKEN` secret is set |

## 📚 Full Documentation

See `GITHUB_PYPI_SETUP.md` for detailed instructions and troubleshooting.

---

**Current Status:**
- ☐ GitHub token created
- ☐ Code pushed to GitHub
- ☐ PyPI tokens created
- ☐ Package uploaded to PyPI
- ☐ Auto-publish configured
- ☐ First release created
