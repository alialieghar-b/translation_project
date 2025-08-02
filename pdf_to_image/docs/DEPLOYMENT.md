# Deployment Guide

## Quick Start

### 1. Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Windows
# Download from: https://github.com/oschwartz10612/poppler-windows
```

### 2. Install Python Package
```bash
# From source (recommended for development)
cd pdf_to_image
pip install -e ".[dev]"

# Or install as package
pip install .

# Or install dependencies manually
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
# Check version
python pdf_converter.py --version

# Run comprehensive tests
python fix_and_test.py

# Run unit tests
python test_converter.py
```

## Production Deployment

### Docker Container
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt pyproject.toml setup.py ./
RUN pip install .

# Copy application
COPY . /app
WORKDIR /app

ENTRYPOINT ["python", "pdf_converter.py"]
```

### Environment Variables
```bash
export PDF_CONVERTER_DEFAULT_DPI=300
export PDF_CONVERTER_DEFAULT_FORMAT=PNG
export PDF_CONVERTER_OUTPUT_DIR=/app/output
```

## Performance Tuning

### Memory Optimization
- Use `--threads 1` for memory-constrained environments
- Process files individually for large PDFs
- Monitor memory usage with `--verbose`

### Speed Optimization
- Use `--threads 4` or higher for multi-core systems
- Use lower DPI for faster processing
- Use JPEG format for smaller file sizes

## Monitoring

### Log Analysis
```bash
# Enable verbose logging
python pdf_converter.py input.pdf --verbose

# Monitor conversion progress
tail -f conversion.log
```

### Health Checks
```bash
# Test conversion capability
python pdf_converter.py --version
echo "Test" | pandoc -o test.pdf && python pdf_converter.py test.pdf
```