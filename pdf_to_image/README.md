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
- **Comprehensive Testing**: 9 unit tests covering all functionality
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

# After installation, you can use either command:
pdf2img --help
pdf-converter --help
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
# Or use the installed commands (after pip install)
pdf2img input.pdf --output-dir ./images
pdf-converter input.pdf --output-dir ./images

# Convert with high quality
python pdf_converter.py input.pdf --preset high
pdf2img input.pdf --preset high
pdf-converter input.pdf --preset high

# Convert entire directory
python pdf_converter.py --input-dir ./pdfs --output-dir ./images
pdf2img --input-dir ./pdfs --output-dir ./images
pdf-converter --input-dir ./pdfs --output-dir ./images
```

### Advanced Options
```bash
# Custom DPI and format
python pdf_converter.py input.pdf --dpi 600 --format TIFF
pdf2img input.pdf --dpi 600 --format TIFF
pdf-converter input.pdf --dpi 600 --format TIFF

# With custom filename prefix
python pdf_converter.py input.pdf --prefix document --output-dir ./output
pdf2img input.pdf --prefix document --output-dir ./output
pdf-converter input.pdf --prefix document --output-dir ./output

# Parallel processing
python pdf_converter.py input.pdf --threads 4 --verbose
pdf2img input.pdf --threads 4 --verbose
pdf-converter input.pdf --threads 4 --verbose
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
    ├── project_status.md         # Development status and completion
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

# Create sample PDF for testing (requires reportlab)
python create_sample_pdf.py

# Use Makefile for automated testing
make test          # Unit tests only
make test-full     # Full test with available PDF files
make sample-pdf    # Create sample PDF (if reportlab installed)
```

### Development Progress
The project has been developed through several phases:

**Foundation & Research**
- Evaluated different PDF processing libraries (pdf2image, PyMuPDF, Wand)
- Established quality standards and DPI requirements
- Built initial proof of concept

**Core Implementation** 
- Developed the main PDFConverter class with full functionality
- Created command-line interface with quality presets
- Added support for multiple output formats and batch processing
- Implemented comprehensive error handling and logging

**Testing & Quality Assurance**
- Built comprehensive test suite with 9 unit tests
- Added input validation for DPI ranges and parameters
- Tested with real PDF files to verify performance
- Documented all functionality and edge cases

**Production Readiness**
- Added modern Python packaging with pyproject.toml
- Created development automation tools (Makefile)
- Wrote comprehensive documentation and guides

The converter is now stable and ready for production use.

## Author

**Mohammad Hossein Soltani**
- GitHub: [github.com/soltanegharb](https://github.com/soltanegharb)
- Project: [PDF to Image Converter](https://github.com/soltanegharb/pdf-to-image-converter)

## License

MIT License - see LICENSE file for details.