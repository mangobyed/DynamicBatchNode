# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-07

### Added
- Initial release of Dynamic Image Batch Node
- Dynamic input count functionality (1-20 inputs)
- Real-time UI updates via JavaScript extension
- Multiple interpolation methods:
  - lanczos (default)
  - nearest
  - linear
  - bilinear
  - bicubic
- Comprehensive error handling and validation
- Automatic image resizing to match first image dimensions
- Support for RGB, Grayscale, and RGBA images
- Strict input validation (all specified inputs must be connected)
- Clear error messages for common issues
- Python installation checker script
- Complete documentation and examples

### Technical Details
- Uses PyTorch tensor operations for efficient processing
- JavaScript extension for dynamic UI manipulation
- Proper ComfyUI node structure with categories
- MIT License for open source distribution

### Files Included
- `__init__.py` - Main node implementation
- `js/dynamic_image_batch.js` - JavaScript for dynamic UI
- `README.md` - Comprehensive documentation
- `LICENSE` - MIT License
- `CHANGELOG.md` - This changelog
- `requirements.txt` - Dependencies (none required)
- `install.py` - Installation verification script
- `.gitignore` - Git ignore rules