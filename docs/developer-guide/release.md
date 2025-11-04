# Release Guide

Complete guide for releasing new versions of tflink to PyPI.

## 🎯 Quick Release (3 Steps)

```bash
# 1. Bump version (automatically updates files, commits, and tags)
make version-minor  # or version-patch, version-major

# 2. Push everything
make release

# 3. Wait for tests to pass, then create GitHub Release
# Visit: https://github.com/tflink-tmpfile/tflink/actions
# After tests pass: Click the link shown in terminal
```

**That's it!** GitHub Actions will automatically publish to PyPI.

## 📚 Semantic Versioning

Choose the right version bump type:

| Command | Current | New | When to Use |
|---------|---------|-----|-------------|
| `make version-patch` | 0.1.0 | 0.1.1 | Bug fixes, small changes |
| `make version-minor` | 0.1.0 | 0.2.0 | New features, backward compatible |
| `make version-major` | 0.1.0 | 1.0.0 | Breaking changes |

## 🚀 Complete Release Workflow

### Step 1: Update Version

```bash
make version-minor
```

**What it does automatically:**
1. ✅ Reads current version from `tflink/__init__.py`
2. ✅ Calculates new version
3. ✅ Asks for confirmation
4. ✅ Updates `tflink/__init__.py`
5. ✅ Updates `pyproject.toml`
6. ✅ Creates git commit
7. ✅ Creates git tag (e.g., `v0.2.0`)

**Example output:**
```
📌 Current version: 0.1.0
🎯 New version: 0.2.0

❓ Update version from 0.1.0 to 0.2.0? [y/N]: y

📝 Updating files...
   ✓ Updated: tflink/__init__.py
   ✓ Updated: pyproject.toml

❓ Create git commit and tag? [Y/n]: y

📝 Git operations:
   ✓ Staged: tflink/__init__.py
   ✓ Staged: pyproject.toml
   ✓ Committed: Bump version to 0.2.0
   ✓ Tagged: v0.2.0

✅ Version bump complete!
```

### Step 2: Push to GitHub

```bash
make release
```

**What it does:**
1. ✅ Pushes code to GitHub
2. ✅ Pushes tag to GitHub
3. ✅ Triggers test.yml workflow
4. ✅ Shows GitHub Release link

**Output:**
```
🚀 Starting release process...

✓ Code pushed
✓ Pushing tag v0.2.0...

✅ Release ready!

📋 Next: Create GitHub Release at:
   https://github.com/tflink-tmpfile/tflink/releases/new?tag=v0.2.0
```

### Step 3: ⚠️ Wait for Tests to Pass

**IMPORTANT:** Before creating the GitHub Release:

1. Visit: https://github.com/tflink-tmpfile/tflink/actions
2. Wait for "Tests" workflow to complete (1-3 minutes)
3. Verify all tests pass (green ✓) on all Python versions (3.8-3.12)
4. Only proceed if tests pass

**Why wait?**
- Prevents publishing broken versions to PyPI
- Tests run on multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
- Tests run on multiple platforms (Ubuntu, macOS, Windows)

### Step 4: Create GitHub Release

1. Click the link from Step 2 (or visit manually)
2. The tag `v0.2.0` is already selected
3. Click **"Generate release notes"** (auto-fills from commits)
4. Edit the description if needed
5. Click **"Publish release"**

**GitHub Actions will automatically:**
- ✅ Build the package
- ✅ Upload to PyPI
- ✅ Update PyPI project page

Wait 1-2 minutes, then check: https://pypi.org/project/tflink/

## 🎬 Complete Example

Real-world example of releasing v0.2.0:

```bash
# Start with current version 0.1.0
$ python -c "import tflink; print(tflink.__version__)"
0.1.0

# Bump version (choose minor for new features)
$ make version-minor
📌 Current version: 0.1.0
🎯 New version: 0.2.0

❓ Update version from 0.1.0 to 0.2.0? [y/N]: y
# ... (updates files, commits, tags)
✅ Version bump complete!

# Verify the change
$ python -c "import tflink; print(tflink.__version__)"
0.2.0

# Push everything
$ make release
🚀 Starting release process...
✓ Code pushed
✓ Pushing tag v0.2.0...
✅ Release ready!

📋 Next: Create GitHub Release at:
   https://github.com/tflink-tmpfile/tflink/releases/new?tag=v0.2.0

# ⚠️ IMPORTANT: Check tests before creating release!
# 1. Visit: https://github.com/tflink-tmpfile/tflink/actions
# 2. Wait for "Tests" workflow to complete (1-3 minutes)
# 3. Ensure all tests pass (green ✓) on all Python versions
# 4. Only if tests pass, create GitHub Release
#    → This triggers automatic PyPI publishing

# Open browser, verify tests passed, create release
# GitHub Actions automatically publishes to PyPI!

# Verify on PyPI (wait 1-2 minutes)
$ pip install --upgrade tflink
$ python -c "import tflink; print(tflink.__version__)"
0.2.0
```

## 🔧 Manual Control Options

