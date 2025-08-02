.PHONY: help install install-dev test lint format clean build upload sample-pdf

help:
	@echo "Available commands:"
	@echo "  install      - Install the package"
	@echo "  install-dev  - Install with development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build distribution packages"
	@echo "  sample-pdf   - Create a sample PDF for testing"

install:
	pip install .

install-dev:
	pip install -e ".[dev]"

test:
	python test_converter.py

lint:
	flake8 --max-line-length=100 *.py || echo "flake8 not available"
	mypy *.py || echo "mypy not available"

format:
	black --line-length=100 *.py || echo "black not available"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

build: clean
	python -m build

sample-pdf:
	python create_sample_pdf.py

# Quick test with sample PDF
test-full: sample-pdf
	python pdf_converter.py sample.pdf --output-dir ./test_output --verbose
	python pdf_converter.py sample.pdf --preset high --output-dir ./test_high
	python pdf_converter.py sample.pdf --format JPEG --dpi 150 --output-dir ./test_jpeg