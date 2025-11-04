# API Reference

Complete API documentation for tflink.

## TFLinkClient

The main client class for uploading files to tmpfile.link.

### Constructor

```python
TFLinkClient(
    user_id: str | None = None,
    auth_token: str | None = None,
    base_url: str = "https://tmpfile.link",
    timeout: int = 300
)
```

**Parameters:**

- `user_id` (str, optional): User ID for authenticated uploads. Default: `None`
- `auth_token` (str, optional): Authentication token for authenticated uploads. Default: `None`
- `base_url` (str, optional): API base URL. Default: `"https://tmpfile.link"`
- `timeout` (int, optional): Request timeout in seconds. Default: `300` (5 minutes)

**Example:**

```python
from tflink import TFLinkClient

# Anonymous client
client = TFLinkClient()

# Authenticated client
client = TFLinkClient(
    user_id='YOUR_USER_ID',
    auth_token='YOUR_AUTH_TOKEN'
)

# Custom configuration
client = TFLinkClient(
    base_url='https://custom.tmpfile.link',
    timeout=600  # 10 minutes
)
```

### Methods

#### upload()

Upload a file to tmpfile.link.

```python
upload(
    file_path: str | Path,
    filename: str | None = None
) -> UploadResult
```

**Parameters:**

- `file_path` (str | Path): Path to the file to upload. Can be a string or `pathlib.Path` object.
- `filename` (str, optional): Custom filename for the uploaded file. If not provided, uses the original filename.

**Returns:**

- `UploadResult`: Object containing upload results and download links.

**Raises:**

- `FileNotFoundError`: File does not exist or is not a file
- `UploadError`: Upload failed (server error, invalid response)
- `AuthenticationError`: Authentication failed (invalid credentials)
- `NetworkError`: Network request failed (connection error, timeout)

**Example:**

```python
from tflink import TFLinkClient
from pathlib import Path

client = TFLinkClient()

# Upload with file path string
result = client.upload('document.pdf')

# Upload with Path object
result = client.upload(Path('document.pdf'))

# Upload with custom filename
result = client.upload('local.txt', filename='remote.txt')
```

#### is_authenticated()

Check if the client is configured with authentication credentials.

```python
is_authenticated() -> bool
```

**Returns:**

- `bool`: `True` if both `user_id` and `auth_token` are configured, `False` otherwise.

**Example:**

```python
client = TFLinkClient()
print(client.is_authenticated())  # False

client = TFLinkClient(user_id='123', auth_token='abc')
print(client.is_authenticated())  # True
```

## UploadResult

Result object returned by the `upload()` method.

### Attributes

#### file_name

```python
file_name: str
```

The name of the uploaded file.

**Example:**
```python
result = client.upload('document.pdf')
print(result.file_name)  # "document.pdf"
```

#### download_link

```python
download_link: str
```

Direct download URL (human-readable, unencoded).

**Format:** `https://d.tmpfile.link/public/2025-07-31/uuid/example.png`

**Use this for:**
- ✅ Display to users
- ✅ Clickable links
- ✅ Web browsers
- ✅ Emails and chat messages
- ✅ Social media sharing

**Example:**
```python
result = client.upload('photo.jpg')
print(f"Share this link: {result.download_link}")
```

#### download_link_encoded

```python
download_link_encoded: str
```

URL-encoded download link (safe for all contexts).

**Format:** `https://d.tmpfile.link/public%2F2025-07-31%2Fuuid%2Fexample.png`

**Use this for:**
- ✅ Programmatic access
- ✅ API calls with URL parameters
- ✅ Filenames with special characters
- ✅ Strict URL parsers
- ✅ JSON/XML embedding

**Example:**
```python
import requests

result = client.upload('data.csv')

# Pass to another API
response = requests.post('https://api.example.com/process', json={
    'file_url': result.download_link_encoded
})
```

#### size

```python
size: int
```

File size in bytes.

**Example:**
```python
result = client.upload('video.mp4')
print(f"Size: {result.size:,} bytes")  # Size: 1,234,567 bytes
print(f"Size: {result.size / 1024 / 1024:.2f} MB")  # Size: 1.18 MB
```

#### file_type

```python
file_type: str
```

MIME type of the uploaded file.

**Example:**
```python
result = client.upload('document.pdf')
print(result.file_type)  # "application/pdf"

result = client.upload('image.png')
print(result.file_type)  # "image/png"
```

#### uploaded_to

```python
uploaded_to: str
```

Upload destination.

**Values:**
- `"public"` - Anonymous upload (7-day expiry)
- `"user: USER_ID"` - Authenticated upload

**Example:**
```python
# Anonymous
client = TFLinkClient()
result = client.upload('file.txt')
print(result.uploaded_to)  # "public"

# Authenticated
client = TFLinkClient(user_id='123', auth_token='abc')
result = client.upload('file.txt')
print(result.uploaded_to)  # "user: 123"
```

## Exceptions

All exceptions inherit from `TFLinkError`.

### TFLinkError

Base exception class for all tflink errors.

```python
class TFLinkError(Exception):
    pass
```

### FileNotFoundError

Raised when the specified file does not exist or is not a file.

```python
class FileNotFoundError(TFLinkError):
    pass
```

**Example:**
```python
from tflink.exceptions import FileNotFoundError

try:
    result = client.upload('nonexistent.pdf')
except FileNotFoundError:
    print("File not found!")
```

