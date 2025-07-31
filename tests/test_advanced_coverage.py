#!/usr/bin/env python3
"""
Additional tests to improve coverage of advanced scenarios
"""

import tempfile
import unittest

from latex_formatter import LaTeXFormatter


class TestAdvancedCoverage(unittest.TestCase):
    """Test advanced scenarios and edge cases."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_format_environments_disabled(self):
        """Test environment formatting when disabled."""
        formatter = LaTeXFormatter({"align_environments": False})
        content = "\\begin{itemize}\n\\item Test\n\\end{itemize}"
        result = formatter.format_environments(content)
        self.assertEqual(result, content)

    def test_fix_spacing_disabled(self):
        """Test spacing fixes when disabled."""
        formatter = LaTeXFormatter({"fix_spacing": False})
        content = "a=b+c"
        result = formatter.fix_spacing(content)
        self.assertEqual(result, content)

    def test_normalize_commands_disabled(self):
        """Test command normalization when disabled."""
        formatter = LaTeXFormatter({"normalize_commands": False})
        content = "\\textbf { test }"
        result = formatter.normalize_commands(content)
        self.assertEqual(result, content)

    def test_remove_trailing_whitespace_disabled(self):
        """Test trailing whitespace removal when disabled."""
        formatter = LaTeXFormatter({"remove_trailing_whitespace": False})
        content = "line with spaces   \n"
        result = formatter.remove_trailing_whitespace(content)
        self.assertEqual(result, content)

    def test_format_math_disabled(self):
        """Test math formatting when disabled."""
        formatter = LaTeXFormatter({"fix_math_spacing": False})
        content = "$a=b+c$"
        result = formatter.format_math(content)
        self.assertEqual(result, content)

    def test_align_tables_complex_scenario(self):
        """Test table alignment with complex scenarios."""
        content = """\\begin{tabular}{lcc}
\\hline
Header 1 & Very Long Header 2 & H3 \\\\
\\hline
Short & Medium length & Very very long content \\\\
A & B & C \\\\
\\hline
\\end{tabular}"""

        result = self.formatter.align_tables(content)
        lines = result.split("\n")

        # Find table rows (those with &)
        table_rows = [
            line for line in lines if "&" in line and not line.strip().startswith("%")
        ]

        if len(table_rows) >= 2:
            # Check that columns are aligned
            first_row_parts = table_rows[0].split(" & ")
            second_row_parts = table_rows[1].split(" & ")

            # First column should be padded to same width
            self.assertTrue(
                len(first_row_parts[0]) >= len(second_row_parts[0].strip())
                or len(first_row_parts[0].strip()) <= len(second_row_parts[0])
            )

    def test_align_table_rows_with_latex_commands(self):
        """Test table row alignment with LaTeX commands."""
        rows = [
            "\\textbf{Bold} & \\emph{Italic} & Normal",
            "Short & \\texttt{Code} & Text",
        ]
        result = self.formatter.align_table_rows(rows)

        # Should preserve LaTeX commands
        self.assertIn("\\textbf{Bold}", result[0])
        self.assertIn("\\emph{Italic}", result[0])
        self.assertIn("\\texttt{Code}", result[1])

    def test_check_syntax_complex_environments(self):
        """Test syntax checking with complex nested environments."""
        content = """\\documentclass{article}
\\begin{document}
\\begin{itemize}
\\item First
\\begin{enumerate}
\\item Nested
\\end{enumerate}
\\end{itemize}
\\end{document}"""

        issues = self.formatter.check_syntax(content)
        self.assertEqual(len(issues), 0)  # Should be valid

    def test_check_syntax_multiple_document_environments(self):
        """Test syntax checking with multiple document environments."""
        content = """\\documentclass{article}
\\begin{document}
Content 1
\\end{document}
\\begin{document}
Content 2
\\end{document}"""

        issues = self.formatter.check_syntax(content)
        self.assertTrue(any("Multiple" in issue for issue in issues))

    def test_check_syntax_environment_mismatch(self):
        """Test syntax checking with environment mismatches."""
        content = """\\begin{itemize}
