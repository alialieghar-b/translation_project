#!/usr/bin/env python3
"""
Basic integration tests for LaTeX Formatter
Focus on high-level integration scenarios not covered by specialized test files
"""

import json
import os
import tempfile
import unittest
from pathlib import Path

from latex_formatter import LaTeXFormatter
from latex_formatter_advanced import AdvancedLaTeXFormatter


class TestBasicIntegration(unittest.TestCase):
    """Basic integration tests for LaTeX formatter functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir)

    def test_simple_document_workflow(self):
        """Test complete workflow with a simple document."""
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
This is"quoted"text.
\\end{document}"""

        result = self.formatter.format_content(content)

        # Basic checks for integration
        self.assertIn("``quoted''", result)
        self.assertIn("\\usepackage{amsmath}", result)
        self.assertIn("\\usepackage{tikz}", result)
        self.assertTrue(result.endswith("\n"))

        # Check package sorting
        amsmath_pos = result.find("\\usepackage{amsmath}")
        tikz_pos = result.find("\\usepackage{tikz}")
        self.assertLess(amsmath_pos, tikz_pos)

    def test_file_round_trip(self):
        """Test formatting a file and writing it back."""
        original_content = """\\documentclass{article}
\\usepackage{graphicx}
\\begin{document}
\\section{Test Section}
Content with"quotes"here.
\\end{document}"""

        # Create test file
        test_file = Path(self.test_dir) / "test.tex"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(original_content)

        # Format the file
        formatted_content = self.formatter.format_file(test_file)
        self.assertIsNotNone(formatted_content)

        # Write formatted content back
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(formatted_content)

        # Read it back and verify
        with open(test_file, "r", encoding="utf-8") as f:
            final_content = f.read()

        self.assertEqual(final_content, formatted_content)
        self.assertIn("``quotes''", final_content)

    def test_error_recovery(self):
        """Test that formatter recovers gracefully from errors."""
        # Malformed content that should not crash the formatter
        malformed_content = """\\documentclass{article}
\\section{Missing brace
\\begin{itemize}
\\item Test
% Missing end itemize
\\end{document}"""

        # Should not raise exception
        result = self.formatter.format_content(malformed_content)
        self.assertIsNotNone(result)

        # Should still have basic structure
        self.assertIn("\\documentclass{article}", result)
        self.assertIn("\\end{document}", result)

        # Should detect syntax issues
        issues = self.formatter.check_syntax(result)
        self.assertGreater(len(issues), 0)

    def test_basic_vs_advanced_formatter_compatibility(self):
        """Test that basic and advanced formatters produce compatible results."""
        content = """\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
Basic content here.
\\end{document}"""

        basic_result = self.formatter.format_content(content)
        advanced_formatter = AdvancedLaTeXFormatter()
        advanced_result = advanced_formatter.format_content(content)

        # Both should produce valid results
        self.assertIsNotNone(basic_result)
        self.assertIsNotNone(advanced_result)

        # Both should have basic formatting applied
        self.assertTrue(basic_result.endswith("\n"))
        self.assertTrue(advanced_result.endswith("\n"))

        # Advanced may have additional formatting, but basic structure should be preserved
        self.assertIn("\\documentclass{article}", basic_result)
        self.assertIn("\\documentclass{article}", advanced_result)


