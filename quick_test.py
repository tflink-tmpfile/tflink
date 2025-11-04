#!/usr/bin/env python3
"""
Quick Test Script - Verify tflink library functionality

This script will create a test file, upload it to tmpfile.link, and display the download link.
"""

import sys
from pathlib import Path

# Add current directory to Python path (for development testing)
sys.path.insert(0, str(Path(__file__).parent))

from tflink import TFLinkClient
from tflink.exceptions import TFLinkError


def main():
    """Run quick test"""
    print("=" * 70)
    print("tflink Quick Test")
    print("=" * 70)

    # Create test file
    test_file = Path("test_upload.txt")
    test_content = """
This is a test file for verifying tflink library functionality.

tflink is a Python library for uploading files to tmpfile.link and retrieving download links.

Test time: {time}
""".format(time=__import__('datetime').datetime.now().isoformat())

    print(f"\n1. Creating test file: {test_file.name}")
    test_file.write_text(test_content, encoding='utf-8')
    print(f"   File size: {test_file.stat().st_size} bytes")

    # Create client and upload
    print("\n2. Initializing tflink client (anonymous mode)")
    client = TFLinkClient()
    print(f"   {client}")

    try:
        print(f"\n3. Uploading file to tmpfile.link...")
        result = client.upload(test_file)

        print("\n" + "=" * 70)
        print("✓ Upload successful!")
        print("=" * 70)
        print(f"\nFile Information:")
        print(f"  File name:     {result.file_name}")
        print(f"  File size:     {result.size:,} bytes")
        print(f"  File type:     {result.file_type}")
        print(f"  Uploaded to:   {result.uploaded_to}")
        print(f"\nTwo download links (both point to the same file):")
        print(f"\n  1. Standard Link (human-readable, use this for most cases):")
        print(f"     {result.download_link}")
        print(f"\n  2. Encoded Link (URL-safe, use for APIs or special characters):")
        print(f"     {result.download_link_encoded}")
        print("\n" + "=" * 70)
        print("Note: Anonymous uploads are automatically deleted after 7 days")
        print("=" * 70)

        return 0

    except TFLinkError as e:
        print("\n" + "=" * 70)
        print("✗ Upload failed")
        print("=" * 70)
        print(f"\nError type: {type(e).__name__}")
        print(f"Error message: {e}")
        print("\nPossible causes:")
        print("  1. Network connection issues")
        print("  2. tmpfile.link service unavailable")
        print("  3. File size exceeds limit")
        print("\nSuggestions:")
        print("  - Check network connection")
        print("  - Try again later")
        print("  - Review detailed error message")
        return 1

    except Exception as e:
        print(f"\n✗ Unexpected error occurred: {e}")
        return 1

    finally:
        # Cleanup test file
        if test_file.exists():
            test_file.unlink()
            print(f"\n4. Cleaned up local test file: {test_file.name}")


if __name__ == "__main__":
    sys.exit(main())