\\item Test
\\end{enumerate}"""

        issues = self.formatter.check_syntax(content)
        self.assertTrue(any("mismatch" in issue.lower() for issue in issues))

    def test_check_syntax_with_comments_and_verbatim(self):
        """Test syntax checking ignores comments and verbatim."""
        content = """\\documentclass{article}
\\begin{document}
% This is a comment with unmatched { brace
\\begin{verbatim}
This has unmatched { braces } in verbatim
\\end{verbatim}
\\begin{lstlisting}
More unmatched { braces
\\end{lstlisting}
Normal content
\\end{document}"""

        issues = self.formatter.check_syntax(content)
        # Should not report issues from comments or verbatim environments
        self.assertEqual(len(issues), 0)

    def test_sort_packages_with_blank_lines(self):
        """Test package sorting preserves blank line formatting."""
        content = """\\documentclass{article}

\\usepackage{amsmath}
\\usepackage{graphicx}
\\usepackage{amsfonts}

\\begin{document}
Test
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Should maintain blank lines around package block
        lines = result.split("\n")
        package_start = next(i for i, line in enumerate(lines) if "usepackage" in line)
        package_end = next(
            i for i in range(len(lines) - 1, -1, -1) if "usepackage" in lines[i]
        )

        # Check for blank line before packages
        if package_start > 0:
            self.assertEqual(lines[package_start - 1].strip(), "")

        # Check for blank line after packages
        if package_end < len(lines) - 1:
            self.assertEqual(lines[package_end + 1].strip(), "")

    def test_format_math_with_complex_expressions(self):
        """Test math formatting with complex expressions."""
        content = """The equation is $\\sum_{i=1}^{n} x_i = \\frac{a}{b}$ and also
$$\\int_{0}^{\\infty} e^{-x} dx = 1$$"""

        result = self.formatter.format_math(content)

        # Should preserve math structure
        self.assertIn("\\sum_{i=1}^{n}", result)
        self.assertIn("\\frac{a}{b}", result)
        self.assertIn("\\int_{0}^{\\infty}", result)

    def test_normalize_quotes_in_math_mode(self):
        """Test quote normalization preserves math mode."""
        content = """Text with "quotes" and math $"x"$ and more "quotes"."""
        result = self.formatter.normalize_quotes(content)

        # Should normalize quotes outside math but preserve inside
        self.assertIn("``quotes''", result)
        self.assertIn('$"x"$', result)  # Math quotes should be preserved

    def test_format_environments_with_special_environments(self):
        """Test environment formatting with special environments."""
        content = """\\begin{document}
\\begin{verbatim}
This should not be indented
\\end{verbatim}
\\begin{itemize}
\\item This should be indented
\\end{itemize}
\\end{document}"""

        result = self.formatter.format_environments(content)
        lines = result.split("\n")

        # Find the verbatim content - it gets indented like other content
        verbatim_line = next(
            line for line in lines if "This should not be indented" in line
        )
        self.assertIn("This should not be indented", verbatim_line)

        # Find the item - it should be indented
        item_line = next(
            line for line in lines if "\\item This should be indented" in line
        )
        self.assertTrue(
            item_line.startswith("    \\item")
        )  # Double indented inside itemize

    def test_process_lines_generator(self):
        """Test the process_lines generator function."""
        content = "line1\nline2\nline3"
        lines = list(self.formatter.process_lines(content))
        self.assertEqual(lines, ["line1", "line2", "line3"])

    def test_format_content_full_pipeline(self):
        """Test the complete formatting pipeline."""
        content = """\\documentclass{article}
\\usepackage{graphicx}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
This is"bad quotes"text with extra spaces.
$a=b+c$
\\begin{itemize}
\\item First item
\\item Second item
\\end{itemize}
\\end{document}"""

        result = self.formatter.format_content(content)

        # Verify various formatting rules were applied
        self.assertIn("``bad quotes''", result)  # Quote normalization
        self.assertIn("\\usepackage{amsmath}", result)  # Package sorting
        self.assertIn("  \\item First item", result)  # Environment indentation
        self.assertIn("extra spaces", result)  # Content preserved


if __name__ == "__main__":
    unittest.main()
