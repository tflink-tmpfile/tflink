# GitHub and PyPI Setup Guide

This guide will help you push your code to GitHub and set up automatic publishing to PyPI.

## Step 1: Push Code to GitHub

### Option A: Using SSH Key (Recommended) ✅

If you have SSH key configured:

```bash
# Set remote URL with SSH
git remote set-url origin git@github.com:tflink-tmpfile/tflink.git

# Push to GitHub
git push -u origin main
```

You should see output like:
```
Enumerating objects: 26, done.
Counting objects: 100% (26/26), done.
...
To github.com:tflink-tmpfile/tflink.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### Option B: Using Personal Access Token

If you don't have SSH key:

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Settings:
   - **Note**: `tflink-push-access`
   - **Expiration**: Choose your preferred duration
   - **Scopes** (check these):
     - ☑ `repo` (Full control of private repositories)
     - ☑ `workflow` (Update GitHub Action workflows)
4. Click **"Generate token"**
5. **IMPORTANT**: Copy the token immediately (it won't be shown again!)
   - Format: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Configure and push:

```bash
# Set remote URL with token
git remote set-url origin https://YOUR_TOKEN@github.com/tflink-tmpfile/tflink.git

# Push to GitHub
git push -u origin main
```

## Step 2: Register on PyPI

### 2.1 Create PyPI Account

1. **TestPyPI** (for testing): https://test.pypi.org/account/register/
2. **Production PyPI**: https://pypi.org/account/register/

Fill in:
- Username: `tflink-tmpfile` (or your choice)
- Email: `pypi@tmpfile.link`
- Password: Choose a strong password

### 2.2 Create PyPI API Token

**For TestPyPI:**
1. Go to: https://test.pypi.org/manage/account/token/
2. Click **"Add API token"**
3. Token name: `tflink-upload`
4. Scope: "Entire account" (can restrict to project after first upload)
5. Click **"Add token"**
6. **COPY THE TOKEN** (starts with `pypi-...`)

**For Production PyPI:**
1. Go to: https://pypi.org/manage/account/token/
2. Repeat the same steps as TestPyPI
3. **COPY THIS TOKEN TOO**

**⚠️ IMPORTANT**: Save both tokens securely! They won't be shown again.

## Step 3: Manual Publishing to PyPI (First Time)

### 3.1 Install Build Tools

```bash
pip install build twine
```

### 3.2 Build Package

```bash
# Clean old builds
rm -rf build/ dist/ *.egg-info/

