# Release Workflow - tflink

This document explains the correct workflow for releasing new versions of tflink.

## ✅ Current Status

- **v0.1.0**: ✅ Successfully published to PyPI
  - Published manually (first time)
  - GitHub Release created
  - Package is live: https://pypi.org/project/tflink/

## 🚀 Recommended Workflow (Automated)

For all future releases, use this workflow:

### Step 1: Update Version Number

Edit two files:

**tflink/__init__.py:**
```python
__version__ = '0.2.0'  # Change version here
```

**pyproject.toml:**
```toml
version = "0.2.0"  # Change version here
```

### Step 2: Update Changelog

Edit **README.md** and add to the Changelog section:

```markdown
## Changelog

### 0.2.0 (2025-01-XX)

- Added feature X
- Fixed bug Y
- Improved Z

### 0.1.0 (2025-01-04)

- Initial release
```

### Step 3: Commit and Push

```bash
# Add changes
git add tflink/__init__.py pyproject.toml README.md

# Commit
git commit -m "Bump version to 0.2.0

- Feature: Added X
- Fix: Fixed Y
- Improvement: Z"

# Push to GitHub
git push
```

### Step 4: Create GitHub Release (Triggers Auto-Publish)

**Option A: Via GitHub Web UI (Recommended)**

1. Go to: https://github.com/tflink-tmpfile/tflink/releases
2. Click **"Draft a new release"**
3. Click **"Choose a tag"** → Type `v0.2.0` → Click **"Create new tag: v0.2.0 on publish"**
4. Release title: `v0.2.0 - [Brief Description]`
5. Description (example):
   ```markdown
   ## 🚀 What's New in v0.2.0

   ### ✨ New Features
   - Added feature X
   - Added feature Y

   ### 🐛 Bug Fixes
   - Fixed issue with Z

   ### 📚 Documentation
   - Updated API documentation

   ### Installation
   ```bash
   pip install --upgrade tflink
   ```

   ### Full Changelog
   See [CHANGELOG.md](https://github.com/tflink-tmpfile/tflink/blob/main/README.md#changelog)
   ```
6. Click **"Publish release"**

**Option B: Via Command Line**

```bash
# Create and push tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0

# Then create release via GitHub web UI (or use GitHub CLI)
```

### Step 5: Verify Automatic Publishing

1. **Check GitHub Actions**:
   - Go to: https://github.com/tflink-tmpfile/tflink/actions
   - You'll see "Publish to PyPI" workflow running
   - Wait 1-2 minutes for completion
   - Check the logs to ensure success

2. **Verify on PyPI**:
   - Visit: https://pypi.org/project/tflink/
   - New version should appear within minutes

3. **Test Installation**:
   ```bash
   pip install --upgrade tflink
   python -c "import tflink; print(tflink.__version__)"
   # Should show: 0.2.0
   ```

## ⚠️ Important Rules

### DO ✅

1. **Always update version in both files**:
   - `tflink/__init__.py`
   - `pyproject.toml`

2. **Use semantic versioning**:
   - **Patch** (0.1.1): Bug fixes, minor changes
   - **Minor** (0.2.0): New features, backward compatible
   - **Major** (1.0.0): Breaking changes

3. **Create GitHub Release to trigger auto-publish**:
   - Tag format: `vX.Y.Z` (e.g., `v0.2.0`)
   - This triggers the GitHub Action

4. **Wait for GitHub Action to complete**:
   - Check Actions tab to ensure success
   - Don't manually upload if using auto-publish

### DON'T ❌

1. **Don't upload the same version twice**:
   - ❌ Manual upload + GitHub Release for same version = Error
   - ✅ Choose one method per version

2. **Don't skip version updates**:
   - Always update `__version__` and `version` in pyproject.toml

3. **Don't reuse version numbers**:
   - PyPI won't allow it
   - Even if you delete a release from GitHub, PyPI keeps it

## 🔄 Two Valid Workflows

### Workflow A: Fully Automated (Recommended) ⭐

```
Update version → Commit → Push → Create GitHub Release
                                        ↓
                                  Auto-publish to PyPI
```

**Pros:**
- ✅ Fully automated
- ✅ GitHub Release history
- ✅ CI/CD logs
- ✅ No manual errors

**When to use:** Regular releases, team projects

### Workflow B: Manual Upload

```
Update version → Build → Manual twine upload → Optional: Create GitHub Release
```

**Pros:**
- ✅ Full control
- ✅ Can review before upload
- ✅ See upload output directly

**When to use:**
- Testing new features
- Emergency hotfixes
- When GitHub Actions is down

**Important:** If you manually upload v0.2.0, don't create GitHub Release v0.2.0!

## 🐛 Troubleshooting

### Error: "File already exists"

**Cause:** Version already uploaded to PyPI

**Solution:**
```bash
# Increment version
# Edit tflink/__init__.py and pyproject.toml
__version__ = '0.2.1'

# Rebuild
rm -rf dist/
python -m build

# Upload again
twine upload dist/*  # Or create GitHub Release
```

### Error: "Invalid credentials"

**Cause:** PyPI token not set or expired

**Solution:**
1. Go to: https://pypi.org/manage/account/token/
2. Create new token
3. Update GitHub Secret: https://github.com/tflink-tmpfile/tflink/settings/secrets/actions
4. Update `PYPI_API_TOKEN` with new token

### GitHub Action Failed

**Check:**
1. Actions tab: https://github.com/tflink-tmpfile/tflink/actions
2. Click on failed workflow
3. Check logs for error details
4. Common issues:
   - Missing `PYPI_API_TOKEN` secret
   - Expired token
   - Version already exists on PyPI

## 📊 Version History Example

| Version | Date | Method | Status |
|---------|------|--------|--------|
| 0.1.0 | 2025-01-04 | Manual | ✅ Live |
| 0.2.0 | 2025-01-XX | Auto (GitHub Release) | 🎯 Next |
| 0.2.1 | 2025-01-XX | Auto (GitHub Release) | 📅 Future |

## 🎯 Quick Reference

### For Next Release (v0.2.0):

```bash
# 1. Update version in code
sed -i '' "s/__version__ = '0.1.0'/__version__ = '0.2.0'/g" tflink/__init__.py
sed -i '' 's/version = "0.1.0"/version = "0.2.0"/g' pyproject.toml

# 2. Commit and push
git add .
git commit -m "Bump version to 0.2.0"
git push

# 3. Create GitHub Release v0.2.0 via web UI
# GitHub Action will automatically publish to PyPI!
```

## 📚 Related Documentation

- **GITHUB_PYPI_SETUP.md** - Initial setup guide
- **NEXT_STEPS.md** - Step-by-step publishing guide
- **QUICK_DEPLOY.md** - Quick reference

---

**Remember:** For v0.2.0 and beyond, just create GitHub Release and let automation do the work! 🚀
