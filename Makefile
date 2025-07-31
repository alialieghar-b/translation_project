# LaTeX Formatter Development Makefile

.PHONY: help install install-dev test test-cov lint format type-check clean build upload docs serve-docs pre-commit integration-test performance-test

# Default target
help:
	@echo "LaTeX Formatter Development Commands"
	@echo "===================================="
	@echo ""
	@echo "Setup:"
	@echo "  install      Install package in production mode"
	@echo "  install-dev  Install package in development mode with all dependencies"
	@echo ""
	@echo "Development:"
	@echo "  test         Run unit tests"
	@echo "  test-cov     Run tests with coverage report"
	@echo "  lint         Run linting (flake8)"
	@echo "  format       Format code with black"
	@echo "  type-check   Run type checking with mypy"
	@echo "  pre-commit   Run all pre-commit checks"
	@echo ""
	@echo "Testing:"
	@echo "  integration-test    Run integration tests"
	@echo "  performance-test    Run performance benchmarks"
	@echo "  test-all           Run all tests"
	@echo ""
	@echo "Build & Release:"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  upload       Upload to PyPI (requires credentials)"
	@echo "  upload-test  Upload to Test PyPI"
	@echo ""
	@echo "Documentation:"
	@echo "  docs         Generate documentation"
	@echo "  serve-docs   Serve documentation locally"
	@echo ""
	@echo "Examples:"
	@echo "  example-basic     Run basic formatting example"
	@echo "  example-advanced  Run advanced formatting example"
	@echo "  example-cli       Run CLI examples"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev,test]"
	pre-commit install

# Testing
test:
	pytest tests/

test-cov:
	pytest tests/ --cov=latex_formatter --cov=latex_formatter_advanced --cov-report=html --cov-report=term-missing

test-all: test integration-test

integration-test:
	@echo "Running integration tests..."
	@mkdir -p test_output
	@echo "Creating test LaTeX file..."
	@cat > test_output/integration_test.tex << 'EOF'
	\documentclass{article}
	\usepackage{tikz}
	\usepackage{amsmath}
	\usepackage{graphicx}
	\begin{document}
	\section{Integration Test}
	This is"bad quotes"and   poor    spacing.

	\begin{tabular}{cc}
	Name&Age&City
	John&25&NYC
	Jane&30&LA
	\end{tabular}

	\begin{equation}
	x+y=z
	\end{equation}
	\end{document}
	EOF
	@echo "Testing basic formatting..."
	python cli.py format test_output/integration_test.tex --check
	@echo "Testing advanced formatting..."
	python cli.py format test_output/integration_test.tex --advanced --diff
	@echo "Testing project analysis..."
	python cli.py analyze test_output/
	@echo "Testing syntax checking..."
	python cli.py check-syntax test_output/integration_test.tex
	@echo "✅ Integration tests passed!"

performance-test:
	@echo "Running performance tests..."
	@mkdir -p test_output
	@echo "Generating large test file..."
	@python tmp_rovodev_perf_test.py
	@echo "Testing sequential processing..."
	@python cli.py format test_output/large_test.tex
	@echo "Testing parallel processing..."
	@python cli.py format test_output/large_test.tex --parallel
	@echo "✅ Performance tests completed!"

# Code Quality
lint:
	flake8 latex_formatter.py latex_formatter_advanced.py cli.py

format:
	black latex_formatter.py latex_formatter_advanced.py cli.py tests/test_latex_formatter.py

type-check:
	mypy latex_formatter.py latex_formatter_advanced.py cli.py

pre-commit: format lint type-check test
	@echo "✅ All pre-commit checks passed!"

