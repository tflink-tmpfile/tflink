# Getting Started with tflink

Welcome to **tflink** - a Python library for uploading files to tmpfile.link!

## What You Have

A complete, production-ready Python library with:

- ✅ Full functionality for file uploads to tmpfile.link
- ✅ Support for both anonymous and authenticated uploads
- ✅ Comprehensive error handling
- ✅ 23+ unit tests with mocking
- ✅ Complete English documentation
- ✅ Ready for PyPI publishing

## Project Structure

```
python-tflink/
├── tflink/              # Core library
│   ├── __init__.py     # Package initialization
│   ├── client.py       # TFLinkClient - main upload client
│   ├── models.py       # UploadResult data model
│   └── exceptions.py   # Custom exception classes
├── tests/              # Unit tests
│   ├── conftest.py     # pytest fixtures
│   ├── test_client.py  # Client tests (23 test cases)
│   └── test_models.py  # Model tests
├── examples/           # Usage examples
│   └── example_usage.py
├── .github/workflows/  # GitHub Actions CI/CD
│   ├── test.yml        # Automated testing
│   └── publish.yml     # Auto-publish to PyPI
├── pyproject.toml      # Project configuration
├── README.md           # Main documentation
├── PUBLISHING.md       # Publishing guide
├── LICENSE             # MIT License
├── Makefile            # Useful commands
└── quick_test.py       # Quick functionality test
```

## Quick Start

### 1. Set Up Your GitHub Repository

```bash
# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: tflink Python library for tmpfile.link"

# Add remote repository
git remote add origin https://github.com/tflink-tmpfile/tflink.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### 2. Personal Information (Already Updated)

The following files have been updated with tfLink contact information:

**pyproject.toml** (lines 13-17):
```toml
authors = [
    {name = "tfLink", email = "pypi@tmpfile.link"}
]
```

GitHub URLs point to: https://github.com/tflink-tmpfile/tflink

**tflink/__init__.py** (line 22):
```python
__author__ = 'tfLink'
```

**LICENSE** (line 3):
```
Copyright (c) 2025 tfLink (pypi@tmpfile.link)
```

If you need to customize these, you can edit the files accordingly.

### 3. Test Locally

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run unit tests
pytest

# Or use Makefile
make install-dev
make test

# Quick functionality test (uploads real file)
python quick_test.py
```

### 4. Usage Examples

**Anonymous Upload:**
```python
from tflink import TFLinkClient

client = TFLinkClient()
result = client.upload('document.pdf')
print(result.download_link)
```

**Authenticated Upload:**
```python
from tflink import TFLinkClient

client = TFLinkClient(
    user_id='YOUR_USER_ID',
    auth_token='YOUR_AUTH_TOKEN'
)
result = client.upload('document.pdf')
print(result.download_link)
```

**With Error Handling:**
```python
from tflink import TFLinkClient
from tflink.exceptions import TFLinkError

client = TFLinkClient()

try:
    result = client.upload('file.pdf')
    print(f"Success: {result.download_link}")
except TFLinkError as e:
    print(f"Error: {e}")
```

## Publishing to PyPI

### Prerequisites

1. Register accounts:
   - TestPyPI: https://test.pypi.org/account/register/
   - PyPI: https://pypi.org/account/register/

2. Create API tokens (Settings → API tokens)

3. (Optional) Configure `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

### Publishing Steps

```bash
# 1. Clean old builds
make clean

# 2. Build distribution
make build

# 3. Check package
twine check dist/*

# 4. Test on TestPyPI first (recommended)
make publish-test

# 5. Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ tflink

# 6. If all good, publish to production PyPI
make publish
```

### Alternative: Manual Publishing

```bash
# Build
python -m build

# Check
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Makefile Commands

```bash
make help          # Show all commands
make install       # Install library
make install-dev   # Install with dev dependencies
make test          # Run tests
make test-cov      # Run tests with coverage
make quick-test    # Quick functionality test
make format        # Format code with black
make lint          # Run code checks
make clean         # Clean build files
make build         # Build distribution
make publish-test  # Publish to TestPyPI
make publish       # Publish to PyPI
```

## GitHub Actions

Two workflows are configured:

1. **test.yml** - Automated Testing
   - Triggers on push and pull requests
   - Tests on Python 3.8-3.12
   - Tests on Linux, macOS, and Windows

2. **publish.yml** - Automated Publishing
   - Triggers on GitHub Release
   - Automatically builds and publishes to PyPI
   - Requires `PYPI_API_TOKEN` secret in GitHub repository settings

## Next Steps

1. ☐ Register GitHub account and create repository
2. ☐ Push code to GitHub (use: git remote add origin https://github.com/tflink-tmpfile/tflink.git)
3. ✅ Update personal information (name, email, URLs) - **Already completed!**
4. ☐ Test locally with `python quick_test.py`
5. ☐ Register PyPI and TestPyPI accounts
6. ☐ Create API tokens
7. ☐ Publish to TestPyPI for testing
8. ☐ Publish to production PyPI
9. ☐ Create GitHub Release (triggers auto-publish if configured)

## Resources

### Documentation
- **README.md** - Main documentation and API reference
- **LINKS_EXPLAINED.md** - Detailed explanation of download_link vs download_link_encoded
- **PUBLISHING.md** - Step-by-step publishing guide
- **examples/example_usage.py** - Working code examples

### External Links
- **tmpfile.link**: https://tmpfile.link
- **PyPI**: https://pypi.org
- **Python Packaging Guide**: https://packaging.python.org/
- **Semantic Versioning**: https://semver.org/

## Support

For issues or questions:
- Check `README.md` for usage documentation
- Check `PUBLISHING.md` for publishing guide
- Review example code in `examples/example_usage.py`
- Run `python quick_test.py` to verify installation

## License

MIT License - see `LICENSE` file for details.

---

**Congratulations! You now have a complete, professional Python library ready to publish!** 🎉
