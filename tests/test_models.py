"""
Tests for tflink.models
"""

import pytest
from tflink.models import UploadResult


def test_upload_result_from_json(mock_response_data):
    """Test creating UploadResult from JSON"""
    result = UploadResult.from_json(mock_response_data)

    assert result.file_name == "test.txt"
    assert result.download_link == "https://d.tmpfile.link/public/2025-01-01/uuid-123/test.txt"
    assert result.size == 1024
    assert result.file_type == "text/plain"
    assert result.uploaded_to == "public"


def test_upload_result_str():
    """Test string representation"""
    result = UploadResult(
        file_name="test.txt",
        download_link="https://example.com/test.txt",
        download_link_encoded="https://example.com/test.txt",
        size=1024,
        file_type="text/plain",
        uploaded_to="public"
    )

    str_repr = str(result)
    assert "test.txt" in str_repr
    assert "https://example.com/test.txt" in str_repr


def test_upload_result_repr():
    """Test detailed representation"""
    result = UploadResult(
        file_name="test.txt",
        download_link="https://example.com/test.txt",
        download_link_encoded="https://example.com/test.txt",
        size=1024,
        file_type="text/plain",
        uploaded_to="public"
    )

    repr_str = repr(result)
    assert "test.txt" in repr_str
    assert "1024" in repr_str
    assert "text/plain" in repr_str


def test_upload_result_attributes():
    """Test all attributes are set correctly"""
    result = UploadResult(
        file_name="document.pdf",
        download_link="https://example.com/doc.pdf",
        download_link_encoded="https://example.com/doc.pdf",
        size=2048,
        file_type="application/pdf",
        uploaded_to="user: test_user"
    )

    assert result.file_name == "document.pdf"
    assert result.download_link == "https://example.com/doc.pdf"
    assert result.download_link_encoded == "https://example.com/doc.pdf"
    assert result.size == 2048
    assert result.file_type == "application/pdf"
    assert result.uploaded_to == "user: test_user"
