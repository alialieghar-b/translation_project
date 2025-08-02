# PDF to Image Converter

A high-quality Python utility for converting PDF files to images with configurable output settings.

## Features

- **High-Quality Output**: Configurable DPI settings (150-600 DPI)
- **Multiple Formats**: PNG, JPEG, TIFF, BMP support
- **Quality Presets**: Web, Print, High, Archive presets
- **Batch Processing**: Convert single files or entire directories
- **Robust Error Handling**: Comprehensive validation and logging
- **Command-Line Interface**: Easy-to-use CLI with extensive options
- **Modern Python Packaging**: pyproject.toml configuration
- **Comprehensive Testing**: 9 unit tests with 100% pass rate
- **Development Tools**: Makefile, validation scripts, sample PDF generator

## Installation

### Prerequisites
- Python 3.7+
- Poppler utilities (system dependency)

#### Install Poppler:
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Windows
# Download from: https://github.com/oschwartz10612/poppler-windows
```

### Install Python Dependencies

#### For End Users (Recommended):
```bash
# Install from PyPI (when published)
pip install pdf-to-image-converter

# Or install from source
pip install .
```

#### For Developers:
```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Or install dependencies manually
pip install -r requirements.txt

# Use Makefile for common tasks
make install-dev    # Install with dev dependencies
make test          # Run unit tests
make sample-pdf    # Create sample PDF for testing
make test-full     # Run comprehensive tests with sample PDF
make lint          # Run code linting
make format        # Format code with black
```

## Usage

### Basic Usage
```bash
# Convert single PDF
python pdf_converter.py input.pdf --output-dir ./images

# Convert with high quality
python pdf_converter.py input.pdf --preset high

# Convert entire directory
python pdf_converter.py --input-dir ./pdfs --output-dir ./images
```

### Advanced Options
```bash
# Custom DPI and format
python pdf_converter.py input.pdf --dpi 600 --format TIFF

# With custom filename prefix
python pdf_converter.py input.pdf --prefix document --output-dir ./output

# Parallel processing
python pdf_converter.py input.pdf --threads 4 --verbose
```

### Quality Presets
- **web**: 150 DPI, PNG (optimized for web)
- **print**: 300 DPI, PNG (default, good for printing)
- **high**: 600 DPI, PNG (high quality)
- **archive**: 600 DPI, TIFF (archival quality)

### Input Validation
- **DPI Range**: Automatically validates DPI between 150-600
- **Format Support**: Validates against supported formats (PNG/JPEG/TIFF/BMP)
- **Thread Count**: Ensures thread count is ≥ 1
- **File Validation**: Checks PDF file existence and format

## API Usage

```python
from pdf_converter import PDFConverter

# Initialize converter
converter = PDFConverter(dpi=300, output_format='PNG')

# Convert single file
output_paths = converter.convert_pdf('input.pdf', './output')

# Convert directory
results = converter.convert_directory('./pdfs', './output')
```

## Project Structure

```
pdf-to-image-converter/
├── README.md              # Main documentation
├── LICENSE                # MIT License
├── setup.py              # Legacy package configuration
├── pyproject.toml         # Modern Python packaging
├── requirements.txt       # Python dependencies
├── Makefile              # Development automation
├── MANIFEST.in           # Package manifest
├── CHANGELOG.md          # Version history
├── pdf_converter.py      # Main converter script
├── test_converter.py     # Comprehensive test suite (9 tests)
├── create_sample_pdf.py  # Sample PDF generator
├── fix_and_test.py       # Validation and testing script
├── .gitignore            # Git ignore rules
└── docs/                 # Comprehensive documentation
    ├── HOW_IT_WORKS.md           # Technical implementation guide
    ├── LIVE_TEST_RESULTS.md      # Real PDF testing results
    ├── DEPLOYMENT.md             # Production deployment guide
    ├── TEST_RESULTS.md           # Unit test documentation
    ├── GITHUB_SETUP.md           # Publishing guide
    ├── project_status.md         # Development status (COMPLETE)
    ├── library_comparison.md     # Library research results
    └── quality_baseline.md       # Quality configuration docs
```

## Development

### Running Tests
```bash
# Run unit tests
python test_converter.py

# Run comprehensive validation
python fix_and_test.py

# Create sample PDF for testing
python create_sample_pdf.py

# Use Makefile for automated testing
make test          # Unit tests only
make test-full     # Full test with sample PDF
```

### Development Status
- ✅ **Sprint 0**: Foundation & Discovery (Complete)
  - ✅ Library research completed
  - ✅ Quality baseline established
  - ✅ PoC script implemented
- ✅ **Sprint 1**: Core Implementation (Complete)
  - ✅ Full CLI interface with presets
  - ✅ Multi-format support and batch processing
  - ✅ Error handling and logging system
- ✅ **Sprint 2**: Quality & Testing (Complete)
  - ✅ Comprehensive test suite (9 unit tests)
  - ✅ Input validation and error handling
  - ✅ Live testing with real PDF files
- ✅ **Sprint 3**: Production Readiness (Complete)
  - ✅ Modern Python packaging (pyproject.toml)
  - ✅ Development automation (Makefile)
  - ✅ Comprehensive documentation

**Status: 🎉 PRODUCTION READY - All sprints completed successfully!**

## Author

**Mohammad Hossein Soltani**
- GitHub: [github.com/soltanegharb](https://github.com/soltanegharb)
- Project: [PDF to Image Converter](https://github.com/soltanegharb/pdf-to-image-converter)

## License

MIT License - see LICENSE file for details.