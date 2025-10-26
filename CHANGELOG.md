# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-26

### Added
- Initial release of DeepSeek OCR web application
- FastAPI backend with OCR processing endpoints
- Modern web interface with drag-and-drop file upload
- **Progress bar for model download** with real-time updates
- **Demo mode** to test interface without downloading model
- Multiple OCR modes: Free OCR, Markdown, Grounding, Parse Figure, Detailed
- Docker Compose deployment setup
- GPU acceleration support (NVIDIA CUDA 11.8+)
- Health check endpoints
- API documentation with Swagger/OpenAPI
- Comprehensive project documentation
- Test script for API validation

### Features
- Real-time model download progress tracking
- Manual model download trigger button
- Background model loading
- Image preview before processing
- Result copying and downloading
- Responsive web design
- Error handling and user feedback
- Multiple OCR processing modes with custom prompts

### Documentation
- README with quick start guide
- LICENSE (MIT - Development and Testing Only)
- CONTRIBUTING guidelines
- CODE_OF_CONDUCT
- SECURITY policy
- QUICKSTART guide
- USAGE_GUIDE comprehensive manual
- WINDOWS_SETUP guide
- CHANGELOG

### Technical
- Optimized Docker images (using runtime instead of devel)
- Minimal system dependencies
- BuildKit cache support for faster rebuilds
- Proper error handling and logging
- CORS configuration for API access
- File upload validation
- Health monitoring

### Security Notes
- ⚠️ Designed for development and testing only
- No authentication implemented
- No rate limiting
- Open CORS policy
- Not hardened for production use

## [Unreleased]

### Planned
- User authentication and authorization
- Rate limiting
- Enhanced security features
- Multi-language support for UI
- Batch processing support
- Result history and management
- Advanced configuration options
- Performance optimizations
- Additional OCR modes
- PDF multi-page support

---

## Version History

### How to Read This Changelog

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

---

**Note**: This project is for development and testing purposes only. Production use is not recommended and done at your own risk.
