#!/usr/bin/env python3
"""
Final tests to achieve 100% coverage
"""

import tempfile
import unittest
from pathlib import Path

from latex_formatter import LaTeXFormatter


class TestFinalCoverage(unittest.TestCase):
    """Test remaining uncovered lines."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_sort_packages_no_blank_line_needed(self):
        """Test package sorting when no blank line is needed after packages."""
        # This should hit line 651 where next_line_idx >= len(lines)
        content = """\\documentclass{article}
\\usepackage{amsmath}
\\usepackage{graphicx}"""

        result = self.formatter.sort_packages(content)

        # Should sort packages
        lines = result.split("\n")
        package_lines = [line for line in lines if "usepackage" in line]
        self.assertEqual(package_lines[0], "\\usepackage{amsmath}")
        self.assertEqual(package_lines[1], "\\usepackage{graphicx}")

    def test_align_table_rows_max_cols_one(self):
        """Test table alignment when max columns is 1 or less."""
        # This should hit line 734 where max_cols <= 1
        rows = ["Single column row", "Another single row"]
        result = self.formatter.align_table_rows(rows)
        self.assertEqual(result, ["Single column row", "Another single row"])

    def test_main_function_direct_call(self):
        """Test calling main() function directly to hit line 956."""
        # Create a simple test file
        test_file = Path(self.temp_dir) / "test.tex"
        test_file.write_text(
            "\\documentclass{article}\n\\begin{document}\nTest\n\\end{document}"
        )

        # Import and test the main function directly
        from unittest.mock import patch

        # Test the if __name__ == "__main__": block
        with patch("sys.argv", ["latex-formatter", str(test_file)]):
            with patch("builtins.print"):
                # This should execute the main() function
                from latex_formatter import main

                main()

    def test_table_alignment_edge_case_single_column_table(self):
        """Test table with only single column entries."""
        content = """\\begin{tabular}{c}
Header
Data1
Data2
\\end{tabular}"""

        result = self.formatter.align_tables(content)
        # Should handle single column tables gracefully
        self.assertIn("Header", result)
        self.assertIn("Data1", result)

    def test_package_sorting_edge_case_no_insertion_point(self):
        """Test package sorting edge case."""
        # Test with packages but unusual structure
        content = """\\documentclass{article}
% Comment before packages
\\usepackage{amsmath}
% Comment after packages
\\begin{document}
Test
\\end{document}"""

        result = self.formatter.sort_packages(content)
        self.assertIn("\\usepackage{amsmath}", result)

    def test_environment_formatting_end_document_special_case(self):
        """Test that \\end{document} is never indented."""
        content = """\\documentclass{article}
\\begin{document}
\\begin{itemize}
\\item Test
\\end{itemize}
\\end{document}"""

        result = self.formatter.format_environments(content)
        lines = result.split("\n")

        # Find \\end{document} line
        end_doc_line = next(line for line in lines if line.strip() == "\\end{document}")
        self.assertEqual(end_doc_line, "\\end{document}")  # Should not be indented


if __name__ == "__main__":
    unittest.main()
