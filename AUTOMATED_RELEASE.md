# Automated Release Guide

This guide shows you how to release new versions with **minimal manual work**.

## 🎯 Quick Release (3 Commands)

```bash
# 1. Bump version (automatically updates files, commits, and tags)
make version-minor  # or version-patch, version-major

# 2. Push everything
make release

# 3. Create GitHub Release (opens browser)
# Click the link shown in terminal
```

**That's it!** GitHub Actions will automatically publish to PyPI.

## 📚 Detailed Workflow

### Step 1: Choose Version Bump Type

Use semantic versioning:

| Command | Current | New | When to Use |
|---------|---------|-----|-------------|
| `make version-patch` | 0.1.0 | 0.1.1 | Bug fixes, small changes |
| `make version-minor` | 0.1.0 | 0.2.0 | New features, backward compatible |
| `make version-major` | 0.1.0 | 1.0.0 | Breaking changes |

### Step 2: Run Version Bump

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

**Output example:**
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

📋 Next steps:
   1. Review changes: git show
   2. Push code: git push
   3. Push tag: git push origin v0.2.0
   4. Create GitHub Release for v0.2.0
   5. GitHub Actions will auto-publish to PyPI!
```

### Step 3: Push to GitHub

```bash
make release
```

**What it does:**
1. ✅ Pushes code to GitHub
2. ✅ Pushes tag to GitHub
3. ✅ Shows GitHub Release link

**Output:**
```
🚀 Starting release process...

✓ Code pushed
✓ Pushing tag v0.2.0...

✅ Release ready!

📋 Next: Create GitHub Release at:
   https://github.com/tflink-tmpfile/tflink/releases/new?tag=v0.2.0
```

### Step 4: Create GitHub Release

1. Click the link from Step 3 (or visit manually)
2. The tag `v0.2.0` is already selected
3. Click **"Generate release notes"** (auto-fills from commits)
4. Edit the description if needed
5. Click **"Publish release"**

**GitHub Actions will automatically:**
- ✅ Build the package
- ✅ Upload to PyPI
- ✅ Update PyPI project page

Wait 1-2 minutes, then check: https://pypi.org/project/tflink/

## 🛠️ Manual Control Options

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

### Option 3: Manual Everything (Not Recommended)

```bash
# 1. Edit tflink/__init__.py
__version__ = '0.2.0'

# 2. Edit pyproject.toml
version = "0.2.0"

# 3. Commit and tag
git add .
git commit -m "Bump version to 0.2.0"
git tag -a v0.2.0 -m "Release 0.2.0"
git push && git push origin v0.2.0
```

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

# Open browser, create release
# GitHub Actions automatically publishes to PyPI!

# Verify on PyPI (wait 1-2 minutes)
$ pip install --upgrade tflink
$ python -c "import tflink; print(tflink.__version__)"
0.2.0
```

## 📊 Comparison: Manual vs Automated

| Task | Manual | Automated | Time Saved |
|------|--------|-----------|------------|
| Update __init__.py | Edit file | ✅ Auto | 30s |
| Update pyproject.toml | Edit file | ✅ Auto | 30s |
| Git commit | Type command | ✅ Auto | 20s |
| Git tag | Type command | ✅ Auto | 20s |
| Git push | 2 commands | ✅ 1 command | 30s |
| **Total** | ~5 minutes | **~30 seconds** | **90% faster** |

## 🔧 Tools Reference

### bump_version.py

The core automation script.

**Features:**
- ✅ Semantic version bumping
- ✅ Updates multiple files
- ✅ Git integration
- ✅ Interactive confirmation
- ✅ Error checking

**Usage:**
```bash
python bump_version.py patch   # 0.1.0 -> 0.1.1
python bump_version.py minor   # 0.1.0 -> 0.2.0
python bump_version.py major   # 0.1.0 -> 1.0.0
python bump_version.py 0.3.5   # Set specific version
```

### Makefile Commands

**Version Management:**
```bash
make version-patch    # Bump patch version
make version-minor    # Bump minor version
make version-major    # Bump major version
make release          # Push code and tags
```

**Development:**
```bash
make install-dev      # Install for development
make test             # Run tests
make format           # Format code
make lint             # Check code quality
```

**Publishing:**
```bash
make build            # Build package
make publish-test     # Upload to TestPyPI
make publish          # Upload to PyPI (not recommended, use GitHub Release)
```

## ⚠️ Important Notes

1. **Always test before releasing**:
   ```bash
   make test
   ```

2. **Version numbers are permanent**:
   - Can't delete from PyPI
   - Can't reuse version numbers
   - Always increment forward

3. **Use GitHub Release for publishing**:
   - ✅ Creates release notes
   - ✅ Automatic via GitHub Actions
   - ✅ Traceable history
   - ❌ Don't use `make publish` directly

4. **Check GitHub Actions**:
   - After creating release, check: https://github.com/tflink-tmpfile/tflink/actions
   - Ensure workflow completes successfully
   - Check logs if it fails

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
   - Update README.md changelog
   - Write detailed GitHub Release notes

4. **Check before pushing**:
   ```bash
   git show  # Review changes
   git log --oneline -5  # Check recent commits
   ```

## 🚀 Quick Reference Card

```bash
# Complete release in 3 commands:
make version-minor          # Update version
make release               # Push to GitHub
# Create GitHub Release → Auto-publish to PyPI

# Or step by step:
python bump_version.py minor   # Bump version
git push                       # Push code
git push origin v0.2.0         # Push tag
# Create GitHub Release

# Verify:
git describe --tags           # Check current tag
python -c "import tflink; print(tflink.__version__)"  # Check version
```

## 📖 See Also

- **RELEASE_WORKFLOW.md** - Detailed release workflow
- **GITHUB_PYPI_SETUP.md** - Initial setup guide
- **Makefile** - All available commands

---

**Remember:** Version bump + Create GitHub Release = Automatic PyPI publish! 🎉
