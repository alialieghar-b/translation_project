# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Initial release of PDF to Image Converter
- High-quality PDF to image conversion with configurable DPI (150-600)
- Support for multiple output formats: PNG, JPEG, TIFF, BMP
- Quality presets: web (150 DPI), print (300 DPI), high (600 DPI), archive (600 DPI TIFF)
- Batch processing for entire directories
- Command-line interface with comprehensive options
- Parallel processing support with configurable thread count
- Robust error handling and logging
- Comprehensive test suite
- Development tools and scripts

### Features
- **High-Quality Output**: Configurable DPI settings from 150 to 600
- **Multiple Formats**: PNG, JPEG, TIFF, BMP support with optimized settings
- **Quality Presets**: Pre-configured settings for different use cases
- **Batch Processing**: Convert single files or entire directories
- **CLI Interface**: Easy-to-use command-line interface
- **Error Handling**: Comprehensive validation and logging
- **Testing**: Full test suite with unit and integration tests

### Dependencies
- pdf2image >= 1.16.0
- Pillow >= 8.0.0
- Python >= 3.7

### Development
- Added pyproject.toml for modern Python packaging
- Added Makefile for common development tasks
- Added comprehensive test suite
- Added sample PDF creation script
- Added fix and test validation script
- Added proper documentation and examples

### Fixed
- Corrected dependency versions in setup.py (pdf2image 1.16.0 instead of non-existent 3.1.0)
- Added input validation for DPI range (150-600)
- Added input validation for thread count (>= 1)
- Improved error messages with supported format lists
- Fixed test cases for better coverage
- Added proper directory creation handling

### Documentation
- Comprehensive README with installation and usage instructions
- API documentation with examples
- Development setup instructions
- Testing guidelines
- Project structure documentation