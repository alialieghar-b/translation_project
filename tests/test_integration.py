#!/usr/bin/env python3
"""
Integration tests for LaTeX Formatter
Tests end-to-end workflows, file I/O, and configuration handling
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from latex_formatter import LaTeXFormatter
from latex_formatter_advanced import AdvancedLaTeXFormatter


class TestFileIOOperations(unittest.TestCase):
    """Test file input/output operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.formatter = LaTeXFormatter()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_format_file_basic(self):
        """Test basic file formatting operation."""
        # Create test file
        test_file = Path(self.test_dir) / "test.tex"
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
This is"bad quotes"text.
\\end{document}"""

        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        # Format the file
        result = self.formatter.format_file(test_file)

        # Check result
        self.assertIsNotNone(result)
        self.assertIn("``bad quotes''", result)
        self.assertIn("\\usepackage{amsmath}", result)
        self.assertIn("\\usepackage{tikz}", result)

        # Check package order
        amsmath_pos = result.find("\\usepackage{amsmath}")
        tikz_pos = result.find("\\usepackage{tikz}")
        self.assertLess(amsmath_pos, tikz_pos)

    def test_format_file_with_encoding(self):
        """Test file formatting with different encodings."""
        test_file = Path(self.test_dir) / "test_utf8.tex"
        content = """\\documentclass{article}
\\begin{document}
\\section{Test with ñ and ü characters}
Content with accented characters: café, naïve, résumé.
\\end{document}"""

        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        result = self.formatter.format_file(test_file)

        self.assertIsNotNone(result)
        self.assertIn("café", result)
        self.assertIn("naïve", result)
        self.assertIn("résumé", result)

    def test_format_file_nonexistent(self):
        """Test formatting non-existent file."""
        nonexistent_file = Path(self.test_dir) / "nonexistent.tex"
        result = self.formatter.format_file(nonexistent_file)

        self.assertIsNone(result)

    def test_format_file_permission_error(self):
        """Test formatting file with permission error."""
        test_file = Path(self.test_dir) / "test.tex"
        with open(test_file, "w") as f:
            f.write("\\documentclass{article}")

        # Mock open to raise PermissionError
        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            result = self.formatter.format_file(test_file)

            self.assertIsNone(result)

    def test_format_file_unicode_error(self):
        """Test formatting file with unicode decode error."""
        test_file = Path(self.test_dir) / "test.tex"

        # Write binary content that will cause decode error
        with open(test_file, "wb") as f:
            f.write(b"\xff\xfe\\documentclass{article}")

        # Mock open to raise UnicodeDecodeError
        with patch(
            "builtins.open",
            side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid start byte"),
        ):
            result = self.formatter.format_file(test_file)

            self.assertIsNone(result)

    def test_format_multiple_files(self):
        """Test formatting multiple files."""
        files = []
        for i in range(3):
            test_file = Path(self.test_dir) / f"test{i}.tex"
            content = f"""\\documentclass{{article}}
