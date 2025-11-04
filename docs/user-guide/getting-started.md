# Getting Started with tflink

This guide will help you get started with tflink, a Python library for uploading files to tmpfile.link.

## Installation

Install tflink using pip:

```bash
pip install tflink
```

## Quick Start

### Anonymous Upload (Simplest)

Files uploaded anonymously are automatically deleted after 7 days.

```python
from tflink import TFLinkClient

# Create client
client = TFLinkClient()

# Upload file
result = client.upload('document.pdf')

# Get download link
print(f"Download: {result.download_link}")
```

That's it! You'll get a download URL that you can share with anyone.

### Authenticated Upload

If you have a tmpfile.link account, you can upload files that won't be automatically deleted.

```python
from tflink import TFLinkClient

# Create authenticated client
client = TFLinkClient(
    user_id='YOUR_USER_ID',
    auth_token='YOUR_AUTH_TOKEN'
)

# Upload file
result = client.upload('document.pdf')

# Get download link
print(f"Download: {result.download_link}")
print(f"Uploaded to: {result.uploaded_to}")  # Shows "user: YOUR_USER_ID"
```

## Basic Examples

### Upload with Custom Filename

```python
from tflink import TFLinkClient

client = TFLinkClient()

# Upload with custom filename
result = client.upload('local_file.txt', filename='custom_name.txt')

print(f"Download: {result.download_link}")
print(f"Filename: {result.file_name}")  # Shows 'custom_name.txt'
```

### Get File Information

```python
from tflink import TFLinkClient

client = TFLinkClient()
result = client.upload('image.png')

# Access file information
print(f"File name: {result.file_name}")
print(f"File size: {result.size} bytes")
print(f"File type: {result.file_type}")
print(f"Download link: {result.download_link}")
print(f"Uploaded to: {result.uploaded_to}")
```

### Handle Errors

```python
from tflink import TFLinkClient
from tflink.exceptions import (
    TFLinkError,
    FileNotFoundError,
    UploadError,
    NetworkError
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
    print(f"Error: {e}")
```

## Understanding Download Links

tflink provides two types of download links:

```python
result = client.upload('document.pdf')

# Standard link (human-readable)
print(result.download_link)
# Example: https://d.tmpfile.link/public/2025-07-31/uuid/document.pdf

# Encoded link (URL-safe)
print(result.download_link_encoded)
# Example: https://d.tmpfile.link/public%2F2025-07-31%2Fuuid%2Fdocument.pdf
```

**Which one should you use?**
- **`download_link`** - Use this for most cases (simpler, works in browsers)
- **`download_link_encoded`** - Use when you need guaranteed URL safety

For detailed explanation, see [API Reference](api-reference.md#download-links).

## Complete Example

Here's a complete example showing best practices:

```python
from pathlib import Path
from tflink import TFLinkClient
from tflink.exceptions import TFLinkError

def upload_file(file_path, user_id=None, auth_token=None):
    """
    Upload a file to tmpfile.link

    Args:
        file_path: Path to file to upload
        user_id: Optional user ID for authenticated upload
        auth_token: Optional auth token for authenticated upload

    Returns:
        Download URL if successful, None otherwise
    """
    # Check if file exists
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        return None

    try:
        # Create client
        if user_id and auth_token:
            client = TFLinkClient(user_id=user_id, auth_token=auth_token)
            print(f"Uploading {path.name} (authenticated)...")
        else:
            client = TFLinkClient()
            print(f"Uploading {path.name} (anonymous, 7-day expiry)...")

        # Upload
        result = client.upload(file_path)

        # Display results
        print(f"✓ Upload successful!")
        print(f"  File: {result.file_name}")
        print(f"  Size: {result.size:,} bytes")
        print(f"  Type: {result.file_type}")
        print(f"  Download: {result.download_link}")

        return result.download_link

    except TFLinkError as e:
        print(f"✗ Upload failed: {e}")
        return None

# Example usage
if __name__ == '__main__':
    # Anonymous upload
    url = upload_file('document.pdf')

    # Authenticated upload
    # url = upload_file('document.pdf',
    #                   user_id='YOUR_USER_ID',
    #                   auth_token='YOUR_TOKEN')
```

## Configuration Options

### Client Configuration

```python
from tflink import TFLinkClient

client = TFLinkClient(
    user_id='YOUR_USER_ID',        # Optional: For authenticated uploads
    auth_token='YOUR_AUTH_TOKEN',  # Optional: For authenticated uploads
    base_url='https://tmpfile.link',  # Optional: Custom API URL
    timeout=300                     # Optional: Request timeout in seconds
)
```

### Check Authentication Status

```python
client = TFLinkClient()
print(client.is_authenticated())  # False

client = TFLinkClient(user_id='123', auth_token='abc')
print(client.is_authenticated())  # True
```

## Common Use Cases

### 1. Share Large Files

```python
from tflink import TFLinkClient

client = TFLinkClient()
result = client.upload('large_video.mp4')

print(f"Share this link: {result.download_link}")
```

### 2. Backup Files

```python
from tflink import TFLinkClient
from pathlib import Path

client = TFLinkClient(user_id='YOUR_ID', auth_token='YOUR_TOKEN')

backup_dir = Path('backups')
for file in backup_dir.glob('*.zip'):
    result = client.upload(file)
    print(f"Backed up: {file.name} -> {result.download_link}")
```

### 3. Batch Upload

```python
from tflink import TFLinkClient
from pathlib import Path

client = TFLinkClient()

files = ['file1.pdf', 'file2.doc', 'file3.xlsx']
links = []

for file in files:
    try:
        result = client.upload(file)
        links.append({
            'file': file,
            'link': result.download_link,
            'size': result.size
        })
    except Exception as e:
        print(f"Failed to upload {file}: {e}")

# Print summary
for item in links:
    print(f"{item['file']}: {item['link']}")
```

## Next Steps

- [API Reference](api-reference.md) - Detailed API documentation
- [Python API Documentation](https://pypi.org/project/tflink/) - PyPI page
- [tmpfile.link](https://tmpfile.link) - Official website

## Getting Help

- **GitHub Issues**: https://github.com/tflink-tmpfile/tflink/issues
- **Email**: pypi@tmpfile.link

## Tips

1. **Anonymous uploads expire after 7 days** - Use authenticated uploads for permanent storage
2. **Check file size limits** - tmpfile.link may have upload size limits
3. **Handle errors gracefully** - Always use try-except blocks
4. **Use Path objects** - More reliable than string paths
5. **Test with small files first** - Verify everything works before uploading large files
