#!/bin/bash
set -e

echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

echo "🧪 Running tests..."
python test_converter.py

echo "🏗️ Building package..."
python -m build

echo "🔍 Checking package..."
python -m twine check dist/*

echo "📤 Uploading to TestPyPI..."
echo "Run: python -m twine upload --repository testpypi dist/*"
echo ""
echo "After testing on TestPyPI, upload to PyPI with:"
echo "python -m twine upload dist/*"
echo ""
echo "✅ Package ready for publishing!"
echo "🔗 TestPyPI: https://test.pypi.org/project/pdf-to-image-converter/"
echo "🔗 PyPI: https://pypi.org/project/pdf-to-image-converter/"