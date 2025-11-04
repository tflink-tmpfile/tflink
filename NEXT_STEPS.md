# Next Steps - Publishing tflink to PyPI

## ✅ What's Done

- ✅ Code is ready with no personal information
- ✅ Git repository configured correctly
- ✅ Code pushed to GitHub: https://github.com/tflink-tmpfile/tflink
- ✅ Documentation complete

## 🎯 What's Next - PyPI Publishing

You need to publish your package to PyPI so users can install it with `pip install tflink`.

### Step 1: Register on PyPI (5 minutes)

You need TWO accounts:

#### A. TestPyPI (for testing)
1. Go to: https://test.pypi.org/account/register/
2. Fill in:
   - **Email**: `pypi@tmpfile.link`
   - **Username**: Choose one (e.g., `tflink` or `tflink-tmpfile`)
   - **Password**: Create a strong password
3. Verify your email

#### B. PyPI (production)
1. Go to: https://pypi.org/account/register/
2. Use the **same email and username** as TestPyPI
3. Verify your email

**Why two accounts?**
- TestPyPI: Safe place to test uploads (mistakes don't matter)
- PyPI: Real production package (mistakes are permanent!)

### Step 2: Create API Tokens (5 minutes)

You need TWO tokens (one for each PyPI):

#### A. TestPyPI Token
1. Login to TestPyPI
2. Go to: https://test.pypi.org/manage/account/token/
3. Click **"Add API token"**
4. Settings:
   - Token name: `tflink-upload`
   - Scope: "Entire account (all projects)"
5. Click **"Add token"**
6. **IMPORTANT**: Copy the token NOW (looks like `pypi-AgEIcH...`)
7. Save it somewhere safe (password manager, note app, etc.)

#### B. PyPI Token (Production)
1. Login to PyPI
2. Go to: https://pypi.org/manage/account/token/
3. Repeat the same steps as TestPyPI
4. **IMPORTANT**: Copy this token too and save it separately

**Security Note**: Treat these tokens like passwords. Never commit them to git!

### Step 3: Test Upload to TestPyPI (10 minutes)

Now let's do a test upload to make sure everything works:

```bash
# 1. Install build tools (if not already installed)
pip install build twine

# 2. Build your package
python -m build

# This creates two files in dist/:
# - tflink-0.1.0.tar.gz (source)
# - tflink-0.1.0-py3-none-any.whl (wheel)

# 3. Check the package (make sure it's valid)
twine check dist/*

# Should show:
# Checking dist/tflink-0.1.0.tar.gz: PASSED
# Checking dist/tflink-0.1.0-py3-none-any.whl: PASSED

# 4. Upload to TestPyPI
twine upload --repository testpypi dist/*

# When prompted:
# Username: __token__
# Password: [paste your TestPyPI token]
```

**Expected output:**
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading tflink-0.1.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 15.3/15.3 kB • 00:00
Uploading tflink-0.1.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.1/12.1 kB • 00:00

View at:
https://test.pypi.org/project/tflink/0.1.0/
```

### Step 4: Test Installation (5 minutes)

Test that your package can be installed from TestPyPI:

```bash
# Create a test environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ tflink

# Test it works
python -c "from tflink import TFLinkClient; print('✓ Import successful!')"

# Try the quick test
python -c "from tflink import TFLinkClient; client = TFLinkClient(); print(client)"

# Cleanup
deactivate
rm -rf test_env
```

If everything works, you're ready for production!

### Step 5: Upload to Production PyPI (5 minutes)

**⚠️ IMPORTANT**: This is the real deal. Once uploaded, you can't delete or modify it!

```bash
# Upload to production PyPI
twine upload dist/*

# When prompted:
# Username: __token__
# Password: [paste your PRODUCTION PyPI token]
```

**Success!** Your package is now live at:
- https://pypi.org/project/tflink/

Anyone can now install it:
```bash
pip install tflink
```

### Step 6: Setup Automatic Publishing (10 minutes)

So you don't have to manually upload every time:

#### A. Add PyPI Token to GitHub

1. Go to: https://github.com/tflink-tmpfile/tflink/settings/secrets/actions
2. Click **"New repository secret"**
3. Add secret:
   - **Name**: `PYPI_API_TOKEN`
   - **Secret**: [paste your PRODUCTION PyPI token]
4. Click **"Add secret"**

#### B. Verify Workflow File

Your repo already has `.github/workflows/publish.yml`. This workflow will:
- Trigger when you create a GitHub Release
- Build the package automatically
- Upload to PyPI automatically

#### C. Create Your First Release

1. Go to: https://github.com/tflink-tmpfile/tflink/releases
2. Click **"Create a new release"**
3. Click **"Choose a tag"** → Type `v0.1.0` → Click **"Create new tag: v0.1.0 on publish"**
4. Release title: `v0.1.0 - Initial Release`
5. Description:
   ```markdown
   ## 🎉 First Release - tflink v0.1.0

   Python library for uploading files to tmpfile.link

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

   ### Features
   - Anonymous and authenticated uploads
   - Two download link formats
   - Full error handling
   - Complete documentation
   ```
6. Click **"Publish release"**

#### D. Watch It Work!

1. Go to: https://github.com/tflink-tmpfile/tflink/actions
2. You'll see "Publish to PyPI" workflow running
3. Wait 1-2 minutes for it to complete
4. Check https://pypi.org/project/tflink/ - new version should appear!

## 🎯 Summary of Next Steps

| Step | What | Time | Link |
|------|------|------|------|
| 1 | Register TestPyPI | 3 min | https://test.pypi.org/account/register/ |
| 2 | Register PyPI | 3 min | https://pypi.org/account/register/ |
| 3 | Create TestPyPI token | 2 min | https://test.pypi.org/manage/account/token/ |
| 4 | Create PyPI token | 2 min | https://pypi.org/manage/account/token/ |
| 5 | Build package | 2 min | `python -m build` |
| 6 | Upload to TestPyPI | 3 min | `twine upload --repository testpypi dist/*` |
| 7 | Test installation | 3 min | Install from TestPyPI |
| 8 | Upload to PyPI | 3 min | `twine upload dist/*` |
| 9 | Add secret to GitHub | 2 min | GitHub Settings → Secrets |
| 10 | Create GitHub Release | 3 min | GitHub Releases |

**Total time: ~30 minutes**

## 📝 Commands Cheat Sheet

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ tflink

# Test install from PyPI
pip install tflink
```

## 🆘 Troubleshooting

### "Invalid or non-existent authentication"
- Make sure username is `__token__` (not your username!)
- Make sure you copied the full token (starts with `pypi-`)

### "File already exists"
- You can't upload the same version twice
- Increment version in `tflink/__init__.py` and `pyproject.toml`
- Rebuild with `python -m build`

### "403 Forbidden"
- Check your token hasn't expired
- Make sure you're using the right token (TestPyPI vs PyPI)
- Regenerate token if needed

## 🎉 What Happens After Publishing?

Once published to PyPI:

1. **Anyone can install your package**:
   ```bash
   pip install tflink
   ```

2. **It appears on PyPI**: https://pypi.org/project/tflink/

3. **Future updates are automatic**: Just create a GitHub Release!

## 📚 Full Documentation

- **GITHUB_PYPI_SETUP.md** - Detailed step-by-step guide
- **QUICK_DEPLOY.md** - Quick reference
- **PUBLISHING.md** - Publishing best practices

---

**Ready to start?** Begin with Step 1 - Register on TestPyPI!

Need help at any step? Check the full documentation or ask questions.
