#!/usr/bin/env python3
"""
TDD Tests for Cross-Reference Formatting Feature
Following Red-Green-Refactor cycle
"""

import unittest

from latex_formatter import LaTeXFormatter


class TestCrossReferenceFormatting(unittest.TestCase):
    """TDD tests for cross-reference formatting functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_format_label_commands(self):
        """RED: Test that \\label commands are properly formatted."""
        input_content = """\\documentclass{article}
\\begin{document}
\\section{Introduction}\\label   {   sec:intro   }
\\subsection{Background}\\label{subsec:background}
Some text here.
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that label commands are properly formatted
        self.assertIn("\\label{sec:intro}", result)
        self.assertIn("\\label{subsec:background}", result)
        # Check that extra spaces are removed
        self.assertNotIn("\\label   {", result)
        self.assertNotIn("{   sec:intro   }", result)

    def test_format_ref_commands(self):
        """RED: Test that \\ref commands are properly formatted."""
        input_content = """\\documentclass{article}
\\begin{document}
See Section \\ref   {   sec:intro   } for details.
Also refer to \\ref{subsec:background} and \\pageref   {   sec:conclusion   }.
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that ref commands are properly formatted
        self.assertIn("\\ref{sec:intro}", result)
        self.assertIn("\\ref{subsec:background}", result)
        self.assertIn("\\pageref{sec:conclusion}", result)
        # Check that extra spaces are removed
        self.assertNotIn("\\ref   {", result)
        self.assertNotIn("\\pageref   {", result)

    def test_format_eqref_commands(self):
        """RED: Test that \\eqref commands are properly formatted."""
        input_content = """\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
The equation \\eqref   {   eq:main   } shows the relationship.
See also \\eqref{eq:secondary}.
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that eqref commands are properly formatted
        self.assertIn("\\eqref{eq:main}", result)
        self.assertIn("\\eqref{eq:secondary}", result)
        # Check that extra spaces are removed
        self.assertNotIn("\\eqref   {", result)

    def test_label_placement_after_sections(self):
        """RED: Test that labels are properly placed after section commands."""
        input_content = """\\documentclass{article}
\\begin{document}
\\section{Introduction}
\\label{sec:intro}
\\subsection{Background}\\label{subsec:bg}
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that labels are present and properly formatted
        self.assertIn("\\label{sec:intro}", result)
        self.assertIn("\\label{subsec:bg}", result)

    def test_crossref_spacing_normalization(self):
        """RED: Test that cross-references have proper spacing."""
        input_content = """\\documentclass{article}
\\begin{document}
See Section~\\ref{sec:intro}for details.
Also refer to\\ref{subsec:background} and \\pageref{sec:conclusion}.
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that proper spacing is maintained around references
        # Should have space before and after references
        self.assertIn("Section~\\ref{sec:intro} for", result)
        self.assertIn("refer to \\ref{subsec:background}", result)

    def test_crossref_validation_basic(self):
        """RED: Test basic cross-reference validation."""
        input_content = """\\documentclass{article}
\\begin{document}
\\section{Introduction}\\label{sec:intro}
See Section \\ref{sec:intro} for details.
Also see \\ref{sec:nonexistent}.
\\end{document}"""

        # This test will check that the formatter can identify cross-reference issues
        issues = self.formatter.check_crossreferences(input_content)

        # Should find the undefined reference
        self.assertTrue(any("sec:nonexistent" in issue for issue in issues))
        # Should not complain about the valid reference
        self.assertFalse(
            any("sec:intro" in issue and "undefined" in issue for issue in issues)
        )

    def test_multiple_crossref_types(self):
        """RED: Test formatting of multiple cross-reference types."""
        input_content = """\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
\\section{Introduction}\\label   {   sec:intro   }
\\begin{equation}\\label   {   eq:main   }
E = mc^2
\\end{equation}
\\begin{figure}\\label   {   fig:diagram   }
\\caption{A diagram}
\\end{figure}

See Section \\ref   {   sec:intro   }, Equation \\eqref   {   eq:main   },
and Figure \\ref   {   fig:diagram   } on page \\pageref   {   fig:diagram   }.
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check all label types are formatted
        self.assertIn("\\label{sec:intro}", result)
        self.assertIn("\\label{eq:main}", result)
        self.assertIn("\\label{fig:diagram}", result)

        # Check all reference types are formatted
        self.assertIn("\\ref{sec:intro}", result)
        self.assertIn("\\eqref{eq:main}", result)
        self.assertIn("\\ref{fig:diagram}", result)
        self.assertIn("\\pageref{fig:diagram}", result)


if __name__ == "__main__":
    unittest.main()