# Build & Release
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf test_output/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload: build
	twine upload dist/*

upload-test: build
	twine upload --repository testpypi dist/*

# Documentation
docs:
	@echo "Generating documentation..."
	@mkdir -p docs
	@cat > docs/README.md << 'EOF'
	# LaTeX Formatter Documentation

	## Quick Start

	\`\`\`bash
	# Install
	pip install latex-formatter

	# Format files
	latex-format document.tex

	# Check formatting
	latex-format --check *.tex

	# Show differences
	latex-format --diff paper.tex
	\`\`\`

	## Configuration

	Create a \`pyproject.toml\` file:

	\`\`\`toml
	[tool.latex-formatter]
	line_length = 80
	indent_size = 2
	sort_packages = true
	\`\`\`

	## Advanced Features

	\`\`\`bash
	# Use advanced formatter
	latex-format --advanced document.tex

	# Parallel processing
	latex-format --parallel *.tex

	# Project analysis
	latex-format analyze ./project/
	\`\`\`
	EOF
	@echo "📚 Documentation generated in docs/"

serve-docs:
	@echo "Serving documentation at http://localhost:8000"
	@cd docs && python -m http.server 8000

# Examples
example-basic:
	@echo "Running basic formatting example..."
	@mkdir -p examples
	@cat > examples/basic_example.tex << 'EOF'
	\documentclass{article}
	\usepackage{tikz}
	\usepackage{amsmath}
	\begin{document}
	\section{Example}
	This is"bad quotes"text.
	\begin{equation}
	x+y=z
	\end{equation}
	\end{document}
	EOF
	@echo "Before formatting:"
	@cat examples/basic_example.tex
	@echo ""
	@echo "Formatting..."
	@python latex_formatter.py examples/basic_example.tex
	@echo ""
	@echo "After formatting:"
	@cat examples/basic_example.tex

example-advanced:
	@echo "Running advanced formatting example..."
	@mkdir -p examples
	@cat > examples/advanced_example.tex << 'EOF'
	\documentclass{article}
	\usepackage{natbib}
	\usepackage{amsmath}
	\begin{document}
	\section{Advanced Example}
	This is a very long line that should be wrapped because it exceeds the maximum line length and contains citations \cite{ref1,ref2}.

	\begin{tabular}{ccc}
	Name&Age&City
	John&25&NYC
	Jane&30&LA
	\end{tabular}

	\bibliography{references}
	\end{document}
	EOF
	@echo "Before advanced formatting:"
	@cat examples/advanced_example.tex
	@echo ""
	@echo "Advanced formatting..."
	@python -c "
	from latex_formatter_advanced import AdvancedLaTeXFormatter
	formatter = AdvancedLaTeXFormatter({
	    'wrap_long_lines': True,
	    'format_citations': True,
	    'line_length': 60
	})
	with open('examples/advanced_example.tex', 'r') as f:
	    content = f.read()
	formatted = formatter.format_content(content)
	with open('examples/advanced_example.tex', 'w') as f:
	    f.write(formatted)
	"
	@echo ""
	@echo "After advanced formatting:"
	@cat examples/advanced_example.tex

example-cli:
	@echo "Running CLI examples..."
	@mkdir -p examples
	@cat > examples/cli_example.tex << 'EOF'
	\documentclass{article}
	\usepackage{amsmath}
	\begin{document}
	\section{CLI Example}
	Test content.
	\end{document}
	EOF
	@echo "1. Check formatting:"
	@python cli.py format examples/cli_example.tex --check || true
	@echo ""
	@echo "2. Show diff:"
	@python cli.py format examples/cli_example.tex --diff
	@echo ""
	@echo "3. Analyze project:"
	@python cli.py analyze examples/
	@echo ""
	@echo "4. Generate config template:"
	@python cli.py config-template

# Development shortcuts
dev-setup: install-dev
	@echo "🚀 Development environment ready!"
	@echo "Run 'make help' to see available commands"

quick-test: format lint test
	@echo "✅ Quick development checks passed!"

release-check: pre-commit integration-test performance-test
	@echo "✅ Release checks completed successfully!"

# Docker support (optional)
docker-build:
	docker build -t latex-formatter .

docker-test:
	docker run --rm -v $(PWD):/workspace latex-formatter make test

# Benchmark
benchmark:
	@echo "Running benchmarks..."
	@python -c "\
import time; \
from latex_formatter import LaTeXFormatter; \
from latex_formatter_advanced import AdvancedLaTeXFormatter; \
content = r'''\\documentclass{article}\
\\usepackage{amsmath}\
\\begin{document}\
''' + '\\\\section{Test}\\\\nContent here.\\\\n' * 100 + r'\\end{document}'; \
formatter = LaTeXFormatter(); \
start = time.time(); \
[formatter.format_content(content) for _ in range(10)]; \
basic_time = time.time() - start; \
advanced_formatter = AdvancedLaTeXFormatter(); \
start = time.time(); \
[advanced_formatter.format_content(content) for _ in range(10)]; \
advanced_time = time.time() - start; \
print(f'Basic formatter: {basic_time:.3f}s (10 runs)'); \
print(f'Advanced formatter: {advanced_time:.3f}s (10 runs)'); \
print(f'Performance ratio: {advanced_time/basic_time:.2f}x')"