### UploadError

Raised when the upload fails (server error, invalid response).

```python
class UploadError(TFLinkError):
    pass
```

**Example:**
```python
from tflink.exceptions import UploadError

try:
    result = client.upload('document.pdf')
except UploadError as e:
    print(f"Upload failed: {e}")
```

### AuthenticationError

Raised when authentication fails (invalid credentials).

```python
class AuthenticationError(TFLinkError):
    pass
```

**Example:**
```python
from tflink.exceptions import AuthenticationError

try:
    client = TFLinkClient(user_id='wrong', auth_token='invalid')
    result = client.upload('file.pdf')
except AuthenticationError:
    print("Invalid credentials!")
```

### NetworkError

Raised when a network request fails (connection error, timeout).

```python
class NetworkError(TFLinkError):
    pass
```

**Example:**
```python
from tflink.exceptions import NetworkError

try:
    result = client.upload('large_file.zip')
except NetworkError as e:
    print(f"Network error: {e}")
```

## Download Links Explained

### The Two Links

tflink provides two download links for every uploaded file:

| Link Type | Format | Use Case |
|-----------|--------|----------|
| `download_link` | `https://d.tmpfile.link/public/2025-07-31/uuid/file.pdf` | Human-readable, for users |
| `download_link_encoded` | `https://d.tmpfile.link/public%2F2025-07-31%2Fuuid%2Ffile.pdf` | URL-encoded, for APIs |

### Which One Should You Use?

**Simple rule of thumb:**
- Showing link to a human? → Use `download_link`
- Passing link to a machine/API? → Consider `download_link_encoded`
- Not sure? → Use `download_link` (it works 99% of the time)

### Both Links Work

Both links point to **the exact same file**. The only difference is URL encoding:

- `download_link`: Contains regular forward slashes (`/`)
- `download_link_encoded`: Forward slashes encoded as `%2F`

### Examples

#### For User Display

```python
from tflink import TFLinkClient

client = TFLinkClient()
result = client.upload('report.pdf')

# Show to user
print(f"Download: {result.download_link}")
```

#### For API Integration

```python
from tflink import TFLinkClient
import requests

client = TFLinkClient()
result = client.upload('data.json')

# Pass to API
api_response = requests.post('https://api.example.com/process', json={
    'file_url': result.download_link_encoded  # Use encoded for safety
})
```

#### Dynamic Choice

```python
def get_link(result, for_api=False):
    """Get appropriate link based on use case"""
    if for_api:
        return result.download_link_encoded
    return result.download_link

# For user
user_link = get_link(result, for_api=False)
print(f"Share: {user_link}")

# For API
api_link = get_link(result, for_api=True)
send_to_api(api_link)
```

## Complete Examples

### Basic Upload

```python
from tflink import TFLinkClient

client = TFLinkClient()
result = client.upload('document.pdf')

print(f"File: {result.file_name}")
print(f"Size: {result.size:,} bytes")
print(f"Type: {result.file_type}")
print(f"Link: {result.download_link}")
```

### Error Handling

```python
from tflink import TFLinkClient
from tflink.exceptions import (
    FileNotFoundError,
    UploadError,
    NetworkError,
    TFLinkError
)

client = TFLinkClient()

try:
    result = client.upload('document.pdf')
    print(f"Success: {result.download_link}")

except FileNotFoundError:
    print("File not found!")

except UploadError as e:
    print(f"Upload failed: {e}")

except NetworkError as e:
    print(f"Network error: {e}")

except TFLinkError as e:
    print(f"Unknown error: {e}")
```

### Batch Upload

```python
from tflink import TFLinkClient
from pathlib import Path

client = TFLinkClient()
results = []

files = ['file1.pdf', 'file2.doc', 'file3.txt']

for file in files:
    try:
        result = client.upload(file)
        results.append({
            'file': file,
            'link': result.download_link,
            'size': result.size
        })
        print(f"✓ {file}")
    except Exception as e:
        print(f"✗ {file}: {e}")

# Print summary
for item in results:
    print(f"{item['file']}: {item['link']} ({item['size']:,} bytes)")
```

### Authenticated Upload

```python
from tflink import TFLinkClient

client = TFLinkClient(
    user_id='YOUR_USER_ID',
    auth_token='YOUR_AUTH_TOKEN'
)

result = client.upload('important.pdf')

print(f"Uploaded to: {result.uploaded_to}")  # "user: YOUR_USER_ID"
print(f"Download: {result.download_link}")
```

## Type Hints

tflink is fully typed. You can use type checkers like mypy:

```python
from tflink import TFLinkClient, UploadResult
from pathlib import Path

client: TFLinkClient = TFLinkClient()

# Type checking works
file_path: Path = Path('document.pdf')
result: UploadResult = client.upload(file_path)

# Your IDE will provide autocomplete
link: str = result.download_link
size: int = result.size
```

## Constants

```python
from tflink import __version__, __author__, __license__

print(__version__)  # "0.1.0"
print(__author__)   # "tfLink"
print(__license__)  # "MIT"
```

## Next Steps

- [Getting Started Guide](getting-started.md) - Beginner-friendly guide
- [PyPI Project Page](https://pypi.org/project/tflink/) - Package information
- [GitHub Repository](https://github.com/tflink-tmpfile/tflink) - Source code
