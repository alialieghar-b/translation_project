#!/bin/bash

# Make the formatter executable
chmod +x latex_formatter.py

# Format a single file
python latex_formatter.py document.tex

# Format multiple files
python latex_formatter.py *.tex

# Check if files need formatting (CI/CD usage)
python latex_formatter.py --check document.tex
if [ $? -ne 0 ]; then
    echo "LaTeX files need formatting!"
    exit 1
fi

# Show what would change
python latex_formatter.py --diff document.tex

# Custom configuration
python latex_formatter.py \
    --line-length 100 \
    --indent-size 4 \
    --verbose \
    document.tex

# Format all LaTeX files in project
find . -name "*.tex" -exec python latex_formatter.py {} \;