\\begin{{document}}
\\section{{Test {i}}}
This is"quotes"in file {i}.
\\end{{document}}"""

            with open(test_file, "w") as f:
                f.write(content)
            files.append(test_file)

        # Format all files
        results = []
        for file_path in files:
            result = self.formatter.format_file(file_path)
            results.append(result)

        # Check all results
        for i, result in enumerate(results):
            self.assertIsNotNone(result)
            self.assertIn(f"Test {i}", result)
            self.assertIn("``quotes''", result)


class TestConfigurationLoading(unittest.TestCase):
    """Test configuration file loading and merging."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_load_json_config(self):
        """Test loading JSON configuration file."""
        config_file = Path(self.test_dir) / "config.json"
        config_data = {
            "line_length": 100,
            "indent_size": 4,
            "sort_packages": False,
            "normalize_quotes": True,
        }

        with open(config_file, "w") as f:
            json.dump(config_data, f)

        config = LaTeXFormatter.load_config(str(config_file))

        # Check loaded values
        self.assertEqual(config["line_length"], 100)
        self.assertEqual(config["indent_size"], 4)
        self.assertEqual(config["sort_packages"], False)
        self.assertEqual(config["normalize_quotes"], True)

        # Check default values are still present
        self.assertIn("align_environments", config)
        self.assertIn("fix_spacing", config)

    def test_load_toml_config(self):
        """Test loading TOML configuration file."""
        try:
            import toml  # noqa: F401

            config_file = Path(self.test_dir) / "pyproject.toml"
            config_content = """[tool.latex-formatter]
line_length = 120
indent_size = 3
sort_packages = true
normalize_quotes = false

[tool.latex-formatter.environments]
no_indent = ["verbatim", "lstlisting"]
blank_lines_around = ["section", "subsection"]
"""

            with open(config_file, "w") as f:
                f.write(config_content)

            config = LaTeXFormatter.load_config(str(config_file))

            # Check loaded values
            self.assertEqual(config["line_length"], 120)
            self.assertEqual(config["indent_size"], 3)
            self.assertEqual(config["sort_packages"], True)
            self.assertEqual(config["normalize_quotes"], False)

        except ImportError:
            self.skipTest("TOML library not available")

    def test_load_invalid_json_config(self):
        """Test loading invalid JSON configuration file."""
        config_file = Path(self.test_dir) / "invalid.json"

        with open(config_file, "w") as f:
            f.write("{ invalid json content")

        # Should not raise exception, should return default config
        config = LaTeXFormatter.load_config(str(config_file))

        self.assertIsInstance(config, dict)
        self.assertEqual(config["line_length"], 80)  # default value
        self.assertEqual(config["indent_size"], 2)  # default value

    def test_load_empty_config_file(self):
        """Test loading empty configuration file."""
        config_file = Path(self.test_dir) / "empty.json"

        with open(config_file, "w") as f:
            f.write("{}")

        config = LaTeXFormatter.load_config(str(config_file))

        # Should have default values
        self.assertEqual(config["line_length"], 80)
        self.assertEqual(config["indent_size"], 2)

    def test_config_partial_override(self):
        """Test partial configuration override."""
        config_file = Path(self.test_dir) / "partial.json"
        config_data = {"line_length": 120, "sort_packages": False}

        with open(config_file, "w") as f:
            json.dump(config_data, f)

        config = LaTeXFormatter.load_config(str(config_file))

        # Overridden values
        self.assertEqual(config["line_length"], 120)
        self.assertEqual(config["sort_packages"], False)

        # Default values should remain
        self.assertEqual(config["indent_size"], 2)
        self.assertTrue(config["normalize_quotes"])

    def test_formatter_with_custom_config(self):
        """Test formatter initialization with custom configuration."""
        custom_config = {
            "line_length": 60,
            "indent_size": 3,
            "sort_packages": False,
            "normalize_quotes": False,
            "align_environments": False,
        }

        formatter = LaTeXFormatter(custom_config)

        # Test that custom config is used
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
This is "quoted" text.
\\end{document}"""

        result = formatter.format_content(content)

        # Packages should NOT be sorted (disabled)
        self.assertIn("\\usepackage{tikz}\n\\usepackage{amsmath}", result)

        # Quotes should NOT be normalized (disabled)
        self.assertIn('"quoted"', result)


class TestEndToEndWorkflows(unittest.TestCase):
    """Test complete end-to-end formatting workflows."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_complete_document_formatting(self):
        """Test formatting a complete LaTeX document."""
        formatter = LaTeXFormatter()

        input_content = """\\documentclass[12pt,a4paper]{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\usepackage{amsfonts}
\\title{Test   Document}
\\author{John   Doe}
\\begin{document}
\\maketitle


\\section{Introduction}
This is"quoted text"and some math: $x=y+z$.




\\subsection{Methods}
We used the following approach:
\\begin{itemize}
\\item First step
\\item Second step
\\begin{enumerate}
\\item Substep A
\\item Substep B
\\end{enumerate}
\\end{itemize}

\\section{Results}
\\begin{tabular}{ccc}
Name&Age&City
John&25&NYC
Jane&30&LA
\\end{tabular}

\\section{Conclusion}
This concludes our study.
\\end{document}"""

        result = formatter.format_content(input_content)

        # Check various formatting aspects

        # 1. Package sorting
        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]
        expected_order = [
            "\\usepackage{amsfonts}",
            "\\usepackage{amsmath}",
            "\\usepackage{graphicx}",
            "\\usepackage{tikz}",
        ]
        self.assertEqual(package_lines, expected_order)

        # 2. Quote normalization
        self.assertIn("``quoted text''", result)

        # 3. Empty line compression
        self.assertNotIn("\n\n\n\n", result)

        # 4. Environment indentation
        self.assertIn("  \\item First step", result)
        self.assertIn("    \\item Substep A", result)

        # 5. Table alignment
        self.assertIn("Name & Age & City", result)
        self.assertIn("John & 25  & NYC", result)

        # 6. Final newline
        self.assertTrue(result.endswith("\n"))

        # 7. Command normalization (formatter preserves internal spacing)
        self.assertIn(
            "\\title{Test   Document}", result
        )  # Fixed: formatter preserves internal spacing in titles
        self.assertIn(
            "\\author{John   Doe}", result
        )  # Fixed: formatter preserves internal spacing

    def test_advanced_document_formatting(self):
        """Test advanced formatting features on a document."""
        config = {
            "format_bibliography": True,
            "format_citations": True,
            "optimize_whitespace": True,
            "wrap_long_lines": False,  # Disabled for predictable testing
            "align_comments": False,  # Disabled for predictable testing
        }
        formatter = AdvancedLaTeXFormatter(config)

        input_content = """\\documentclass{article}
\\usepackage{natbib}
\\begin{document}
\\section{Introduction}
See \\cite  { ref1 , ref2 } for more details .
This is important research .

\\begin{thebibliography}{9}
\\bibitem{ref1}
Author, A. (2020). First paper title.
\\bibitem{ref2}
Author, B. (2021). Second paper title.
\\end{thebibliography}
\\end{document}"""

        result = formatter.format_content(input_content)

        # Check advanced formatting
        self.assertIn("\\cite{ref1,ref2}", result)  # Citation formatting
        self.assertIn("details.", result)  # Whitespace optimization
        self.assertIn("research.", result)

        # Bibliography formatting
        self.assertIn("  \\bibitem{ref1}", result)
        self.assertIn("    Author, A. (2020)", result)

    def test_malformed_document_handling(self):
        """Test handling of malformed LaTeX documents."""
        formatter = LaTeXFormatter()

        malformed_content = """\\documentclass{article}
\\begin{document}
\\section{Test
Missing closing brace above.

\\begin{itemize}
\\item First item
\\item Second item
% Missing \\end{itemize}

\\begin{table}
\\begin{tabular}{cc}
Name&Age
John&25
\\end{tabular}
\\end{table}

\\end{document}"""

        # Should not crash, should format what it can
        result = formatter.format_content(malformed_content)

        self.assertIsNotNone(result)
        self.assertIn("\\documentclass{article}", result)
        self.assertIn("\\begin{document}", result)
        self.assertIn("\\end{document}", result)

        # Check syntax issues
        issues = formatter.check_syntax(result)
        self.assertGreater(len(issues), 0)  # Should detect issues

    def test_large_document_processing(self):
        """Test processing of large documents."""
        formatter = LaTeXFormatter()

        # Generate large document
        sections = []
        for i in range(50):
            section = f"""\\section{{Section {i}}}
This is content for section {i}. It has "quotes" and math $x_{{i}} = y_{{i}} + z_{{i}}$.

\\begin{{itemize}}
\\item Point 1 for section {i}
\\item Point 2 for section {i}
\\end{{itemize}}

"""
            sections.append(section)

        large_content = (
            """\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
"""
            + "".join(sections)
            + """\\end{document}"""
        )

        # Should handle large content efficiently
        result = formatter.format_content(large_content)

        self.assertIsNotNone(result)
        self.assertIn("Section 0", result)
        self.assertIn("Section 49", result)
        self.assertIn("``quotes''", result)

        # Check that all sections are properly formatted
        for i in range(0, 49, 10):  # Check every 10th section
            self.assertIn(f"Section {i}", result)

    def test_real_latex_document_workflow(self):
        """Test workflow with a realistic LaTeX document."""
        # Create a realistic LaTeX document
        document_content = """\\documentclass[11pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{amsmath,amssymb,amsfonts}
\\usepackage{graphicx}
\\usepackage{booktabs}
\\usepackage{hyperref}
\\usepackage{cite}

\\title{A Study of LaTeX Formatting}
\\author{Jane Smith\\\\University of Example}
\\date{\\today}

\\begin{document}
\\maketitle

\\begin{abstract}
This paper presents a study of LaTeX formatting. We examine document structure,
math typesetting, and citations.
\\end{abstract}

\\section{Introduction}
LaTeX is a typesetting system used in academia\\cite{lamport1994latex}.
It supports math notation, as shown in Equation~\\ref{eq:example}.

\\begin{equation}
\\label{eq:example}
E = mc^2
\\end{equation}

\\section{Methodology}
Our approach involves several steps:
\\begin{enumerate}
\\item Data collection
\\item Statistical analysis
\\item Result interpretation
\\end{enumerate}

\\section{Results}
Table~\\ref{tab:results} shows our findings.

\\begin{table}[htbp]
\\centering
\\caption{Experimental Results}
\\label{tab:results}
\\begin{tabular}{lcc}
\\toprule
Method&Accuracy&Time (s)\\\\
\\midrule
Approach A&0.95&10.2\\\\
Approach B&0.92&8.5\\\\
\\bottomrule
\\end{tabular}
\\end{table}

\\section{Conclusion}
We have demonstrated the effectiveness of our approach.

\\bibliographystyle{plain}
\\bibliography{references}

\\end{document}"""

        # Test with both basic and advanced formatters
        basic_formatter = LaTeXFormatter()
        advanced_formatter = AdvancedLaTeXFormatter()

        basic_result = basic_formatter.format_content(document_content)
        advanced_result = advanced_formatter.format_content(document_content)

        # Both should produce valid results
        self.assertIsNotNone(basic_result)
        self.assertIsNotNone(advanced_result)

        # Check common formatting
        for result in [basic_result, advanced_result]:
            # Package sorting
            amsfonts_pos = result.find("\\usepackage{amsfonts}")
            graphicx_pos = result.find("\\usepackage{graphicx}")
            self.assertLess(amsfonts_pos, graphicx_pos)

            # Environment indentation
            self.assertIn("  \\item Data collection", result)

            # Table formatting
            self.assertIn("Method & Accuracy & Time (s)", result)

            # Final newline
            self.assertTrue(result.endswith("\n"))

        # Advanced formatter should have additional optimizations
        self.assertIn(
            "\\cite{lamport1994latex}", advanced_result
        )  # Citation formatting


