# Changelog

All notable changes to tflink will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-04

### Added
- Initial release of tflink
- Support for anonymous file uploads (7-day expiry)
- Support for authenticated file uploads with user ID and auth token
- Two download link formats: standard and URL-encoded
- Complete error handling with custom exception classes
- Full type hints support for better IDE experience
- Comprehensive test suite with 20+ test cases
- GitHub Actions CI/CD for automated testing and publishing
- Automated version bumping tool (bump_version.py)
- Documentation for users and developers

### Features
- `TFLinkClient` class for file uploads
- `UploadResult` dataclass with file information and download links
- Custom exceptions: `TFLinkError`, `UploadError`, `AuthenticationError`, `FileNotFoundError`, `NetworkError`
- Support for custom filenames
- Configurable timeout and base URL
- Python 3.8+ support

### Documentation
- Comprehensive README with examples
- Getting Started guide
- API Reference documentation
- Developer Setup guide
- Release workflow documentation

### Testing
- Unit tests for client, models, and exceptions
- Integration tests for upload functionality
- Test coverage across Python 3.8, 3.9, 3.10, 3.11, 3.12
- Cross-platform testing (Ubuntu, macOS, Windows)

## [Unreleased]

### Added
- Client-side file size validation before upload (default: 100MB)
- Configurable `max_file_size` parameter in `TFLinkClient`
- Files exceeding size limit are rejected before upload to save time and bandwidth
- Comprehensive error messages showing file size and limit

### Changed
- Reorganized documentation into docs/ directory structure
- Created comprehensive documentation index
- Added detailed API reference
- Improved release workflow documentation
- Updated all documentation to include file size limit information

### Fixed
- Files larger than 100MB are now rejected immediately instead of after upload attempt

---

## Version History

- **0.1.0** (2025-01-04) - Initial release

[0.1.0]: https://github.com/tflink-tmpfile/tflink/releases/tag/v0.1.0
[Unreleased]: https://github.com/tflink-tmpfile/tflink/compare/v0.1.0...HEAD
