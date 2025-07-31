#!/usr/bin/env python3
"""
TDD Cycle 2 Summary: Cross-Reference Formatting
Demonstrates the complete implementation and integration
"""

import unittest

from latex_formatter import LaTeXFormatter


class TestTDDCycle2Summary(unittest.TestCase):
    """Summary test demonstrating TDD Cycle 2 success."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_tdd_cycle2_complete_integration(self):
        """Comprehensive test showing all TDD Cycle 2 features working together."""
        input_content = """\\documentclass{article}
\\usepackage{amsmath}
\\usepackage{natbib}
\\begin{document}

\\section{Introduction}\\label   {   sec:intro   }
This paper presents new findings. We cite \\cite   {   author2023   }.

\\section{Background}\\label{sec:background}
Previous work by \\citet   {   smith2022   } is relevant.
See Section \\ref   {   sec:intro   }for context.

\\begin{equation}\\label   {   eq:fundamental   }
E = mc^2
\\end{equation}

\\begin{figure}\\label   {   fig:results   }
\\caption{Main results}
\\end{figure}

\\section{Results}\\label{sec:results}
Our key finding is shown in Equation \\eqref   {   eq:fundamental   }.
Figure \\ref   {   fig:results   } on page \\pageref   {   fig:results   }
illustrates this concept.

\\section{Conclusion}\\label{sec:conclusion}
We conclude by referencing Section \\ref{sec:background}.

\\bibliographystyle   {   plain   }
\\bibliography   {   references   }

\\end{document}"""

        result = self.formatter.format_content(input_content)

        # Verify TDD Cycle 1 features (Bibliography) still work
        self.assertIn("\\cite{author2023}", result)
        self.assertIn("\\citet{smith2022}", result)
        self.assertIn("\\bibliographystyle{plain}", result)
        self.assertIn("\\bibliography{references}", result)

        # Verify TDD Cycle 2 features (Cross-references) work
        self.assertIn("\\label{sec:intro}", result)
        self.assertIn("\\label{eq:fundamental}", result)
        self.assertIn("\\label{fig:results}", result)
        self.assertIn("\\ref{sec:intro} for", result)  # Spacing fixed
        self.assertIn("\\eqref{eq:fundamental}", result)
        self.assertIn("\\pageref{fig:results}", result)

        # Verify no malformed commands remain
        self.assertNotIn("\\label   {", result)
        self.assertNotIn("\\ref   {", result)
        self.assertNotIn("\\cite   {", result)

        # Verify cross-reference validation works
        issues = self.formatter.check_crossreferences(result)
        # Should have no undefined references (all are properly defined)
        undefined_refs = [issue for issue in issues if "Undefined reference" in issue]
        self.assertEqual(len(undefined_refs), 0)

    def test_both_tdd_cycles_configuration(self):
        """Test that both TDD cycle features can be configured independently."""
        # Test with both features enabled (default)
        config1 = self.formatter.default_config()
        self.assertTrue(config1["format_bibliography"])
        self.assertTrue(config1["format_crossreferences"])

        # Test with bibliography disabled, cross-references enabled
        config2 = self.formatter.default_config()
        config2["format_bibliography"] = False
        config2["format_crossreferences"] = True
        formatter2 = LaTeXFormatter(config2)

        self.assertFalse(formatter2.config["format_bibliography"])
        self.assertTrue(formatter2.config["format_crossreferences"])

        # Test with cross-references disabled, bibliography enabled
        config3 = self.formatter.default_config()
        config3["format_bibliography"] = True
        config3["format_crossreferences"] = False
        formatter3 = LaTeXFormatter(config3)

        self.assertTrue(formatter3.config["format_bibliography"])
        self.assertFalse(formatter3.config["format_crossreferences"])


if __name__ == "__main__":
    unittest.main()
