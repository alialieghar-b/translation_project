# PyPI Publishing Guide for PDF to Image Converter

## 📦 Complete Guide to Publishing on PyPI

This guide will walk you through publishing the PDF to Image Converter package to the Python Package Index (PyPI).

## 🔧 Prerequisites

### 1. Install Required Tools
```bash
# Install build tools
pip install --upgrade pip
pip install build twine

# Optional: Install keyring for secure credential storage
pip install keyring
```

### 2. Create PyPI Accounts
1. **PyPI Account**: Register at [pypi.org](https://pypi.org/account/register/)
2. **TestPyPI Account**: Register at [test.pypi.org](https://test.pypi.org/account/register/) (for testing)

### 3. Generate API Tokens (Recommended)
1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Set scope to "Entire account" (or specific project after first upload)
5. Copy the token (starts with `pypi-`)
6. Repeat for TestPyPI at [test.pypi.org](https://test.pypi.org/manage/account/)

## 📋 Pre-Publishing Checklist

### 1. Verify Package Configuration
```bash
# Check pyproject.toml is properly configured
cat pyproject.toml

# Verify all required files exist
ls -la README.md LICENSE pyproject.toml pdf_converter.py
```

### 2. Update Version (if needed)
Edit `pyproject.toml`:
```toml
[project]
version = "1.0.0"  # Update this for new releases
```

### 3. Clean Previous Builds
```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/
```

### 4. Run Tests
```bash
# Ensure all tests pass
python test_converter.py
make test
```

## 🏗️ Building the Package

### 1. Build Distribution Files
```bash
# Build both source distribution and wheel
python -m build

# This creates:
# dist/pdf-to-image-converter-1.0.0.tar.gz (source distribution)
# dist/pdf_to_image_converter-1.0.0-py3-none-any.whl (wheel)
```

### 2. Verify Build Contents
```bash
# Check what's included in the package
tar -tzf dist/pdf-to-image-converter-1.0.0.tar.gz

# Or for wheel
unzip -l dist/pdf_to_image_converter-1.0.0-py3-none-any.whl
```

## 🧪 Testing on TestPyPI (Recommended)

### 1. Upload to TestPyPI
```bash
# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*

# You'll be prompted for credentials:
# Username: __token__
# Password: your-testpypi-token (pypi-...)
```

### 2. Test Installation from TestPyPI
```bash
# Create a new virtual environment for testing
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pdf-to-image-converter

# Test the installation
pdf2img --help
pdf-converter --help

# Test with a sample PDF
pdf2img sample.pdf --output-dir test_output

# Deactivate and remove test environment
deactivate
rm -rf test_env
```

## 🚀 Publishing to PyPI

### 1. Upload to PyPI
```bash
# Upload to the real PyPI
python -m twine upload dist/*

# You'll be prompted for credentials:
# Username: __token__
# Password: your-pypi-token (pypi-...)
```

### 2. Verify Publication
1. Visit [pypi.org/project/pdf-to-image-converter/](https://pypi.org/project/pdf-to-image-converter/)
2. Check that all information displays correctly
3. Verify the README renders properly

### 3. Test Installation
```bash
# Test installation from PyPI
pip install pdf-to-image-converter

# Verify commands work
pdf2img --help
pdf-converter --version
```

## 🔐 Secure Credential Management

### Option 1: Using API Tokens (Recommended)
```bash
# Configure credentials using keyring
keyring set https://upload.pypi.org/legacy/ __token__
# Enter your PyPI token when prompted

keyring set https://test.pypi.org/legacy/ __token__
# Enter your TestPyPI token when prompted
```

### Option 2: Using .pypirc File
Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token-here
```

**Security Note**: Keep your tokens secure and never commit them to version control!

## 📝 Publishing Workflow Script

Create `publish.sh` for automated publishing:

```bash
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
python -m twine upload --repository testpypi dist/*

echo "✅ Package uploaded to TestPyPI!"
echo "🔗 Check: https://test.pypi.org/project/pdf-to-image-converter/"
echo ""
echo "To upload to PyPI, run:"
echo "python -m twine upload dist/*"
```

Make it executable:
```bash
chmod +x publish.sh
```

## 🔄 Version Management

### Semantic Versioning
Follow [semver.org](https://semver.org/) guidelines:
- **1.0.0**: Initial release
- **1.0.1**: Bug fixes
- **1.1.0**: New features (backward compatible)
- **2.0.0**: Breaking changes

### Release Process
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v1.0.1`
4. Build and publish
5. Push tag: `git push origin v1.0.1`

## 🚨 Troubleshooting

### Common Issues

#### 1. "Package already exists"
```bash
# If you need to update, increment version number in pyproject.toml
# PyPI doesn't allow overwriting existing versions
```

#### 2. "Invalid credentials"
```bash
# Verify your API token is correct
# Make sure username is "__token__" (with underscores)
```

#### 3. "README not rendering"
```bash
# Ensure README.md is valid Markdown
# Check that readme = "README.md" is in pyproject.toml
```

#### 4. "Missing files in package"
```bash
# Check MANIFEST.in includes all necessary files
# Verify pyproject.toml [tool.setuptools] configuration
```

### Validation Commands
```bash
# Check package metadata
python -m twine check dist/*

# Validate pyproject.toml
pip install validate-pyproject
validate-pyproject pyproject.toml

# Test local installation
pip install -e .
```

## 📊 Post-Publication

### 1. Monitor Package
- Check download statistics on PyPI
- Monitor for issues or bug reports
- Respond to user feedback

### 2. Documentation Updates
- Update README with PyPI installation instructions
- Add PyPI badge to repository
- Update project documentation

### 3. Continuous Integration
Consider setting up GitHub Actions for automated publishing:
```yaml
# .github/workflows/publish.yml
name: Publish to PyPI
on:
  release:
    types: [published]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - run: pip install build twine
    - run: python -m build
    - run: python -m twine upload dist/*
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

## 🎉 Success!

Once published, users can install your package with:
```bash
pip install pdf-to-image-converter
```

Your package will be available at:
- **PyPI**: https://pypi.org/project/pdf-to-image-converter/
- **Documentation**: Auto-generated from your README
- **Download Statistics**: Available on the PyPI project page

## 📞 Support

If you encounter issues:
1. Check [PyPI Help](https://pypi.org/help/)
2. Review [Python Packaging Guide](https://packaging.python.org/)
3. Ask on [Python Packaging Discourse](https://discuss.python.org/c/packaging/)

---

**Happy Publishing!** 🚀📦