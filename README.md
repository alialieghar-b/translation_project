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
# Install from source
git clone https://github.com/your-username/latex-formatter
cd latex-formatter
pip install -e .

# Or install directly
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

### Command Line

```bash
# Format files (modifies in-place)
latex-format document.tex paper.tex

# Check without modifying (exit code 1 if changes needed)
latex-format --check document.tex

# Show diff of proposed changes
latex-format --diff document.tex

# Custom settings
latex-format --line-length 100 --indent-size 4 document.tex

# Format all LaTeX files
latex-format *.tex
```

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

```
usage: latex-format [-h] [--check] [--diff] [--line-length LINE_LENGTH]
                   [--indent-size INDENT_SIZE] [--config CONFIG] [--verbose]
                   files [files ...]

LaTeX Formatter - Format LaTeX files like Black formats Python

positional arguments:
  files                 LaTeX files to format

optional arguments:
  -h, --help            show this help message and exit
  --check               Check if files are formatted without modifying them
  --diff                Show diff of changes
  --line-length LINE_LENGTH
                        Maximum line length (default: 80)
  --indent-size INDENT_SIZE
                        Indentation size (default: 2)
  --config CONFIG       Path to configuration file
  --verbose, -v         Verbose output
```

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
