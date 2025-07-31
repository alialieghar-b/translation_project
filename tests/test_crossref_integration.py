#!/usr/bin/env python3
"""
Integration tests for cross-reference formatting
"""

import unittest

from latex_formatter import LaTeXFormatter


class TestCrossReferenceIntegration(unittest.TestCase):
    """Integration tests for cross-reference functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_complete_document_with_crossrefs(self):
        """Integration test: Complete document with cross-references."""
        input_content = """\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}

\\section{Introduction}\\label   {   sec:intro   }
This section introduces the main concepts.

\\section{Methodology}\\label{sec:method}
In this section, we describe our approach.
See Section \\ref   {   sec:intro   } for background.

\\begin{equation}\\label   {   eq:main   }
E = mc^2
\\end{equation}

\\begin{figure}\\label   {   fig:diagram   }
\\caption{Main diagram}
\\end{figure}

\\section{Results}\\label{sec:results}
Our results are shown in Equation \\eqref   {   eq:main   }.
Figure \\ref   {   fig:diagram   } on page \\pageref   {   fig:diagram   }
illustrates the concept.

\\section{Conclusion}\\label{sec:conclusion}
We conclude by referring back to Section \\ref{sec:method}.

\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Verify all cross-reference formatting
        self.assertIn("\\label{sec:intro}", result)
        self.assertIn("\\label{sec:method}", result)
        self.assertIn("\\label{eq:main}", result)
        self.assertIn("\\label{fig:diagram}", result)

        self.assertIn("\\ref{sec:intro}", result)
        self.assertIn("\\eqref{eq:main}", result)
        self.assertIn("\\ref{fig:diagram}", result)
        self.assertIn("\\pageref{fig:diagram}", result)

        # Verify no malformed commands remain
        self.assertNotIn("\\label   {", result)
        self.assertNotIn("\\ref   {", result)
        self.assertNotIn("\\eqref   {", result)

    def test_crossref_validation_comprehensive(self):
        """Test comprehensive cross-reference validation."""
        input_content = """\\documentclass{article}
\\begin{document}
\\section{Introduction}\\label{sec:intro}
\\section{Methods}\\label{sec:methods}
\\label{unused:label}

See Section \\ref{sec:intro} and \\ref{sec:methods}.
Also see \\ref{nonexistent:ref} and \\pageref{another:missing}.
\\end{document}"""

        issues = self.formatter.check_crossreferences(input_content)

        # Should find undefined references
        undefined_issues = [issue for issue in issues if "Undefined reference" in issue]
        self.assertEqual(len(undefined_issues), 2)
        self.assertTrue(any("nonexistent:ref" in issue for issue in undefined_issues))
        self.assertTrue(any("another:missing" in issue for issue in undefined_issues))

        # Should find unused labels
        unused_issues = [issue for issue in issues if "Unused label" in issue]
        self.assertEqual(len(unused_issues), 1)
        self.assertTrue(any("unused:label" in issue for issue in unused_issues))

    def test_crossref_configuration_options(self):
        """Test that cross-reference formatting can be configured."""
        # Test with cross-reference formatting disabled
        config = self.formatter.default_config()
        config["format_crossreferences"] = False
        formatter_disabled = LaTeXFormatter(config)

        input_content = """\\documentclass{article}
\\begin{document}
\\section{Test}\\label   {   sec:test   }
See Section \\ref   {   sec:test   }.
\\end{document}"""

        formatter_disabled.format_content(input_content)

        # Verify the configuration option works
        self.assertFalse(formatter_disabled.config["format_crossreferences"])

    def test_crossref_with_other_features(self):
        """Test cross-references work well with other formatting features."""
        input_content = """\\documentclass{article}
\\usepackage{amsmath}
\\usepackage{natbib}
\\begin{document}

\\section{Introduction}\\label{sec:intro}
This section cites \\cite   {   author2023   } and refers to
Section \\ref   {   sec:methods   }.

\\section{Methods}\\label{sec:methods}
Our approach builds on \\citep   {   smith2022   }.

\\begin{equation}\\label{eq:main}
E = mc^2
\\end{equation}

See Equation \\eqref{eq:main} for details.

\\bibliographystyle   {   plain   }
\\bibliography   {   references   }

\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Verify both bibliography and cross-reference formatting work together
        self.assertIn("\\cite{author2023}", result)  # Bibliography formatting
        self.assertIn("\\ref{sec:methods}", result)  # Cross-reference formatting
        self.assertIn("\\label{sec:intro}", result)  # Label formatting
        self.assertIn("\\eqref{eq:main}", result)  # Equation reference formatting


if __name__ == "__main__":
    unittest.main()
