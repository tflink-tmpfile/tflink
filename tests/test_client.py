"""
Tests for tflink.client
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path

from tflink import TFLinkClient, UploadResult
from tflink.exceptions import (
    UploadError,
    AuthenticationError,
    FileNotFoundError,
    NetworkError,
)


class TestTFLinkClientInit:
    """Tests for TFLinkClient initialization"""

    def test_init_anonymous(self):
        """Test initialization without credentials"""
        client = TFLinkClient()
        assert client.user_id is None
        assert client.auth_token is None
        assert client.base_url == "https://tmpfile.link"
        assert not client.is_authenticated()

    def test_init_authenticated(self):
        """Test initialization with credentials"""
        client = TFLinkClient(user_id="test_user", auth_token="test_token")
        assert client.user_id == "test_user"
        assert client.auth_token == "test_token"
        assert client.is_authenticated()

    def test_init_partial_credentials_raises_error(self):
        """Test that partial credentials raise ValueError"""
        with pytest.raises(ValueError):
            TFLinkClient(user_id="test_user")

        with pytest.raises(ValueError):
            TFLinkClient(auth_token="test_token")

    def test_init_custom_base_url(self):
        """Test initialization with custom base URL"""
        client = TFLinkClient(base_url="https://custom.example.com")
        assert client.base_url == "https://custom.example.com"
        assert client.upload_url == "https://custom.example.com/api/upload"

    def test_init_custom_timeout(self):
        """Test initialization with custom timeout"""
        client = TFLinkClient(timeout=600)
        assert client.timeout == 600


class TestTFLinkClientUpload:
    """Tests for upload functionality"""

    @patch('tflink.client.requests.post')
    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_upload_anonymous_success(
        self, mock_file, mock_stat, mock_is_file, mock_exists, mock_post, mock_response_data
    ):
        """Test successful anonymous upload"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size (1MB - within limit)
        mock_stat_result = Mock()
        mock_stat_result.st_size = 1024 * 1024
        mock_stat.return_value = mock_stat_result

        # Mock successful response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_post.return_value = mock_response

        client = TFLinkClient()
        result = client.upload('/tmp/test.txt')

        assert isinstance(result, UploadResult)
        assert result.file_name == "test.txt"
        assert result.download_link == mock_response_data['downloadLink']
        assert mock_post.called
        # Verify no auth headers
        call_kwargs = mock_post.call_args[1]
        assert 'X-User-Id' not in call_kwargs['headers']
        assert 'X-Auth-Token' not in call_kwargs['headers']

    @patch('tflink.client.requests.post')
    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_upload_authenticated_success(
        self, mock_file, mock_stat, mock_is_file, mock_exists, mock_post, auth_mock_response_data
    ):
        """Test successful authenticated upload"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size (1MB - within limit)
        mock_stat_result = Mock()
        mock_stat_result.st_size = 1024 * 1024
        mock_stat.return_value = mock_stat_result

        # Mock successful response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = auth_mock_response_data
        mock_post.return_value = mock_response

        client = TFLinkClient(user_id="test_user", auth_token="test_token")
        result = client.upload('/tmp/test.txt')

        assert isinstance(result, UploadResult)
        assert result.uploaded_to == "user: test_user"

        # Verify auth headers were sent
        call_kwargs = mock_post.call_args[1]
        assert call_kwargs['headers']['X-User-Id'] == "test_user"
        assert call_kwargs['headers']['X-Auth-Token'] == "test_token"

    @patch('tflink.client.Path.exists')
    def test_upload_file_not_found(self, mock_exists):
        """Test upload with non-existent file"""
        mock_exists.return_value = False

        client = TFLinkClient()
        with pytest.raises(FileNotFoundError):
            client.upload('/tmp/nonexistent.txt')

    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    def test_upload_path_is_not_file(self, mock_is_file, mock_exists):
        """Test upload with directory path"""
        mock_exists.return_value = True
        mock_is_file.return_value = False

        client = TFLinkClient()
        with pytest.raises(FileNotFoundError):
            client.upload('/tmp/')

    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    def test_upload_file_too_large(self, mock_stat, mock_is_file, mock_exists):
        """Test upload with file exceeding size limit"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size: 150MB (exceeds 100MB limit)
        mock_stat_result = Mock()
        mock_stat_result.st_size = 150 * 1024 * 1024
        mock_stat.return_value = mock_stat_result

        client = TFLinkClient()
        with pytest.raises(UploadError) as exc_info:
            client.upload('/tmp/large_file.zip')

        assert "File too large" in str(exc_info.value)
        assert "150.00MB" in str(exc_info.value)
        assert "100MB" in str(exc_info.value)

    @patch('tflink.client.requests.post')
    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_upload_file_within_size_limit(
        self, mock_file, mock_stat, mock_is_file, mock_exists, mock_post, mock_response_data
    ):
        """Test upload with file within size limit"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size: 50MB (within 100MB limit)
        mock_stat_result = Mock()
        mock_stat_result.st_size = 50 * 1024 * 1024
        mock_stat.return_value = mock_stat_result

        # Mock successful response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_post.return_value = mock_response

        client = TFLinkClient()
        result = client.upload('/tmp/test.txt')

        assert isinstance(result, UploadResult)
        assert mock_post.called

    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    def test_upload_custom_max_file_size(self, mock_stat, mock_is_file, mock_exists):
        """Test upload with custom maximum file size"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size: 50MB
        mock_stat_result = Mock()
        mock_stat_result.st_size = 50 * 1024 * 1024
        mock_stat.return_value = mock_stat_result

        # Client with 30MB limit
        client = TFLinkClient(max_file_size=30 * 1024 * 1024)

        with pytest.raises(UploadError) as exc_info:
            client.upload('/tmp/file.zip')

        assert "File too large" in str(exc_info.value)
        assert "50.00MB" in str(exc_info.value)
        assert "30MB" in str(exc_info.value)

    def test_init_default_max_file_size(self):
        """Test that default max file size is 100MB"""
        client = TFLinkClient()
        assert client.max_file_size == 100 * 1024 * 1024

    def test_init_custom_max_file_size(self):
        """Test initialization with custom max file size"""
        custom_size = 50 * 1024 * 1024
        client = TFLinkClient(max_file_size=custom_size)
        assert client.max_file_size == custom_size

    @patch('tflink.client.requests.post')
    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_upload_authentication_error(self, mock_file, mock_stat, mock_is_file, mock_exists, mock_post):
        """Test upload with authentication error"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size
        mock_stat_result = Mock()
        mock_stat_result.st_size = 1024 * 1024
        mock_stat.return_value = mock_stat_result

        # Mock 401 response
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        client = TFLinkClient(user_id="bad_user", auth_token="bad_token")
        with pytest.raises(AuthenticationError):
            client.upload('/tmp/test.txt')

    @patch('tflink.client.requests.post')
    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_upload_server_413_error(self, mock_file, mock_stat, mock_is_file, mock_exists, mock_post):
        """Test upload with server 413 error (file too large from server)"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size (1MB - within client limit)
        mock_stat_result = Mock()
        mock_stat_result.st_size = 1024 * 1024
        mock_stat.return_value = mock_stat_result

        # Mock 413 response from server
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 413
        mock_post.return_value = mock_response

        client = TFLinkClient()
        with pytest.raises(UploadError) as exc_info:
            client.upload('/tmp/large_file.bin')
        assert "too large" in str(exc_info.value).lower()

    @patch('tflink.client.requests.post')
    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_upload_server_error(self, mock_file, mock_stat, mock_is_file, mock_exists, mock_post):
        """Test upload with server error"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size
        mock_stat_result = Mock()
        mock_stat_result.st_size = 1024 * 1024
        mock_stat.return_value = mock_stat_result

        # Mock 500 response
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        client = TFLinkClient()
        with pytest.raises(UploadError) as exc_info:
            client.upload('/tmp/test.txt')
        assert "server error" in str(exc_info.value).lower()

    @patch('tflink.client.requests.post')
    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_upload_timeout(self, mock_file, mock_stat, mock_is_file, mock_exists, mock_post):
        """Test upload timeout"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size
        mock_stat_result = Mock()
        mock_stat_result.st_size = 1024 * 1024
        mock_stat.return_value = mock_stat_result

        import requests
        mock_post.side_effect = requests.exceptions.Timeout()

        client = TFLinkClient()
        with pytest.raises(NetworkError) as exc_info:
            client.upload('/tmp/test.txt')
        assert "timeout" in str(exc_info.value).lower()

    @patch('tflink.client.requests.post')
    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_upload_connection_error(self, mock_file, mock_stat, mock_is_file, mock_exists, mock_post):
        """Test upload connection error"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size
        mock_stat_result = Mock()
        mock_stat_result.st_size = 1024 * 1024
        mock_stat.return_value = mock_stat_result

        import requests
        mock_post.side_effect = requests.exceptions.ConnectionError("Network error")

        client = TFLinkClient()
        with pytest.raises(NetworkError) as exc_info:
            client.upload('/tmp/test.txt')
        assert "connection error" in str(exc_info.value).lower()

    @patch('tflink.client.requests.post')
    @patch('tflink.client.Path.exists')
    @patch('tflink.client.Path.is_file')
    @patch('tflink.client.Path.stat')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_upload_custom_filename(self, mock_file, mock_stat, mock_is_file, mock_exists, mock_post, mock_response_data):
        """Test upload with custom filename"""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock file size
        mock_stat_result = Mock()
        mock_stat_result.st_size = 1024 * 1024
        mock_stat.return_value = mock_stat_result

        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_post.return_value = mock_response

        client = TFLinkClient()
        result = client.upload('/tmp/test.txt', filename='custom_name.txt')

        # Verify custom filename was used in the upload
        call_args = mock_post.call_args[1]
        assert mock_post.called


class TestTFLinkClientHelpers:
    """Tests for helper methods"""

    def test_is_authenticated_true(self):
        """Test is_authenticated returns True for authenticated client"""
        client = TFLinkClient(user_id="test_user", auth_token="test_token")
        assert client.is_authenticated() is True

    def test_is_authenticated_false(self):
        """Test is_authenticated returns False for anonymous client"""
        client = TFLinkClient()
        assert client.is_authenticated() is False

    def test_repr_anonymous(self):
        """Test string representation for anonymous client"""
        client = TFLinkClient()
        repr_str = repr(client)
        assert "anonymous" in repr_str
        assert "https://tmpfile.link" in repr_str

    def test_repr_authenticated(self):
        """Test string representation for authenticated client"""
        client = TFLinkClient(user_id="test_user", auth_token="test_token")
        repr_str = repr(client)
        assert "authenticated" in repr_str
