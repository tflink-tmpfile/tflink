# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**tflink** is a Python client library for tmpfile.link file upload service. It provides a simple interface to upload files and retrieve download links, supporting both anonymous (7-day expiry) and authenticated uploads.

**Key constraint**: tmpfile.link only accepts files up to 100MB. The client validates file size **before upload** to save time and bandwidth.

## Development Commands

### Setup
```bash
make install-dev    # Install with dev dependencies
```

### Testing
```bash
make test           # Run all tests (24 tests)
pytest tests/test_client.py::TestTFLinkClientUpload::test_upload_file_too_large  # Run single test
make test-cov       # Run with coverage (target: >80%)
make quick-test     # Quick smoke test
```

### Code Quality
```bash
make format         # Black formatting (line-length: 100)
make lint           # flake8 + mypy checks
```

### Building
```bash
make build          # Build distribution packages
make clean          # Clean build artifacts
```

### Version Management & Release

**Automated workflow** (recommended):
```bash
# 1. Bump version (updates tflink/__init__.py and pyproject.toml automatically)
make version-minor  # 0.1.0 -> 0.2.0
make version-patch  # 0.1.0 -> 0.1.1
make version-major  # 0.1.0 -> 1.0.0

# 2. Push code and tags
make release

# 3. Wait for test.yml to pass on GitHub Actions
# 4. Create GitHub Release at the URL shown
# 5. publish.yml workflow auto-publishes to PyPI
```

**Version files to keep in sync**:
- `tflink/__init__.py`: `__version__ = '0.2.0'`
- `pyproject.toml`: `version = "0.2.0"`
- `pyproject.toml`: `[tool.mypy] python_version = "3.8"` (NOT the package version)

**Important**: The `bump_version.py` script handles syncing these files. Don't edit versions manually.

## Architecture

### Core Components

1. **TFLinkClient** (`tflink/client.py`):
   - Main API class
   - Constructor parameters:
     - `max_file_size`: Default 100MB (104857600 bytes)
     - `user_id` + `auth_token`: Optional for authenticated uploads
     - `base_url`: API endpoint (default: https://tmpfile.link)
     - `timeout`: Request timeout (default: 300s)
   - `upload()`: Validates file size locally before HTTP upload
   - `_handle_response()`: Processes API responses and errors

2. **UploadResult** (`tflink/models.py`):
   - Dataclass returned by `upload()`
   - Contains two link formats:
     - `download_link`: Human-readable (e.g., `https://d.tmpfile.link/public/2025-07-31/uuid/file.pdf`)
     - `download_link_encoded`: URL-encoded (e.g., `https://d.tmpfile.link/public%2F2025-07-31%2Fuuid%2Ffile.pdf`)
   - Both point to the same file; use `download_link` for most cases

3. **Exceptions** (`tflink/exceptions.py`):
   - Hierarchy: `TFLinkError` (base) → `UploadError`, `AuthenticationError`, `FileNotFoundError`, `NetworkError`
   - `UploadError` raised for file size violations (client-side check)

### File Size Validation

**Critical implementation detail**: File size is checked in `client.py` **before** opening the file for upload:

```python
# In upload() method:
file_size = file_path.stat().st_size
if file_size > self.max_file_size:
    raise UploadError(f"File too large: {size_mb:.2f}MB. Maximum allowed: {max_mb:.0f}MB")
```

This happens before the `with open(file_path, 'rb')` block to avoid wasting bandwidth.

### Testing Architecture

**Test structure** (`tests/`):
- `conftest.py`: Fixtures for mock response data
- `test_client.py`: 24 tests covering all client functionality
- `test_models.py`: UploadResult model tests

**When adding upload tests**: Always mock `Path.stat()` to simulate file sizes:
```python
@patch('tflink.client.Path.stat')
def test_something(self, mock_stat):
    mock_stat_result = Mock()
    mock_stat_result.st_size = 1024 * 1024  # 1MB
    mock_stat.return_value = mock_stat_result
```

## GitHub Actions Workflows

Two workflows in `.github/workflows/`:

1. **test.yml**: Runs on every push
   - Tests on Python 3.8-3.12 × Ubuntu/macOS/Windows
   - Does NOT publish to PyPI

2. **publish.yml**: Runs on GitHub Release creation
   - Builds and publishes to PyPI using `PYPI_API_TOKEN` secret
   - Does NOT run tests (assumes test.yml passed)

**Critical**: Always check test.yml passes before creating a GitHub Release.

## Documentation Structure

```
docs/
├── user-guide/
│   ├── getting-started.md  # User-facing tutorials
│   └── api-reference.md    # Complete API docs
└── developer-guide/
    ├── setup.md            # GitHub & PyPI setup
    └── release.md          # Release workflow guide
```

When adding features, update relevant docs in `docs/` and the main `README.md`.

## Common Pitfalls

1. **Version syncing**: Use `bump_version.py`, not manual edits. It updates both `__init__.py` and `pyproject.toml`.

2. **mypy config bug**: `[tool.mypy] python_version` should be `"3.8"`, NOT the package version.

3. **Test mocking**: New upload tests must mock `Path.stat()` due to file size validation.

4. **Release workflow**: Creating a GitHub Release triggers publish.yml. Don't manually run `make publish`.

5. **File size**: The 100MB limit is a tmpfile.link server constraint, not arbitrary. Client-side validation is a feature.

## Contact & Repository

- **Email**: pypi@tmpfile.link
- **GitHub**: https://github.com/tflink-tmpfile/tflink
- **PyPI**: https://pypi.org/project/tflink/
