# tflink

[![PyPI version](https://badge.fury.io/py/tflink.svg)](https://badge.fury.io/py/tflink)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tflink)](https://pypi.org/project/tflink/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tflink)](https://pypi.org/project/tflink/)
[![GitHub](https://img.shields.io/github/license/tflink-tmpfile/tflink)](https://github.com/tflink-tmpfile/tflink/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/tflink-tmpfile/tflink)](https://github.com/tflink-tmpfile/tflink/issues)

A simple and easy-to-use Python library for uploading files to [tmpfile.link](https://tmpfile.link) and retrieving download links.

**📦 [View on PyPI](https://pypi.org/project/tflink/) | 📖 [Documentation](docs/) | 🐛 [Report Issues](https://github.com/tflink-tmpfile/tflink/issues)**

## Features

- 🚀 **Simple API** - Upload files with just 3 lines of code
- 🔒 **Anonymous & Authenticated** - Support for both upload modes
- 📦 **Dual Download Links** - Standard and URL-encoded formats
- 🎯 **Type Hints** - Full type annotations for better IDE experience
- ✅ **Fully Tested** - Comprehensive test coverage
- 🐍 **Python 3.8+** - Modern Python support

## Quick Start

### Installation

```bash
pip install tflink
```

### Upload a File

```python
from tflink import TFLinkClient

# Create client and upload
client = TFLinkClient()
result = client.upload('document.pdf')

# Get download link
print(f"Download: {result.download_link}")
```

That's it! 🎉

## Examples

### Anonymous Upload

```python
from tflink import TFLinkClient

client = TFLinkClient()
result = client.upload('document.pdf')

print(f"File: {result.file_name}")
print(f"Size: {result.size:,} bytes")
print(f"Link: {result.download_link}")
```

### Authenticated Upload

```python
from tflink import TFLinkClient

client = TFLinkClient(
    user_id='YOUR_USER_ID',
    auth_token='YOUR_AUTH_TOKEN'
)

result = client.upload('document.pdf')
print(f"Download: {result.download_link}")
```

### Error Handling

```python
from tflink import TFLinkClient
from tflink.exceptions import TFLinkError

client = TFLinkClient()

try:
    result = client.upload('document.pdf')
    print(f"Success: {result.download_link}")
except TFLinkError as e:
    print(f"Error: {e}")
```

## Download Links

tflink provides two download link formats:

- **`download_link`** - Human-readable, perfect for sharing with users
- **`download_link_encoded`** - URL-safe, ideal for API integrations

```python
result = client.upload('file.pdf')

# For users
print(result.download_link)
# https://d.tmpfile.link/public/2025-07-31/uuid/file.pdf

# For APIs
print(result.download_link_encoded)
# https://d.tmpfile.link/public%2F2025-07-31%2Fuuid%2Ffile.pdf
```

Both links point to the same file. Use `download_link` for most cases.

## Documentation

- 📖 **[Getting Started Guide](docs/user-guide/getting-started.md)** - Detailed tutorials and examples
- 📚 **[API Reference](docs/user-guide/api-reference.md)** - Complete API documentation
- 🛠️ **[Developer Guide](docs/developer-guide/)** - For contributors and maintainers

## API Overview

### TFLinkClient

```python
TFLinkClient(
    user_id: str | None = None,
    auth_token: str | None = None,
    base_url: str = "https://tmpfile.link",
    timeout: int = 300
)
```

**Methods:**
- `upload(file_path, filename=None)` - Upload a file
- `is_authenticated()` - Check authentication status

### UploadResult

**Attributes:**
- `file_name` - Uploaded file name
- `download_link` - Standard download URL
- `download_link_encoded` - URL-encoded download URL
- `size` - File size in bytes
- `file_type` - MIME type
- `uploaded_to` - Upload destination

### Exceptions

- `TFLinkError` - Base exception
- `FileNotFoundError` - File not found
- `UploadError` - Upload failed
- `AuthenticationError` - Invalid credentials
- `NetworkError` - Network request failed

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
make test           # Run tests
make test-cov       # Run with coverage
make quick-test     # Quick functionality test
```

### Code Quality

```bash
make format         # Format code with black
make lint           # Run linters (flake8, mypy)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- **PyPI:** https://pypi.org/project/tflink/
- **GitHub:** https://github.com/tflink-tmpfile/tflink
- **Documentation:** [docs/](docs/)
- **tmpfile.link:** https://tmpfile.link
- **Issues:** https://github.com/tflink-tmpfile/tflink/issues
- **Email:** pypi@tmpfile.link

## Support

- 📧 Email: pypi@tmpfile.link
- 🐛 Issues: [GitHub Issues](https://github.com/tflink-tmpfile/tflink/issues)
- 📖 Docs: [Documentation](docs/)

---

Made with ❤️ for the tmpfile.link community
