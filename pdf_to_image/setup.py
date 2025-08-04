#!/usr/bin/env python3
"""
Setup script for PDF to Image Converter
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="pdf-to-image-converter",
    version="1.0.0",
    description="High-quality PDF to image converter with configurable output settings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mohammad Hossein Soltani",
    author_email="contact@soltanegharb.com",
    url="https://github.com/soltanegharb/pdf-to-image-converter",
    py_modules=["pdf_converter"],
    python_requires=">=3.7",
    install_requires=[
        "pdf2image>=1.16.0",
        "Pillow>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.991",
        ],
        "alternatives": [
            "PyMuPDF>=1.20.0",
            "Wand>=0.6.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "pdf2img=pdf_converter:main",
            "pdf-converter=pdf_converter:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    keywords="pdf image conversion png jpeg tiff quality dpi",
    project_urls={
        "Bug Reports": "https://github.com/soltanegharb/pdf-to-image-converter/issues",
        "Source": "https://github.com/soltanegharb/pdf-to-image-converter",
        "Documentation": "https://github.com/soltanegharb/pdf-to-image-converter/blob/main/README.md",
    },
)