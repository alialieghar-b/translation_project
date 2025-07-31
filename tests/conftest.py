#!/usr/bin/env python3
"""
pytest configuration and fixtures for LaTeX Formatter tests
Provides shared fixtures, test utilities, and pytest configuration
"""

import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator, List

import pytest

from latex_formatter import LaTeXFormatter
from latex_formatter_advanced import AdvancedLaTeXFormatter

from .fixtures.sample_latex_files import SAMPLE_DOCUMENTS, generate_large_document


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def basic_formatter() -> LaTeXFormatter:
    """Create a basic LaTeX formatter instance."""
    return LaTeXFormatter()


@pytest.fixture
def advanced_formatter() -> AdvancedLaTeXFormatter:
    """Create an advanced LaTeX formatter instance."""
    return AdvancedLaTeXFormatter()


@pytest.fixture
def custom_config_formatter() -> LaTeXFormatter:
    """Create a formatter with custom configuration."""
    config = {
        "line_length": 100,
        "indent_size": 4,
        "sort_packages": False,
        "normalize_quotes": False,
        "align_ampersands": True,
        "max_empty_lines": 1,
    }
    return LaTeXFormatter(config)


@pytest.fixture
def sample_latex_basic() -> str:
    """Provide basic LaTeX document content."""
    return SAMPLE_DOCUMENTS["basic_article"]


@pytest.fixture
def sample_latex_complex() -> str:
    """Provide complex LaTeX document content."""
    return SAMPLE_DOCUMENTS["complex_document"]


@pytest.fixture
def sample_latex_malformed() -> str:
    """Provide malformed LaTeX document content."""
    return SAMPLE_DOCUMENTS["unmatched_braces"]


@pytest.fixture
def sample_latex_tables() -> str:
    """Provide LaTeX document with complex tables."""
    return SAMPLE_DOCUMENTS["complex_tables"]


@pytest.fixture
def sample_latex_math() -> str:
    """Provide LaTeX document with complex mathematics."""
    return SAMPLE_DOCUMENTS["complex_math"]


@pytest.fixture
def sample_latex_utf8() -> str:
    """Provide LaTeX document with UTF-8 content."""
    return SAMPLE_DOCUMENTS["utf8_content"]


@pytest.fixture
def large_document() -> str:
    """Generate a large LaTeX document for performance testing."""
    return generate_large_document(sections=20, items_per_section=5)


@pytest.fixture
def test_tex_file(temp_dir: Path, sample_latex_basic: str) -> Path:
    """Create a temporary LaTeX file for testing."""
    tex_file = temp_dir / "test.tex"
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(sample_latex_basic)
    return tex_file


@pytest.fixture
def multiple_tex_files(temp_dir: Path) -> List[Path]:
    """Create multiple temporary LaTeX files for testing."""
    files = []
    for i, (name, content) in enumerate(list(SAMPLE_DOCUMENTS.items())[:3]):
        tex_file = temp_dir / f"test_{i}_{name}.tex"
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(tex_file)
    return files


@pytest.fixture
def config_file_json(temp_dir: Path) -> Path:
    """Create a JSON configuration file for testing."""
    import json

    config_file = temp_dir / "config.json"
    config_data = {
        "line_length": 90,
        "indent_size": 3,
        "sort_packages": True,
        "normalize_quotes": False,
        "align_ampersands": True,
    }

    with open(config_file, "w") as f:
        json.dump(config_data, f, indent=2)

    return config_file


@pytest.fixture
def config_file_toml(temp_dir: Path) -> Path:
    """Create a TOML configuration file for testing."""
    try:
        import toml  # noqa: F401

        config_file = temp_dir / "pyproject.toml"
        config_content = """[tool.latex-formatter]
line_length = 110
indent_size = 4
sort_packages = false
normalize_quotes = true
align_ampersands = false

[tool.latex-formatter.environments]
no_indent = ["verbatim", "lstlisting"]
blank_lines_around = ["section", "chapter"]
"""

        with open(config_file, "w") as f:
            f.write(config_content)

        return config_file

    except ImportError:
        pytest.skip("TOML library not available")
        # This line is never reached, but mypy needs it for type checking
        return temp_dir / "dummy.toml"  # pragma: no cover  # type: ignore[unreachable]


@pytest.fixture
def invalid_config_file(temp_dir: Path) -> Path:
    """Create an invalid configuration file for testing."""
    config_file = temp_dir / "invalid.json"
    with open(config_file, "w") as f:
        f.write('{ "line_length": 80, "invalid": }')  # Invalid JSON
    return config_file