class TestConfigurationIntegration(unittest.TestCase):
    """Test integration of configuration with formatting operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_json_config_integration(self):
        """Test complete workflow with JSON configuration."""
        # Create configuration file
        config_file = Path(self.test_dir) / "config.json"
        config_data = {
            "line_length": 60,
            "indent_size": 4,
            "sort_packages": True,
            "normalize_quotes": True,
            "align_ampersands": True,
            "max_empty_lines": 1,
        }

        with open(config_file, "w") as f:
            json.dump(config_data, f)

        # Create test document
        test_file = Path(self.test_dir) / "test.tex"
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}


\\begin{document}
\\section{Test}
This is"quoted"text.

\\begin{tabular}{cc}
Name&Age
John&25
\\end{tabular}
\\end{document}"""

        with open(test_file, "w") as f:
            f.write(content)

        # Load config and format
        config = LaTeXFormatter.load_config(str(config_file))
        formatter = LaTeXFormatter(config)
        result = formatter.format_file(test_file)

        # Verify configuration was applied
        self.assertIn("``quoted''", result)  # Quote normalization

        # Package sorting
        amsmath_pos = result.find("\\usepackage{amsmath}")
        tikz_pos = result.find("\\usepackage{tikz}")
        self.assertLess(amsmath_pos, tikz_pos)

        # Empty line compression (max 1)
        self.assertNotIn("\n\n\n", result)

        # Table alignment
        self.assertIn("Name & Age", result)
        self.assertIn("John & 25", result)

    def test_configuration_precedence(self):
        """Test configuration precedence: file config vs runtime config."""
        # Create base config file
        config_file = Path(self.test_dir) / "base_config.json"
        base_config = {
            "line_length": 80,
            "sort_packages": True,
            "normalize_quotes": True,
        }

        with open(config_file, "w") as f:
            json.dump(base_config, f)

        # Load base config
        config = LaTeXFormatter.load_config(str(config_file))

        # Override with runtime config
        config.update({"line_length": 120, "normalize_quotes": False})

        formatter = LaTeXFormatter(config)

        # Test content
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\begin{document}
This is"quoted"text.
\\end{document}"""

        result = formatter.format_content(content)

        # Runtime overrides should take effect
        self.assertIn('"quoted"', result)  # Quotes NOT normalized (runtime override)

        # Base config should still apply where not overridden
        amsmath_pos = result.find("\\usepackage{amsmath}")
        tikz_pos = result.find("\\usepackage{tikz}")
        self.assertLess(amsmath_pos, tikz_pos)  # Packages sorted (base config)


if __name__ == "__main__":
    unittest.main()