class TestConfigurationIntegration(unittest.TestCase):
    """Test configuration integration scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir)

    def test_config_file_workflow(self):
        """Test complete workflow with configuration file."""
        # Create configuration file
        config_file = Path(self.test_dir) / "config.json"
        config_data = {
            "line_length": 100,
            "indent_size": 4,
            "sort_packages": True,
            "normalize_quotes": False,  # Disable quote normalization
        }

        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

        # Load configuration and create formatter
        config = LaTeXFormatter.load_config(str(config_file))
        formatter = LaTeXFormatter(config)

        # Test with sample content
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\begin{document}
This has "quotes" that should not be normalized.
\\end{document}"""

        result = formatter.format_content(content)

        # Check that configuration was applied
        self.assertIn('"quotes"', result)  # Quotes should NOT be normalized

        # Check that other formatting still works
        amsmath_pos = result.find("\\usepackage{amsmath}")
        tikz_pos = result.find("\\usepackage{tikz}")
        self.assertLess(amsmath_pos, tikz_pos)  # Packages should be sorted

    def test_invalid_config_fallback(self):
        """Test fallback to defaults with invalid configuration."""
        # Create invalid configuration file
        config_file = Path(self.test_dir) / "invalid.json"
        with open(config_file, "w") as f:
            f.write('{ "line_length": 100, invalid }')

        # Should not crash, should use defaults
        config = LaTeXFormatter.load_config(str(config_file))
        formatter = LaTeXFormatter(config)

        # Should still work with default configuration
        content = "\\documentclass{article}\n\\begin{document}\nTest\n\\end{document}"
        result = formatter.format_content(content)

        self.assertIsNotNone(result)
        self.assertIn("\\documentclass{article}", result)


class TestEndToEndScenarios(unittest.TestCase):
    """Test realistic end-to-end usage scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir)

    def test_thesis_chapter_formatting(self):
        """Test formatting a realistic thesis chapter."""
        chapter_content = """\\chapter{Literature Review}
\\label{chap:literature}

This chapter provides a comprehensive review of existing literature in the field.

\\section{Historical Development}
The field began with the work of \\citet{pioneer1950} who first introduced the concepts.

\\subsection{Early Contributions}
Early work focused on basic principles:
\\begin{itemize}
\\item Theoretical foundations
\\item Initial experimental validation
\\item Proof of concept implementations
\\end{itemize}

\\section{Recent Advances}
Recent developments have focused on improving efficiency\\cite{recent2020}.

\\begin{table}[htbp]
\\centering
\\caption{Summary of approaches}
\\begin{tabular}{lcc}
\\hline
Method&Accuracy&Speed\\\\
\\hline
Traditional&85\\%&Slow\\\\
Modern&95\\%&Fast\\\\
\\hline
\\end{tabular}
\\end{table}

The results show significant improvements over traditional methods.
"""

        formatter = LaTeXFormatter()
        result = formatter.format_content(chapter_content)

        # Should preserve chapter structure
        self.assertIn("\\chapter{Literature Review}", result)
        self.assertIn("\\label{chap:literature}", result)

        # Should format table
        self.assertIn("Method & Accuracy & Speed", result)

        # Should preserve citations
        self.assertIn("\\citet{pioneer1950}", result)
        self.assertIn("\\cite{recent2020}", result)

        # Should have proper indentation for lists
        self.assertIn("  \\item", result)

    def test_article_with_math_and_figures(self):
        """Test formatting an article with mathematical content."""
        article_content = """\\documentclass{article}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\begin{document}
\\title{Mathematical Analysis}
\\author{Researcher}
\\maketitle

\\section{Introduction}
This paper presents analysis of the equation:
\\begin{equation}
\\frac{\\partial u}{\\partial t} = \\nabla^2 u + f(x,y)
\\end{equation}

\\section{Results}
Figure~\\ref{fig:results} shows our findings.

\\begin{figure}[htbp]
\\centering
\\includegraphics[width=0.8\\textwidth]{results.png}
\\caption{Experimental results}
\\label{fig:results}
\\end{figure}

The mathematical formulation in Equation~(1) provides the foundation.
\\end{document}"""

        formatter = LaTeXFormatter()
        result = formatter.format_content(article_content)

        # Should preserve mathematical content
        self.assertIn("\\frac{\\partial u}{\\partial t}", result)
        self.assertIn("\\nabla^2 u", result)

        # Should preserve figure references
        self.assertIn("Figure~\\ref{fig:results}", result)
        self.assertIn("\\includegraphics", result)

        # Should have proper document structure
        self.assertIn("\\maketitle", result)
        self.assertTrue(result.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