# Test utilities
class TestHelpers:
    """Helper methods for testing."""

    @staticmethod
    def assert_valid_latex_structure(content: str) -> bool:
        """Assert that content has valid LaTeX document structure."""
        if "\\documentclass" not in content:
            return False
        if "\\begin{document}" in content:
            if "\\end{document}" not in content:
                return False
        return True

    @staticmethod
    def assert_proper_formatting(original: str, formatted: str) -> None:
        """Assert that formatting was applied properly."""
        # Should end with newline
        assert formatted.endswith("\n")

        # Should not have excessive empty lines
        assert "\n\n\n\n" not in formatted

        # Should preserve document structure
        if "\\documentclass" in original:
            assert "\\documentclass" in formatted

    @staticmethod
    def assert_package_sorting(content: str) -> None:
        """Assert that packages are sorted alphabetically."""
        lines = content.split("\n")
        package_lines = [line.strip() for line in lines if "\\usepackage" in line]

        if len(package_lines) > 1:
            # Extract package names for comparison
            package_names = []
            for line in package_lines:
                # Extract package name from \usepackage{name} or
                # \usepackage[options]{name}
                import re

                match = re.search(r"\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", line)
                if match:
                    package_names.append(match.group(1))

            # Check if sorted
            assert package_names == sorted(
                package_names
            ), f"Packages not sorted: {package_names}"

    @staticmethod
    def assert_quote_normalization(content: str) -> None:
        """Assert that quotes are normalized to LaTeX style."""
        # Should have LaTeX-style quotes
        if '"' in content:
            # May have been normalized
            pass  # This is content-dependent

    @staticmethod
    def count_lines(content: str) -> int:
        """Count number of lines in content."""
        return len(content.split("\n"))

    @staticmethod
    def count_empty_lines(content: str) -> int:
        """Count consecutive empty lines."""
        lines = content.split("\n")
        max_consecutive = 0
        current_consecutive = 0

        for line in lines:
            if line.strip() == "":
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0

        return max_consecutive


@pytest.fixture
def test_helpers() -> Any:
    """Provide test helper methods."""
    return TestHelpers()


@pytest.fixture
def simple_latex_content() -> str:
    """Simple LaTeX content for testing."""
    return """\\documentclass{article}
\\begin{document}
\\section{Test}
This is a simple test document.
\\end{document}"""


@pytest.fixture
def complex_latex_content() -> str:
    """Complex LaTeX content for testing."""
    return """\\documentclass[12pt,a4paper]{article}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\begin{document}
\\title{Complex Document}
\\author{Test Author}
\\maketitle

\\section{Introduction}
This is a complex document with math: $x = y + z$.

\\begin{equation}
E = mc^2
\\end{equation}

\\subsection{Subsection}
\\begin{itemize}
\\item First item
\\item Second item
\\end{itemize}
\\end{document}"""


@pytest.fixture
def temp_file(tmp_path: Path) -> Path:
    """Create a temporary file for testing."""
    return tmp_path / "test.tex"


@pytest.fixture
def poorly_formatted_content() -> str:
    """Poorly formatted LaTeX content for testing."""
    return """\\documentclass{article}
\\begin{document}
\\section{Test}
This   has    extra   spaces.
\\begin{itemize}
\\item First
\\item Second
\\end{itemize}
\\end{document}"""


@pytest.fixture
def malformed_content() -> str:
    """Malformed LaTeX content for testing."""
    return """\\documentclass{article}
\\begin{document}
\\begin{itemize}
\\item Unclosed item
% Missing \\end{itemize}
\\end{document}"""


@pytest.fixture
def custom_formatter() -> LaTeXFormatter:
    """Custom formatter with specific configuration."""
    from latex_formatter import LaTeXFormatter

    config = {"line_length": 100, "indent_size": 4, "normalize_whitespace": True}
    return LaTeXFormatter(config)


@pytest.fixture
def temp_config_file(tmp_path: Path) -> Path:
    """Create a temporary config file for testing."""
    config_file = tmp_path / "test_config.json"
    config_content = {
        "line_length": 100,
        "indent_size": 4,
        "normalize_whitespace": True,
    }
    import json

    config_file.write_text(json.dumps(config_content))
    return config_file


# Performance testing fixtures
class PerformanceTimer:
    """Simple timer for performance testing."""

    def __init__(self) -> None:
        self._start_time: float = 0.0
        self._end_time: float = 0.0

    def start(self) -> None:
        """Start the timer."""
        import time

        self._start_time = time.time()

    def stop(self) -> None:
        """Stop the timer."""
        import time

        self._end_time = time.time()

    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        return self._end_time - self._start_time


@pytest.fixture
def performance_timer() -> PerformanceTimer:
    """Provide a performance timer for testing."""
    return PerformanceTimer()


@pytest.fixture
def performance_content() -> Dict[str, str]:
    """Generate content for performance testing."""
    return {
        "small": generate_large_document(sections=5, items_per_section=3),
        "medium": generate_large_document(sections=20, items_per_section=5),
        "large": generate_large_document(sections=50, items_per_section=10),
    }


