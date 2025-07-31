# LaTeX Formatter

A **Black/Ruff-style formatter for LaTeX files** that automatically formats, cleans, and standardizes your LaTeX documents.

## 🚀 Features

- **Automatic Formatting**: Clean up spacing, indentation, and structure
- **Package Management**: Sort and organize `\usepackage` commands
- **Environment Alignment**: Proper indentation for nested environments
- **Table Formatting**: Align table columns with ampersands
- **Math Cleanup**: Fix spacing in mathematical expressions
- **Quote Normalization**: Convert straight quotes to LaTeX style
- **Syntax Checking**: Basic LaTeX syntax validation
- **CI/CD Ready**: Perfect for pre-commit hooks and automated workflows

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/latex-formatter
cd latex-formatter

# Install in development mode (recommended)
pip install -e .

# Or install from PyPI (when available)
pip install latex-formatter
```

## 🛠️ Development Setup

### Pre-commit Hooks

To ensure code quality and consistency, this project uses pre-commit hooks that automatically run formatters and linters before each commit.

#### Quick Setup

**Linux/macOS:**
```bash
./setup-pre-commit.sh
```

**Windows:**
```batch
setup-pre-commit.bat
```

#### Manual Setup

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Install the hooks:
```bash
pre-commit install
```

3. (Optional) Run on all files:
```bash
pre-commit run --all-files
```

#### What Gets Checked

The pre-commit hooks will automatically run:
- **Black** - Code formatting
- **isort** - Import sorting
- **MyPy** - Type checking
- **Flake8** - Code linting
- **Bandit** - Security scanning
- **LaTeX Formatter** - Format .tex files
- **General checks** - Trailing whitespace, file endings, etc.

#### Useful Commands

```bash
# Run hooks manually
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate

# Skip hooks for a commit (not recommended)
git commit --no-verify
```

## 🔧 Usage

### Method 1: Direct Python Execution (Recommended)

```bash
# Format files (modifies in-place)
python latex_formatter.py document.tex paper.tex

# Check without modifying (exit code 1 if changes needed)
python latex_formatter.py --check document.tex

# Show diff of proposed changes
python latex_formatter.py --diff document.tex

# Custom settings
python latex_formatter.py --line-length 100 --indent-size 4 document.tex

# Format all LaTeX files
python latex_formatter.py *.tex
```

### Method 2: Enhanced CLI with Advanced Features

```bash
# Format files with enhanced CLI
python cli.py format document.tex

# Use advanced formatting features
python cli.py format --advanced document.tex

# Process multiple files in parallel
python cli.py format --parallel *.tex

# Analyze entire project for issues
python cli.py analyze ./my-latex-project/

# Check syntax only
python cli.py check-syntax document.tex

# Generate configuration template
python cli.py config-template > pyproject.toml
```

### Method 3: Installed Command (if working)

```bash
# If the package is properly installed, you can use:
latex-format document.tex
latex-format --check document.tex
latex-format --diff document.tex
```

> **⚠️ Troubleshooting**: If you get `ModuleNotFoundError: No module named 'latex_formatter'` when using `latex-format`, use Method 1 or 2 above. This is a common issue with Python package installation paths.

### Configuration

Create a `pyproject.toml` file:

```toml
[tool.latex-formatter]
line_length = 80
indent_size = 2
sort_packages = true
align_environments = true
fix_spacing = true
normalize_quotes = true
max_empty_lines = 2
```

### Pre-commit Hook

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/your-username/latex-formatter
    rev: v1.0.0
    hooks:
      - id: latex-formatter
        # Alternative: use local installation
        # entry: python latex_formatter.py
        # language: system
```

## 📝 Before & After Examples

### Before:
```latex
\documentclass{article}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{graphicx}
\begin{document}
\section{Introduction}
This is some text with"bad quotes"and   poor    spacing.

\begin{tabular}{cc}
Name&Age\\
John&25\\
Jane&30\\
\end{tabular}

\begin{align}
x+y&=z\\
a-b&=c
\end{align}
\end{document}
```

### After:
```latex
\documentclass{article}

\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{tikz}

\begin{document}

  \section{Introduction}

  This is some text with ``bad quotes'' and poor spacing.

  \begin{tabular}{cc}
    Name & Age \\
    John & 25  \\
    Jane & 30  \\
  \end{tabular}

  \begin{align}
    x + y &= z \\
    a - b &= c
  \end{align}

\end{document}
```