# Build distribution
python -m build
```

This creates:
- `dist/tflink-0.1.0.tar.gz` (source distribution)
- `dist/tflink-0.1.0-py3-none-any.whl` (wheel distribution)

### 3.3 Check Package

```bash
twine check dist/*
```

Should show:
```
Checking dist/tflink-0.1.0.tar.gz: PASSED
Checking dist/tflink-0.1.0-py3-none-any.whl: PASSED
```

### 3.4 Upload to TestPyPI (Test First!)

```bash
twine upload --repository testpypi dist/*
```

Enter:
- Username: `__token__`
- Password: [paste your TestPyPI token]

Or use command line:
```bash
twine upload --repository testpypi -u __token__ -p YOUR_TESTPYPI_TOKEN dist/*
```

### 3.5 Test Installation from TestPyPI

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ tflink

# Test it
python -c "from tflink import TFLinkClient; print('Success!')"

# Cleanup
deactivate
rm -rf test_env
```

### 3.6 Upload to Production PyPI

```bash
twine upload dist/*
```

Enter:
- Username: `__token__`
- Password: [paste your PyPI token]

Or:
```bash
twine upload -u __token__ -p YOUR_PYPI_TOKEN dist/*
```

### 3.7 Verify on PyPI

Visit: https://pypi.org/project/tflink/

Your package is now live! Users can install it:
```bash
pip install tflink
```

## Step 4: Set Up Automatic GitHub → PyPI Publishing

### 4.1 Add PyPI Token to GitHub Secrets

1. Go to your GitHub repository: https://github.com/tflink-tmpfile/tflink
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add secret:
   - **Name**: `PYPI_API_TOKEN`
   - **Value**: [paste your production PyPI token]
5. Click **"Add secret"**

### 4.2 Verify GitHub Actions Workflow

Your repository already includes `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

This workflow will:
- ✅ Trigger when you create a GitHub Release
- ✅ Build the package automatically
- ✅ Upload to PyPI automatically

### 4.3 Create a GitHub Release (Triggers Auto-Publish)

**Method 1: Via GitHub Web UI**
1. Go to: https://github.com/tflink-tmpfile/tflink/releases
2. Click **"Create a new release"**
3. Click **"Choose a tag"** → Type `v0.1.0` → Click **"Create new tag: v0.1.0 on publish"**
4. Release title: `v0.1.0 - Initial Release`
5. Description:
   ```markdown
   ## tflink v0.1.0 - Initial Release

   First stable release of tflink Python library for tmpfile.link file uploads.

   ### Features
   - Anonymous and authenticated file uploads
   - Two download link formats (standard and URL-encoded)
   - Complete error handling
   - Full type hints support
   - Comprehensive unit tests

   ### Installation
   ```bash
   pip install tflink
   ```

   ### Quick Start
   ```python
   from tflink import TFLinkClient

   client = TFLinkClient()
   result = client.upload('file.pdf')
   print(result.download_link)
   ```
   ```
6. Click **"Publish release"**

**Method 2: Via Command Line**
```bash
# Create and push a tag
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0

# Then create release via GitHub web UI
```

### 4.4 Monitor GitHub Actions

1. Go to: https://github.com/tflink-tmpfile/tflink/actions
2. You'll see the "Publish to PyPI" workflow running
3. Wait for it to complete (usually 1-2 minutes)
4. Check the logs to ensure success

### 4.5 Verify Auto-Published Package

Visit: https://pypi.org/project/tflink/

You should see version 0.1.0 published!

## Step 5: Future Releases (Automated Workflow)

For all future releases, follow this simple process:

### 5.1 Update Version

Edit these files:
```bash
# tflink/__init__.py
__version__ = '0.2.0'

# pyproject.toml
version = "0.2.0"
```

### 5.2 Commit Changes

```bash
git add .
git commit -m "Bump version to 0.2.0"
git push
```

### 5.3 Create GitHub Release

Create a new release on GitHub (as shown in Step 4.3) with tag `v0.2.0`

### 5.4 Automatic Publishing

GitHub Actions will automatically:
1. Detect the new release
2. Build the package
3. Publish to PyPI
4. Done! ✅

## Troubleshooting

### Issue: "Invalid or non-existent authentication information"

**Solution**: Check your PyPI token:
- Make sure it's the full token (starts with `pypi-`)
- Verify the token hasn't expired
- Regenerate a new token if needed

### Issue: "File already exists"

**Solution**: You can't re-upload the same version
- Increment the version number
- Rebuild and upload

### Issue: GitHub Actions fails with "Invalid credentials"

**Solution**:
- Go to GitHub repository Settings → Secrets
- Verify `PYPI_API_TOKEN` is set correctly
- Regenerate PyPI token if needed
- Update the secret with the new token

### Issue: Package not installing correctly

**Solution**:
- Check `pyproject.toml` dependencies
- Test in a clean virtual environment
- Check PyPI project page for errors

## Summary Checklist

- [ ] Created GitHub Personal Access Token
- [ ] Pushed code to GitHub
- [ ] Registered on TestPyPI and PyPI
- [ ] Created PyPI API tokens (TestPyPI and production)
- [ ] Tested upload to TestPyPI
- [ ] Uploaded to production PyPI
- [ ] Added `PYPI_API_TOKEN` to GitHub Secrets
- [ ] Created first GitHub Release
- [ ] Verified automatic publishing works

## Security Notes

1. **Never commit tokens to git**
   - Tokens are in GitHub Secrets (secure)
   - Use `.gitignore` for local config files

2. **Token permissions**
   - Use scoped tokens (limit to specific project after first upload)
   - Rotate tokens periodically

3. **Keep tokens secure**
   - Store in password manager
   - Don't share in plain text
   - Regenerate if compromised

## Resources

- **PyPI**: https://pypi.org
- **TestPyPI**: https://test.pypi.org
- **GitHub Tokens**: https://github.com/settings/tokens
- **Python Packaging Guide**: https://packaging.python.org/
- **Twine Documentation**: https://twine.readthedocs.io/

---

**Need help?** Check the logs in GitHub Actions or PyPI project page for detailed error messages.
