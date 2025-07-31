#!/usr/bin/env python3
"""
TDD Tests for Bibliography Formatting Feature
Following Red-Green-Refactor cycle
"""

import unittest

from latex_formatter import LaTeXFormatter


class TestBibliographyFormatting(unittest.TestCase):
    """TDD tests for bibliography formatting functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_format_bibliography_command(self):
        """GREEN: Test that \\bibliography command is properly formatted."""
        # Test input with poorly formatted bibliography command
        input_content = """\\documentclass{article}
\\begin{document}
\\bibliography   {   references   }
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that the bibliography command is properly formatted (no extra spaces)
        self.assertIn("\\bibliography{references}", result)
        # Check that extra spaces are removed
        self.assertNotIn("\\bibliography   {", result)
        self.assertNotIn("{   references   }", result)

    def test_format_bibliographystyle_command(self):
        """GREEN: Test that \\bibliographystyle command is properly formatted."""
        input_content = """\\documentclass{article}
\\begin{document}
\\bibliographystyle   {   plain   }
\\bibliography{references}
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that bibliographystyle command is properly formatted
        self.assertIn("\\bibliographystyle{plain}", result)
        self.assertIn("\\bibliography{references}", result)
        # Check that extra spaces are removed
        self.assertNotIn("\\bibliographystyle   {", result)
        self.assertNotIn("{   plain   }", result)

    def test_format_cite_commands(self):
        """GREEN: Test that \\cite commands are properly formatted."""
        input_content = """\\documentclass{article}
\\begin{document}
This is a citation \\cite   {   author2023   }.
Multiple citations \\cite   {   author2023,   smith2022   }.
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that cite commands are properly formatted
        self.assertIn("\\cite{author2023}", result)
        self.assertIn("\\cite{author2023, smith2022}", result)
        # Check that extra spaces are removed
        self.assertNotIn("\\cite   {", result)
        self.assertNotIn("{   author2023   }", result)

    def test_format_bibitem_entries(self):
        """GREEN: Test that \\bibitem entries in thebibliography are formatted."""
        input_content = """\\documentclass{article}
\\begin{document}
\\begin{thebibliography}{99}
\\bibitem   {   author2023   }   Author, A. (2023). Title of Paper.
\\bibitem{smith2022}Smith, B. (2022). Another Paper.
\\end{thebibliography}
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that bibitem entries are properly formatted
        self.assertIn(
            "\\bibitem{author2023} Author, A. (2023). Title of Paper.", result
        )
        self.assertIn("\\bibitem{smith2022} Smith, B. (2022). Another Paper.", result)
        # Check that extra spaces are removed
        self.assertNotIn("\\bibitem   {", result)
        self.assertNotIn("{   author2023   }", result)

    def test_format_natbib_commands(self):
        """GREEN: Test that natbib commands are properly formatted."""
        input_content = """\\documentclass{article}
\\usepackage{natbib}
\\begin{document}
Text with \\citep   {   author2023   } and \\citet   {   smith2022   }.
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that natbib commands are properly formatted
        self.assertIn("\\citep{author2023}", result)
        self.assertIn("\\citet{smith2022}", result)
        # Check that extra spaces are removed
        self.assertNotIn("\\citep   {", result)
        self.assertNotIn("\\citet   {", result)

    def test_bibliography_section_spacing(self):
        """GREEN: Test that bibliography sections have proper spacing."""
        input_content = """\\documentclass{article}
\\begin{document}
Some text before bibliography.
\\bibliography{references}
Some text after bibliography.
\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Check that bibliography command is present and properly formatted
        self.assertIn("\\bibliography{references}", result)
        # Check that there's some spacing around bibliography
        # (the exact spacing may vary)
        lines = result.split("\n")
        bib_line_idx = next(
            i for i, line in enumerate(lines) if "\\bibliography{references}" in line
        )

        # There should be some content before and after the bibliography line
        self.assertTrue(bib_line_idx > 0)
        self.assertTrue(bib_line_idx < len(lines) - 1)


if __name__ == "__main__":
    unittest.main()