## 🎯 Formatting Rules

### **Spacing & Whitespace**
- Remove trailing whitespace
- Normalize line endings
- Compress multiple empty lines
- Ensure final newline

### **Commands & Environments**
- Standardize command formatting: `\command{arg}`
- Proper environment indentation
- Sort `\usepackage` commands alphabetically
- Align table columns with ampersands

### **Mathematical Expressions**
- Fix spacing around operators: `x + y = z`
- Clean up math mode delimiters
- Proper alignment in equation environments

### **Typography**
- Convert straight quotes to LaTeX style: `"text"` → `` `text' ``
- Normalize spacing around punctuation

## 🔍 Syntax Checking

The formatter includes basic syntax validation:
- Unmatched braces `{}`
- Unmatched environments `\begin{env}` / `\end{env}`
- Common LaTeX errors

## 🛠 Development

```bash
# Clone and setup
git clone https://github.com/your-username/latex-formatter
cd latex-formatter
pip install -e ".[dev]"

# Run tests
pytest

# Format the formatter itself
black latex_formatter.py
```

## 📋 Command Line Options

### Main Formatter (`python latex_formatter.py`)

```
usage: latex_formatter.py [-h] [--check] [--diff] [--dry-run]
                          [--line-length LINE_LENGTH]
                          [--indent-size INDENT_SIZE] [--config CONFIG]
                          [--logfile LOGFILE] [--verbose] [--version]
                          files [files ...]

LaTeX Formatter - Format LaTeX files like Black formats Python

positional arguments:
  files                 LaTeX files to format

options:
  -h, --help            show this help message and exit
  --check               Check if files are formatted without modifying them
  --diff                Show diff of changes
  --dry-run             Show what would be changed without modifying files
  --line-length LINE_LENGTH
                        Maximum line length (default: 80)
  --indent-size INDENT_SIZE
                        Indentation size (default: 2)
  --config CONFIG       Path to configuration file (JSON or TOML)
  --logfile LOGFILE     Path to log file
  --verbose, -v         Verbose output
  --version             show program's version number and exit
```

### Enhanced CLI (`python cli.py`)

```
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

  LaTeX Formatter - A Black/Ruff-style formatter for LaTeX files.

Commands:
  format           Format LaTeX files
  analyze          Analyze a LaTeX project for formatting issues
  check-syntax     Check LaTeX files for syntax issues
  config-template  Generate a configuration template

Format command options:
  --check                Check if files need formatting without modifying them
  --diff                 Show diff of changes
  --dry-run              Show what would be changed without modifying files
  -p, --parallel         Process files in parallel
  -a, --advanced         Use advanced formatting features
  --line-length INTEGER  Maximum line length
  --indent-size INTEGER  Indentation size
```

## 🔧 Troubleshooting

### Common Issues

#### `ModuleNotFoundError: No module named 'latex_formatter'`

This happens when the `latex-format` command can't find the installed module. **Solutions:**

1. **Use direct Python execution** (recommended):
   ```bash
   python latex_formatter.py --check your-file.tex
   ```

2. **Reinstall the package**:
   ```bash
   pip uninstall latex-formatter
   pip install -e .
   ```

3. **Use the enhanced CLI**:
   ```bash
   python cli.py format --check your-file.tex
   ```

#### File encoding issues

If you get encoding errors:
```bash
# Ensure your LaTeX files are UTF-8 encoded
python latex_formatter.py --verbose your-file.tex
```

#### Permission errors

Make sure you have write permissions to the files you're trying to format:
```bash
chmod +w your-file.tex
python latex_formatter.py your-file.tex
```

### Getting Help

- Check the verbose output: `python latex_formatter.py --verbose your-file.tex`
- Use syntax checking: `python cli.py check-syntax your-file.tex`
- Analyze your project: `python cli.py analyze ./your-project/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

Inspired by:
- [Black](https://github.com/psf/black) - Python code formatter
- [Ruff](https://github.com/astral-sh/ruff) - Python linter
- [Prettier](https://prettier.io/) - Code formatter

---

**Happy LaTeX formatting!** 🎉
# Trigger CI
