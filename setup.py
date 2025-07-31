#!/usr/bin/env python3
"""
Setup script for LaTeX Formatter
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="latex-formatter",
    version="1.0.0",
    author="LaTeX Formatter Team",
    author_email="latex-formatter@example.com",
    description="A Black/Ruff-style formatter for LaTeX files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/latex-formatter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Text Processing :: Markup :: LaTeX",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "toml>=0.10.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "latex-format=latex_formatter:main",
            "latexfmt=latex_formatter:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
