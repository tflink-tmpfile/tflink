# Publishing Guide - tflink

This document provides detailed instructions on how to publish the tflink library to PyPI.

## Prerequisites

### 1. Register PyPI Accounts

Register accounts on the following websites:

- **TestPyPI** (testing environment): https://test.pypi.org/account/register/
- **PyPI** (production environment): https://pypi.org/account/register/

### 2. Create API Tokens

For secure package publishing, it's recommended to use API tokens:

1. Log in to PyPI
2. Visit account settings: https://pypi.org/manage/account/
3. Scroll to the "API tokens" section
4. Click "Add API token"
5. Give your token a name (e.g., "tflink-upload")
6. Select scope (recommend selecting entire account first, can restrict to specific project after first publish)
7. Copy the generated token (it will only be shown once!)

Save the token in a secure location. Format will be similar to: `pypi-AgEIcHlwaS5vcmc...`

### 3. Configure `.pypirc` (Optional but Recommended)

Create a `~/.pypirc` file in your home directory:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # Your PyPI token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEI...  # Your TestPyPI token
```

**Note:** Ensure this file has permissions set to `600` (only you can read/write):

```bash
chmod 600 ~/.pypirc
```

## Publishing Process

### Step 1: Update Version Number

Edit the version number in the following files:

- `pyproject.toml` - `version` field in the `[project]` section
- `tflink/__init__.py` - `__version__` variable

Ensure version numbers follow Semantic Versioning:
- **Patch version** (0.1.1): Backward-compatible bug fixes
- **Minor version** (0.2.0): Backward-compatible new features
- **Major version** (1.0.0): Breaking changes

### Step 2: Update README and CHANGELOG

Ensure README.md is up to date, and add change notes for the new version in the "Changelog" section at the bottom of README.md.

### Step 3: Run Tests

Always run all tests before publishing:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=tflink --cov-report=html

# Code format check
black tflink tests --check

# Type check
mypy tflink
```

Make sure all tests pass!

### Step 4: Clean Old Build Files

```bash
# Delete old build files
rm -rf build/ dist/ *.egg-info/
```

### Step 5: Build Distribution Package

```bash
# Install build tool (if not already installed)
pip install build

# Build distribution package
python -m build
```

This will create two files in the `dist/` directory:
- `tflink-X.Y.Z.tar.gz` (source distribution)
- `tflink-X.Y.Z-py3-none-any.whl` (wheel distribution)

### Step 6: Check Built Package

```bash
# Install twine (if not already installed)
pip install twine

# Check package integrity
twine check dist/*
```

You should see output similar to:
```
Checking dist/tflink-0.1.0.tar.gz: PASSED
Checking dist/tflink-0.1.0-py3-none-any.whl: PASSED
```

### Step 7: Upload to TestPyPI (Recommended to Test First)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*
```

If you haven't configured `.pypirc`, you can use command line arguments:

```bash
twine upload --repository testpypi -u __token__ -p YOUR_TESTPYPI_TOKEN dist/*
```

### Step 8: Test Installation from TestPyPI

```bash
# Create new virtual environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ tflink

# Test if it works properly
python -c "from tflink import TFLinkClient; print('Import successful!')"

# Exit virtual environment
deactivate

# Delete test environment
rm -rf test_env
```

### Step 9: Upload to Production PyPI

After confirming the package works properly on TestPyPI, upload to production PyPI:

```bash
# Upload to PyPI
twine upload dist/*
```

Or use command line arguments:

```bash
twine upload -u __token__ -p YOUR_PYPI_TOKEN dist/*
```

### Step 10: Verify Publication

1. Visit PyPI project page: https://pypi.org/project/tflink/
2. Check if version number is correct
3. Test installation:

```bash
# Create new virtual environment
python -m venv verify_env
source verify_env/bin/activate

# Install from production PyPI
pip install tflink

# Test
python -c "from tflink import TFLinkClient; print(TFLinkClient.__doc__)"

# Cleanup
deactivate
rm -rf verify_env
```

### Step 11: Tag and Push to Git

```bash
# Create git tag
git tag -a v0.1.0 -m "Release version 0.1.0"

# Push tag to remote repository
git push origin v0.1.0

# Or push all tags
git push --tags
```

### Step 12: Create GitHub Release (if using GitHub)

1. Visit your GitHub repository
2. Click "Releases" -> "Create a new release"
3. Select the tag you just created
4. Fill in Release title and description
5. Publish

## Common Issues

### Q: Upload shows "File already exists"

A: PyPI does not allow re-uploading the same version number. You need to:
1. Increment version number
2. Rebuild
3. Upload new version

### Q: How to delete published packages?

A: PyPI does not allow deleting published versions (only hiding them). If you discover serious issues:
1. Use the "yank" feature to mark that version as not recommended
2. Publish a fix version as soon as possible

```bash
# Mark version as yanked
# Need to do this manually on PyPI website
```

### Q: How to update package metadata?

A: Metadata (description, author, etc.) is stored in `pyproject.toml`. Updates need a new version to be published to take effect on PyPI.

### Q: Difference between TestPyPI and PyPI?

A:
- **TestPyPI**: For testing the publishing process, can test freely
- **PyPI**: Official production environment, once published cannot be undone

Recommend always testing on TestPyPI first.

## Quick Publishing Checklist

```bash
# 1. Update version number
# Edit pyproject.toml and tflink/__init__.py

# 2. Run tests
pytest

# 3. Clean
rm -rf build/ dist/ *.egg-info/

# 4. Build
python -m build

# 5. Check
twine check dist/*

# 6. Test upload (optional)
twine upload --repository testpypi dist/*

# 7. Production upload
twine upload dist/*

# 8. Tag
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push --tags
```

## Automated Publishing

Consider using GitHub Actions to automate the publishing process. Create `.github/workflows/publish.yml`:

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

Remember to add `PYPI_API_TOKEN` in GitHub repository Settings -> Secrets.

## Related Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help Documentation](https://pypi.org/help/)
- [Semantic Versioning Specification](https://semver.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