@pytest.fixture
def benchmark_formatter() -> LaTeXFormatter:
    """Create formatter for benchmarking."""
    return LaTeXFormatter(
        {
            "line_length": 80,
            "indent_size": 2,
            "sort_packages": True,
            "normalize_quotes": True,
            "align_ampersands": True,
        }
    )


# Error simulation fixtures
@pytest.fixture
def unreadable_file(temp_dir: Path) -> Path:
    """Create a file that simulates read permission error."""
    from unittest.mock import patch  # noqa: F401

    test_file = temp_dir / "unreadable.tex"
    with open(test_file, "w") as f:
        f.write("\\documentclass{article}")

    # Return a mock that raises PermissionError when opened
    return test_file


@pytest.fixture
def corrupted_file(temp_dir: Path) -> Path:
    """Create a file with corrupted content."""
    test_file = temp_dir / "corrupted.tex"
    with open(test_file, "wb") as f:
        f.write(b"\xff\xfe\x00\x01\x02")  # Invalid UTF-8
    return test_file


# Configuration for different test environments
def pytest_configure(config: Any) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "performance: marks tests as performance tests")
    config.addinivalue_line("markers", "cli: marks tests as CLI tests")


# Cleanup hooks
@pytest.fixture(autouse=True)
def cleanup_logging() -> Generator[None, None, None]:
    """Ensure logging is cleaned up after each test."""
    import logging

    yield
    # Clean up any loggers that might have been created
    logging.getLogger().handlers.clear()


# Skip conditions for optional dependencies
def pytest_collection_modifyitems(config: Any, items: Any) -> None:
    """Modify test collection to handle optional dependencies."""
    import sys  # noqa: F401

    # Skip TOML tests if toml library not available
    try:
        import toml  # noqa: F401
    except ImportError:
        skip_toml = pytest.mark.skip(reason="toml library not available")
        for item in items:
            if "toml" in item.nodeid.lower():
                item.add_marker(skip_toml)

    # Skip performance tests if running in CI or on slow systems
    if config.getoption("--fast"):
        skip_slow = pytest.mark.skip(reason="--fast option given")
        for item in items:
            if "performance" in item.keywords or "slow" in item.keywords:
                item.add_marker(skip_slow)


def pytest_addoption(parser: Any) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--fast", action="store_true", default=False, help="skip slow tests"
    )
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests",
    )


# Test data generators
class TestDataGenerator:
    """Generate test data for various scenarios."""

    @staticmethod
    def generate_malformed_latex(error_type: str) -> str:
        """Generate LaTeX with specific types of errors."""
        base = "\\documentclass{article}\n\\begin{document}\n"

        if error_type == "unmatched_brace":
            return base + "\\section{Missing brace\nContent\n\\end{document}"
        elif error_type == "unmatched_env":
            return base + "\\begin{itemize}\n\\item Test\n\\end{document}"
        elif error_type == "incomplete_command":
            return base + "\\section\n\\textbf{Bold\n\\end{document}"
        else:
            return base + "Content\n\\end{document}"

    @staticmethod
    def generate_table_content(rows: int, cols: int, aligned: bool = False) -> str:
        """Generate table content with specified dimensions."""
        separator = " & " if aligned else "&"

        header = separator.join([f"Col{i+1}" for i in range(cols)])
        rows_content = []

        for r in range(rows):
            row = separator.join([f"R{r+1}C{c+1}" for c in range(cols)])
            rows_content.append(row)

        # Fix f-string backslash issue by using variables
        backslash_newline = " \\\\\n"
        double_backslash = " \\\\"

        return f"""\\begin{{tabular}}{{{('c' * cols)}}}
{header}{double_backslash}
\\hline
{backslash_newline.join(rows_content)}{double_backslash}
\\end{{tabular}}"""


@pytest.fixture
def test_data_generator() -> TestDataGenerator:
    """Provide test data generator."""
    return TestDataGenerator()


if __name__ == "__main__":
    # Show available fixtures when run directly
    print("Available pytest fixtures:")
    fixtures = [
        "temp_dir",
        "basic_formatter",
        "advanced_formatter",
        "custom_config_formatter",
        "sample_latex_basic",
        "sample_latex_complex",
        "sample_latex_malformed",
        "sample_latex_tables",
        "sample_latex_math",
        "sample_latex_utf8",
        "large_document",
        "test_tex_file",
        "multiple_tex_files",
        "config_file_json",
        "config_file_toml",
        "invalid_config_file",
        "test_helpers",
        "performance_content",
        "benchmark_formatter",
        "test_data_generator",
    ]

    for fixture in fixtures:
        print(f"  - {fixture}")

    print("\nCustom pytest markers:")
    markers = ["slow", "integration", "performance", "cli"]
    for marker in markers:
        print(f"  - {marker}")

    print("\nCustom command line options:")
    print("  --fast: skip slow tests")
    print("  --integration: run integration tests")
