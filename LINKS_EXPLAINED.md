# Understanding Download Links in tflink

When you upload a file using tflink, the API returns **two different download links**. This document explains the difference and when to use each one.

## The Two Links

### 1. `download_link` (Standard Link)

**Example:**
```
https://d.tmpfile.link/public/2025-07-31/a1b2c3d4-e5f6-7890-abcd-ef1234567890/example.png
```

**Characteristics:**
- Human-readable
- Contains regular forward slashes (`/`)
- Easier to read and understand
- Works perfectly in web browsers

**Use this link for:**
- ✅ Displaying to users in your UI
- ✅ Creating clickable HTML links
- ✅ Sending in emails or chat messages
- ✅ Sharing on social media
- ✅ Most common use cases

### 2. `download_link_encoded` (URL-Encoded Link)

**Example:**
```
https://d.tmpfile.link/public%2F2025-07-31%2Fa1b2c3d4-e5f6-7890-abcd-ef1234567890%2Fexample.png
```

**Characteristics:**
- URL-safe encoding
- Forward slashes encoded as `%2F`
- Safe for all contexts
- Guaranteed to work in strict URL parsers

**Use this link for:**
- ✅ Making API requests with the URL as a parameter
- ✅ Files with special characters in filenames
- ✅ Embedding in JSON, XML, or other data formats
- ✅ When interfacing with strict URL parsers
- ✅ Programmatic file downloads

## Key Points

### Both Links Work

Both links point to **the exact same file**. You can use either one to download the file. The only difference is how the URL path is encoded.

### Most Users Should Use `download_link`

For the vast majority of use cases, the standard `download_link` is the right choice. It's:
- Simpler
- More readable
- Works everywhere users expect

### When to Use `download_link_encoded`

Use the encoded version when you need absolute certainty about URL safety, such as:
- Passing the URL as a query parameter to another API
- Working with systems that strictly parse URLs
- Dealing with filenames containing special characters

## Code Examples

### Basic Usage (Most Common)

```python
from tflink import TFLinkClient

client = TFLinkClient()
result = client.upload('document.pdf')

# Use the standard link for most cases
print(f"Share this link: {result.download_link}")
```

### Display Both Links to Users

```python
from tflink import TFLinkClient

client = TFLinkClient()
result = client.upload('document.pdf')

print("Your file has been uploaded!")
print(f"Download link: {result.download_link}")
print(f"Alternative link: {result.download_link_encoded}")
```

### Using Encoded Link for API Calls

```python
from tflink import TFLinkClient
import requests

# Upload file
client = TFLinkClient()
result = client.upload('image.png')

# Pass encoded link to another API
api_url = "https://api.example.com/process"
response = requests.post(api_url, json={
    "image_url": result.download_link_encoded  # Use encoded for API safety
})
```

### Choosing Dynamically

```python
from tflink import TFLinkClient

def get_download_link(file_path, use_encoded=False):
    """Upload and return appropriate link"""
    client = TFLinkClient()
    result = client.upload(file_path)

    if use_encoded:
        return result.download_link_encoded
    return result.download_link

# For user display
user_link = get_download_link('photo.jpg', use_encoded=False)
print(f"Share this: {user_link}")

# For API integration
api_link = get_download_link('data.csv', use_encoded=True)
send_to_api(api_link)
```

## Technical Details

### URL Encoding Explained

URL encoding (also called percent-encoding) converts special characters into a format that can be safely transmitted in URLs.

**Common encodings:**
- Space ` ` → `%20`
- Forward slash `/` → `%2F`
- Question mark `?` → `%3F`
- Ampersand `&` → `%26`

In the case of tmpfile.link links:
- `download_link`: Uses literal forward slashes in the path
- `download_link_encoded`: Encodes path separators as `%2F`

### Why Two Links?

tmpfile.link provides both links for maximum compatibility:
1. **Standard link** - Works everywhere and is human-friendly
2. **Encoded link** - Provides extra safety for edge cases

## Best Practices

### ✅ DO:
- Use `download_link` by default
- Use `download_link_encoded` for API integrations
- Test both links if you're unsure
- Choose based on your specific use case

### ❌ DON'T:
- Manually encode `download_link` (use `download_link_encoded` instead)
- Assume one is "better" than the other (they're for different purposes)
- Mix up which one you're using in your code

## Summary

| Feature | `download_link` | `download_link_encoded` |
|---------|----------------|------------------------|
| Readability | ✅ High | ⚠️ Lower |
| Browser compatible | ✅ Yes | ✅ Yes |
| API-safe | ✅ Usually | ✅ Always |
| Default choice | ✅ Yes | ⚠️ Special cases |
| Use for users | ✅ Yes | ⚠️ Optional |
| Use for APIs | ✅ Usually fine | ✅ Guaranteed safe |

## Still Not Sure?

**Simple rule of thumb:**
- Showing link to a human? → Use `download_link`
- Passing link to a machine/API? → Consider `download_link_encoded`
- Not sure? → Use `download_link` (it works 99% of the time)

## Questions?

If you have questions about which link to use:
1. Check the examples in this document
2. Look at `examples/example_usage.py` in the tflink repository
3. When in doubt, use `download_link` (it's simpler and works great)

---

**Remember:** Both links point to the same file and both work. The choice is about which format is more appropriate for your use case!
