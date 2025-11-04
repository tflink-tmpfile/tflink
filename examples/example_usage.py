"""
tflink Usage Examples

This file demonstrates how to use the tflink library to upload files
"""

import sys
from pathlib import Path

# If running from examples directory, add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tflink import TFLinkClient
from tflink.exceptions import TFLinkError


def example_anonymous_upload():
    """Example: Anonymous file upload"""
    print("=" * 60)
    print("Example 1: Anonymous File Upload")
    print("=" * 60)

    # Create client (anonymous mode)
    client = TFLinkClient()
    print(f"Client mode: {client}")

    # Create a test file
    test_file = Path("test_file.txt")
    test_file.write_text("This is a test file to demonstrate tflink upload functionality.\n")

    try:
        # Upload file
        print(f"\nUploading file: {test_file.name}")
        result = client.upload(test_file)

        # Display results
        print(f"\n✓ Upload successful!")
        print(f"  File name: {result.file_name}")
        print(f"  File size: {result.size} bytes")
        print(f"  File type: {result.file_type}")
        print(f"  Uploaded to: {result.uploaded_to}")
        print(f"\n  Two download links are provided:")
        print(f"  1. Standard link (human-readable):")
        print(f"     {result.download_link}")
        print(f"  2. Encoded link (URL-safe):")
        print(f"     {result.download_link_encoded}")
        print(f"\n  Both links point to the same file. Use standard link for simplicity.")

    except TFLinkError as e:
        print(f"\n✗ Upload failed: {e}")

    finally:
        # Cleanup test file
        if test_file.exists():
            test_file.unlink()
            print(f"\nCleaned up test file: {test_file.name}")


def example_authenticated_upload():
    """Example: Authenticated file upload"""
    print("\n" + "=" * 60)
    print("Example 2: Authenticated File Upload")
    print("=" * 60)

    # Get authentication credentials from environment variables or config
    # Using placeholders here - replace with actual values for testing
    user_id = "YOUR_USER_ID"
    auth_token = "YOUR_AUTH_TOKEN"

    if user_id == "YOUR_USER_ID":
        print("\n⚠ Please set user_id and auth_token to test authenticated upload")
        print("  1. Register an account at tmpfile.link")
        print("  2. Get your User ID and Auth Token")
        print("  3. Replace the placeholders in the code")
        return

    # Create authenticated client
    client = TFLinkClient(user_id=user_id, auth_token=auth_token)
    print(f"Client mode: {client}")
    print(f"Authentication status: {client.is_authenticated()}")

    # Create test file
    test_file = Path("auth_test.txt")
    test_file.write_text("This is a test file for authenticated upload.\n")

    try:
        # Upload file
        print(f"\nUploading file: {test_file.name}")
        result = client.upload(test_file)

        # Display results
        print(f"\n✓ Upload successful!")
        print(f"  File name: {result.file_name}")
        print(f"  Download link: {result.download_link}")
        print(f"  Uploaded to: {result.uploaded_to}")

    except TFLinkError as e:
        print(f"\n✗ Upload failed: {e}")

    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
            print(f"\nCleaned up test file: {test_file.name}")


def example_custom_filename():
    """Example: Upload with custom filename"""
    print("\n" + "=" * 60)
    print("Example 3: Upload with Custom Filename")
    print("=" * 60)

    client = TFLinkClient()

    # Create test file
    test_file = Path("original_name.txt")
    test_file.write_text("Test file uploaded with custom filename.\n")

    try:
        # Upload with custom filename
        custom_name = "my_custom_filename.txt"
        print(f"\nUploading: {test_file.name} -> {custom_name}")

        result = client.upload(test_file, filename=custom_name)

        print(f"\n✓ Upload successful!")
        print(f"  Original file: {test_file.name}")
        print(f"  Upload filename: {result.file_name}")
        print(f"  Download link: {result.download_link}")

    except TFLinkError as e:
        print(f"\n✗ Upload failed: {e}")

    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
            print(f"\nCleaned up test file: {test_file.name}")


def example_link_types():
    """Example: Understanding the two types of download links"""
    print("\n" + "=" * 60)
    print("Example 4: Two Types of Download Links")
    print("=" * 60)

    client = TFLinkClient()

    # Create test file with special characters in name
    test_file = Path("test_file.txt")
    test_file.write_text("Demonstrating the difference between two link types.\n")

    try:
        print(f"\nUploading file: {test_file.name}")
        result = client.upload(test_file)

        print(f"\n✓ Upload successful!")
        print(f"\ntmpfile.link returns TWO download links:")

        print(f"\n1. download_link (Standard/Unencoded):")
        print(f"   {result.download_link}")
        print(f"   - Human-readable")
        print(f"   - Contains forward slashes (/)")
        print(f"   - Good for: displaying to users, clickable links")

        print(f"\n2. download_link_encoded (URL-Encoded):")
        print(f"   {result.download_link_encoded}")
        print(f"   - URL-safe encoding")
        print(f"   - Forward slashes encoded as %2F")
        print(f"   - Good for: API calls, programmatic access")

        print(f"\n📝 Key Points:")
        print(f"   • Both links point to the SAME file")
        print(f"   • Both links work in web browsers")
        print(f"   • For most cases, use download_link (simpler)")
        print(f"   • Use download_link_encoded when you need guaranteed URL safety")

        print(f"\n💡 Example Use Cases:")
        print(f"   download_link:")
        print(f"   - Showing link to users in UI")
        print(f"   - Sending in emails or messages")
        print(f"   - Creating clickable HTML links")
        print(f"\n   download_link_encoded:")
        print(f"   - Making API requests with the URL")
        print(f"   - Filenames with special characters")
        print(f"   - Embedding in JSON or XML")

    except TFLinkError as e:
        print(f"\n✗ Upload failed: {e}")

    finally:
        if test_file.exists():
            test_file.unlink()
            print(f"\nCleaned up test file: {test_file.name}")


def example_error_handling():
    """Example: Error handling"""
    print("\n" + "=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)

    from tflink.exceptions import (
        FileNotFoundError,
        UploadError,
        AuthenticationError,
        NetworkError,
    )

    client = TFLinkClient()

    # Try to upload non-existent file
    print("\nTest: Upload non-existent file")
    try:
        result = client.upload("nonexistent_file.txt")
    except FileNotFoundError as e:
        print(f"✓ Correctly caught exception: {type(e).__name__}")
        print(f"  Error message: {e}")

    # Test authentication error (using wrong credentials)
    print("\nTest: Authentication failure")
    try:
        bad_client = TFLinkClient(user_id="bad_user", auth_token="bad_token")

        # Create temporary file
        temp_file = Path("temp.txt")
        temp_file.write_text("Test content")

        result = bad_client.upload(temp_file)

    except AuthenticationError as e:
        print(f"✓ Correctly caught exception: {type(e).__name__}")
        print(f"  Error message: {e}")
    except Exception as e:
        # If server doesn't return 401, might get other errors
        print(f"Caught other exception: {type(e).__name__}: {e}")
    finally:
        if temp_file.exists():
            temp_file.unlink()


def main():
    """Run all examples"""
    print("\ntflink Usage Examples")
    print("=" * 60)

    # Run examples
    example_anonymous_upload()
    example_authenticated_upload()
    example_custom_filename()
    example_link_types()
    example_error_handling()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