### Option 1: Use Python Script Directly

```bash
# Bump to specific version
python bump_version.py 0.3.0

# Or use bump type
python bump_version.py patch
python bump_version.py minor
python bump_version.py major
```

### Option 2: Skip Auto-commit

```bash
# Update files only (no git operations)
python bump_version.py minor
# When asked "Create git commit and tag?", answer: n

# Then manually review and commit
git diff
git add tflink/__init__.py pyproject.toml
git commit -m "Bump version to 0.2.0"
git tag -a v0.2.0 -m "Release 0.2.0"
```

## 🎓 Best Practices

1. **Test before release**:
   ```bash
   make test
   python quick_test.py
   ```

2. **Use meaningful version bumps**:
   - Patch (0.1.1): Bug fixes only
   - Minor (0.2.0): New features
   - Major (1.0.0): Breaking changes

3. **Document changes**:
   - Update CHANGELOG.md
   - Write detailed GitHub Release notes

4. **Check before pushing**:
   ```bash
   git show  # Review changes
   git log --oneline -5  # Check recent commits
   ```

5. **⭐ Wait for test.yml before creating Release**:
   - After `make release`, GitHub Actions automatically runs tests
   - Visit: https://github.com/tflink-tmpfile/tflink/actions
   - Wait 1-3 minutes for all tests to complete
   - ✅ All green? Create GitHub Release → Auto-publish to PyPI
   - ❌ Any red? Fix issues first, don't create Release yet
   - **Why?** This prevents publishing broken versions to PyPI

## 📊 Comparison: Manual vs Automated

| Task | Manual | Automated | Time Saved |
|------|--------|-----------|------------|
| Update __init__.py | Edit file | ✅ Auto | 30s |
| Update pyproject.toml | Edit file | ✅ Auto | 30s |
| Git commit | Type command | ✅ Auto | 20s |
| Git tag | Type command | ✅ Auto | 20s |
| Git push | 2 commands | ✅ 1 command | 30s |
| **Total** | ~5 minutes | **~30 seconds** | **90% faster** |

## 🔄 GitHub Actions Workflows

### test.yml - Runs on Every Push

```yaml
on:
  push:
    branches: [ main, develop ]
```

**What it does:**
- ✅ Runs tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
- ✅ Tests on Ubuntu, macOS, Windows
- ✅ Generates coverage report
- ❌ Does NOT publish to PyPI

### publish.yml - Runs on GitHub Release

```yaml
on:
  release:
    types: [published]
```

**What it does:**
- ✅ Builds the package
- ✅ Publishes to PyPI
- ❌ Does NOT run tests (assumes test.yml passed)

## ⚠️ Important Rules

### DO ✅

1. **Always test before creating Release**
2. **Wait for test.yml to complete** before creating GitHub Release
3. **Use semantic versioning** (MAJOR.MINOR.PATCH)
4. **Update CHANGELOG.md** with changes

### DON'T ❌

1. **Don't create GitHub Release if tests fail**
2. **Don't upload the same version twice**
   - PyPI doesn't allow it
   - Choose either manual OR automated, not both
3. **Don't skip version updates** in both files
4. **Don't reuse version numbers**

## 🆘 Troubleshooting

### "No changes made to file"

**Cause:** Version already exists in file

**Solution:** Check current version, you might have already bumped it

### "Git operation failed"

**Cause:** Not in a git repository or uncommitted changes

**Solution:**
```bash
git status  # Check status
git add .   # Stage changes
```

### "Version format error"

**Cause:** Invalid version format

**Solution:** Use format X.Y.Z (e.g., 0.2.0, 1.0.0)

### GitHub Action Failed: "File already exists"

**Cause:** Version already uploaded to PyPI

**Solution:**
```bash
# Increment version
python bump_version.py patch  # 0.2.0 → 0.2.1

# Push again
make release

# Create GitHub Release with new version
```

### GitHub Action Failed: "Invalid credentials"

**Cause:** PyPI token not set or expired

**Solution:**
1. Go to: https://pypi.org/manage/account/token/
2. Create new token
3. Update GitHub Secret: https://github.com/tflink-tmpfile/tflink/settings/secrets/actions
4. Update `PYPI_API_TOKEN` with new token

## 🚀 Quick Reference

```bash
# Complete release in 3 steps:
make version-minor          # Update version
make release               # Push to GitHub
# Wait for tests → Create GitHub Release → Auto-publish to PyPI

# Or step by step:
python bump_version.py minor   # Bump version
git push                       # Push code
git push origin v0.2.0         # Push tag
# Wait for tests → Create GitHub Release

# Verify:
git describe --tags           # Check current tag
python -c "import tflink; print(tflink.__version__)"  # Check version
```

## 📖 Related Documentation

- [Setup Guide](setup.md) - Initial GitHub & PyPI setup
- [Getting Started](../user-guide/getting-started.md) - User guide
- [CHANGELOG.md](../../CHANGELOG.md) - Version history

---

**Remember:** Version bump + Wait for tests + Create GitHub Release = Automatic PyPI publish! 🎉
