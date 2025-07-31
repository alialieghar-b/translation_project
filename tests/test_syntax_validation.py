#!/usr/bin/env python3
"""
Comprehensive syntax validation tests for LaTeX Formatter
Tests LaTeX syntax checking including unmatched braces, environments, and nesting
"""

import unittest

from latex_formatter import LaTeXFormatter
from latex_formatter_advanced import AdvancedLaTeXFormatter


class TestBasicSyntaxValidation(unittest.TestCase):
    """Test basic syntax validation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()
        self.advanced_formatter = AdvancedLaTeXFormatter()

    def test_balanced_braces_valid(self):
        """Test validation of properly balanced braces."""
        valid_content = """\\documentclass{article}
\\begin{document}
\\section{Title}
\\textbf{Bold text} and \\emph{emphasized text}.
\\end{document}"""

        issues = self.formatter.check_syntax(valid_content)
        self.assertEqual(issues, [])

    def test_unmatched_opening_brace(self):
        """Test detection of unmatched opening braces."""
        invalid_content = """\\documentclass{article}
\\begin{document}
\\section{Missing closing brace
\\end{document}"""

        issues = self.formatter.check_syntax(invalid_content)
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("Unmatched opening braces" in issue for issue in issues))

    def test_unmatched_closing_brace(self):
        """Test detection of unmatched closing braces."""
        invalid_content = """\\documentclass{article}
\\begin{document}
\\section}Title with extra brace{
\\end{document}"""

        issues = self.formatter.check_syntax(invalid_content)
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("Unmatched closing brace" in issue for issue in issues))

    def test_multiple_unmatched_braces(self):
        """Test detection of multiple unmatched braces."""
        invalid_content = """\\documentclass{article}
\\section{First missing brace
\\textbf{Second missing brace
\\emph{Third} but this one is OK
\\end{document}"""

        issues = self.formatter.check_syntax(invalid_content)
        self.assertGreater(len(issues), 0)
        # Should detect multiple unmatched braces
        opening_brace_issues = [issue for issue in issues if "opening braces" in issue]
        self.assertTrue(len(opening_brace_issues) > 0)

    def test_nested_braces_valid(self):
        """Test validation of properly nested braces."""
        valid_content = """\\documentclass{article}
\\begin{document}
\\textbf{\\emph{\\underline{Nested formatting}}}
\\frac{\\sum_{i=1}^{n} x_i}{\\sqrt{n}}
\\end{document}"""

        issues = self.formatter.check_syntax(valid_content)
        self.assertEqual(issues, [])

    def test_nested_braces_invalid(self):
        """Test detection of invalid nested braces."""
        invalid_content = """\\documentclass{article}
\\begin{document}
\\textbf{\\emph{Missing inner brace}
\\end{document}"""

        issues = self.formatter.check_syntax(invalid_content)
        self.assertGreater(len(issues), 0)


class TestEnvironmentValidation(unittest.TestCase):
    """Test environment matching validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_balanced_environments_valid(self):
        """Test validation of properly balanced environments."""
        valid_content = """\\documentclass{article}
\\begin{document}
\\begin{itemize}
\\item First item
\\begin{enumerate}
\\item Nested item
\\end{enumerate}
\\end{itemize}
\\begin{equation}
x = y + z
\\end{equation}
\\end{document}"""

        issues = self.formatter.check_syntax(valid_content)
        self.assertEqual(issues, [])

    def test_missing_end_environment(self):
        """Test detection of missing end environment."""
        invalid_content = """\\documentclass{article}
\\begin{document}
\\begin{itemize}
\\item First item
\\item Second item
% Missing \\end{itemize}
\\end{document}"""

        issues = self.formatter.check_syntax(invalid_content)
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("itemize" in issue for issue in issues))

    def test_missing_begin_environment(self):
        """Test detection of missing begin environment."""
        invalid_content = """\\documentclass{article}
\\begin{document}
\\item Orphaned item
\\end{itemize}
\\end{document}"""

        issues = self.formatter.check_syntax(invalid_content)
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("itemize" in issue for issue in issues))

    def test_mismatched_environment_names(self):
        """Test detection of mismatched environment names."""
        invalid_content = """\\documentclass{article}
\\begin{document}
\\begin{itemize}
\\item First item
\\end{enumerate}
\\end{document}"""

        issues = self.formatter.check_syntax(invalid_content)
        self.assertGreater(len(issues), 0)
        # Should detect both itemize and enumerate issues
        self.assertTrue(
            any("itemize" in issue or "enumerate" in issue for issue in issues)
        )

    def test_nested_environment_mismatch(self):
        """Test detection of nested environment mismatches."""
        invalid_content = """\\documentclass{article}
\\begin{document}
\\begin{itemize}
\\item First level
\\begin{enumerate}
\\item Second level
\\end{itemize}
\\end{enumerate}
\\end{document}"""

        issues = self.formatter.check_syntax(invalid_content)
        self.assertGreater(len(issues), 0)

    def test_multiple_environment_issues(self):
        """Test detection of multiple environment issues."""
        invalid_content = """\\documentclass{article}
\\begin{document}
\\begin{itemize}
\\item Item 1
% Missing end itemize

\\begin{equation}
x = y
% Missing end equation

\\begin{tabular}{cc}
A & B
% Missing end tabular
\\end{document}"""

        # Test the invalid content instead of valid content
        issues = self.formatter.check_syntax(invalid_content)
        # Should detect issues with all three environments
        issue_text = " ".join(issues)
        self.assertIn("itemize", issue_text)
        self.assertIn("equation", issue_text)
        self.assertIn("tabular", issue_text)


class TestComplexNestingScenarios(unittest.TestCase):
    """Test complex nesting scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_deeply_nested_valid(self):
        """Test validation of deeply nested structures."""
        # Create deeply nested but valid structure
        nested_content = "\\documentclass{article}\n\\begin{document}\n"

        # Add 10 levels of nesting
        for i in range(10):
            nested_content += f"\\begin{{itemize}}\n\\item Level {i+1}\n"

        for i in range(10):
            nested_content += "\\end{itemize}\n"

        nested_content += "\\end{document}"

        issues = self.formatter.check_syntax(nested_content)
        self.assertEqual(issues, [])

    def test_deeply_nested_invalid(self):
        """Test detection of errors in deeply nested structures."""
        # Create deeply nested structure with error in the middle
        nested_content = "\\documentclass{article}\n\\begin{document}\n"

        # Add 10 levels of nesting
        for i in range(10):
            nested_content += f"\\begin{{itemize}}\n\\item Level {i+1}\n"

        # Close only 9 levels (missing one end)
        for i in range(9):
            nested_content += "\\end{itemize}\n"

        nested_content += "\\end{document}"

        issues = self.formatter.check_syntax(nested_content)
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("itemize" in issue for issue in issues))

    def test_mixed_environment_nesting(self):
        """Test validation of mixed environment types in nesting."""
        mixed_content = """\\documentclass{article}
\\begin{document}
\\begin{itemize}
\\item First level list
\\begin{enumerate}
\\item Second level numbered
\\begin{description}
\\item[Term] Third level description
\\end{description}
\\end{enumerate}
\\begin{quote}
Quoted text at second level
\\end{quote}
\\end{itemize}
\\end{document}"""

        issues = self.formatter.check_syntax(mixed_content)
        self.assertEqual(issues, [])

    def test_mixed_environment_nesting_invalid(self):
        """Test detection of errors in mixed environment nesting."""
        mixed_content = """\\documentclass{article}
\\begin{document}
\\begin{itemize}
\\item First level list
\\begin{enumerate}
\\item Second level numbered
\\begin{description}
\\item[Term] Third level description
\\end{enumerate}
% Wrong end tag - should be \\end{description}
\\end{description}
\\end{itemize}
\\end{document}"""

        issues = self.formatter.check_syntax(mixed_content)
        self.assertGreater(len(issues), 0)

    def test_math_environment_nesting(self):
        """Test validation of mathematical environment nesting."""
        math_content = """\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
\\begin{align}
x &= \\begin{cases}
1 & \\text{if } n > 0 \\\\
0 & \\text{otherwise}
\\end{cases} \\\\
y &= \\begin{pmatrix}
a & b \\\\
c & d
\\end{pmatrix}
\\end{align}
\\end{document}"""

        issues = self.formatter.check_syntax(math_content)
        self.assertEqual(issues, [])

    def test_table_environment_nesting(self):
        """Test validation of table environment nesting."""
        table_content = """\\documentclass{article}
\\begin{document}
\\begin{table}[htbp]
\\centering
\\begin{tabular}{cc}
\\begin{minipage}{0.4\\textwidth}
Content in minipage
\\end{minipage} &
\\begin{minipage}{0.4\\textwidth}
More content
\\end{minipage} \\\\
\\end{tabular}
\\end{table}
\\end{document}"""

        issues = self.formatter.check_syntax(table_content)
        self.assertEqual(issues, [])


class TestSyntaxValidationEdgeCases(unittest.TestCase):
    """Test edge cases in syntax validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_empty_document(self):
        """Test syntax validation of empty document."""
        empty_content = ""
        issues = self.formatter.check_syntax(empty_content)
        self.assertEqual(issues, [])

    def test_minimal_document(self):
        """Test syntax validation of minimal document."""
        minimal_content = "\\documentclass{article}\\begin{document}\\end{document}"
        issues = self.formatter.check_syntax(minimal_content)
        self.assertEqual(issues, [])

    def test_braces_in_comments(self):
        """Test that braces in comments don't affect validation."""
        content_with_comments = """\\documentclass{article}
\\begin{document}
% This comment has { unmatched braces } but should be ignored
\\section{Real Section}
% Another comment with \\begin{fake} environment
Content here.
\\end{document}"""

        issues = self.formatter.check_syntax(content_with_comments)
        self.assertEqual(issues, [])

    def test_braces_in_verbatim(self):
        """Test that braces in verbatim environments are ignored."""
        verbatim_content = """\\documentclass{article}
\\begin{document}
\\begin{verbatim}
This has { unmatched braces
And \\begin{fake} environments
\\end{verbatim}
\\end{document}"""

        issues = self.formatter.check_syntax(verbatim_content)
        self.assertEqual(issues, [])

    def test_escaped_braces(self):
        """Test handling of escaped braces."""
        escaped_content = """\\documentclass{article}
\\begin{document}
These are literal braces: \\{ and \\}
And these are real braces: \\textbf{bold text}
\\end{document}"""

        issues = self.formatter.check_syntax(escaped_content)
        self.assertEqual(issues, [])

    def test_math_mode_braces(self):
        """Test handling of braces in math mode."""
        math_content = """\\documentclass{article}
\\begin{document}
Inline math: $\\frac{a}{b}$ and $x^{2}$ and $y_{i}$
Display math: $$\\sum_{i=1}^{n} x_{i}$$
\\end{document}"""

        issues = self.formatter.check_syntax(math_content)
        self.assertEqual(issues, [])

    def test_command_arguments(self):
        """Test handling of command arguments with braces."""
        command_content = """\\documentclass{article}
\\begin{document}
\\includegraphics[width=0.5\\textwidth]{image.png}
\\cite{ref1,ref2,ref3}
\\newcommand{\\mycmd}[2]{#1 and #2}
\\end{document}"""

        issues = self.formatter.check_syntax(command_content)
        self.assertEqual(issues, [])

    def test_very_long_line_with_braces(self):
        """Test syntax validation with very long lines containing many braces."""
        long_line = "\\textbf{" + "word " * 100 + "}"
        content = f"""\\documentclass{{article}}
\\begin{{document}}
{long_line}
\\end{{document}}"""

        issues = self.formatter.check_syntax(content)
        self.assertEqual(issues, [])

    def test_multiple_documents_in_content(self):
        """Test handling of multiple document environments (invalid LaTeX)."""
        multi_doc_content = """\\documentclass{article}
\\begin{document}
First document content
\\end{document}

\\begin{document}
Second document content
\\end{document}"""

        issues = self.formatter.check_syntax(multi_doc_content)
        # This should detect environment issues
        self.assertGreater(len(issues), 0)


class TestSyntaxValidationPerformance(unittest.TestCase):
    """Test performance of syntax validation on large inputs."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_large_valid_document(self):
        """Test syntax validation performance on large valid document."""
        # Generate large document with many nested structures
        large_content = "\\documentclass{article}\n\\begin{document}\n"

        for i in range(100):
            large_content += f"""\\section{{Section {i}}}
Content for section {i}.
\\begin{{itemize}}
\\item Item 1 for section {i}
\\item Item 2 for section {i}
\\end{{itemize}}
"""

        large_content += "\\end{document}"

        # Should complete without hanging and report no issues
        issues = self.formatter.check_syntax(large_content)
        self.assertEqual(issues, [])

    def test_large_invalid_document(self):
        """Test syntax validation performance on large invalid document."""
        # Generate large document with systematic errors
        large_content = "\\documentclass{article}\n\\begin{document}\n"

        for i in range(50):
            large_content += f"""\\section{{Section {i}}}
Content for section {i}.
\\begin{{itemize}}
\\item Item 1 for section {i}
% Missing \\end{{itemize}} - systematic error
"""

        large_content += "\\end{document}"

        # Should complete and detect many issues
        issues = self.formatter.check_syntax(large_content)
        self.assertGreater(len(issues), 10)  # Should find many unmatched environments


if __name__ == "__main__":
    unittest.main()
