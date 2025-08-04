
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
	@echo "  test-full    - Run tests with sample PDF"

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

# Quick test with sample PDF or existing PDF
test-full: test
	@if [ -f "sample.pdf" ]; then \
		echo "Testing with sample.pdf..."; \
		python pdf_converter.py sample.pdf --output-dir ./test_output --verbose; \
		python pdf_converter.py sample.pdf --preset high --output-dir ./test_high; \
		python pdf_converter.py sample.pdf --format JPEG --dpi 150 --output-dir ./test_jpeg; \
	elif [ -f "changing zsh to ohmyz.sh.pdf" ]; then \
		echo "Testing with existing PDF file..."; \
		python pdf_converter.py "changing zsh to ohmyz.sh.pdf" --output-dir ./test_output --verbose; \
		python pdf_converter.py "changing zsh to ohmyz.sh.pdf" --preset high --output-dir ./test_high; \
		python pdf_converter.py "changing zsh to ohmyz.sh.pdf" --format JPEG --dpi 150 --output-dir ./test_jpeg; \
	else \
		echo "No PDF file found. Run 'make sample-pdf' first or add a PDF file."; \
		exit 1; \
	fi