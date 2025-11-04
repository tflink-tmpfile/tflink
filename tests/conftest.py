"""
Pytest configuration and fixtures
"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_file():
    """Create a temporary file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write('This is a test file for tflink upload')
        temp_path = f.name

    yield Path(temp_path)

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def mock_response_data():
    """Sample API response data"""
    return {
        "fileName": "test.txt",
        "downloadLink": "https://d.tmpfile.link/public/2025-01-01/uuid-123/test.txt",
        "downloadLinkEncoded": "https://d.tmpfile.link/public%2F2025-01-01%2Fuuid-123%2Ftest.txt",
        "size": 1024,
        "type": "text/plain",
        "uploadedTo": "public"
    }


@pytest.fixture
def auth_mock_response_data():
    """Sample API response data for authenticated upload"""
    return {
        "fileName": "test.txt",
        "downloadLink": "https://d.tmpfile.link/users/test_user/2025-01-01/uuid-456/test.txt",
        "downloadLinkEncoded": "https://d.tmpfile.link/users%2Ftest_user%2F2025-01-01%2Fuuid-456%2Ftest.txt",
        "size": 1024,
        "type": "text/plain",
        "uploadedTo": "user: test_user"
    }
