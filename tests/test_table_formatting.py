#!/usr/bin/env python3
"""
Specialized tests for table alignment functionality
Tests table alignment, column padding, comment preservation, and complex table structures
"""

import unittest

from latex_formatter import LaTeXFormatter
from latex_formatter_advanced import AdvancedLaTeXFormatter


class TestBasicTableAlignment(unittest.TestCase):
    """Test basic table alignment functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_simple_table_alignment(self):
        """Test alignment of simple table structure."""
        rows = ["Name & Age & City", "John & 25 & NYC", "Jane & 30 & Los Angeles"]

        result = self.formatter.align_table_rows(rows)

        # All rows should have consistent spacing
        self.assertTrue(all(" & " in row for row in result))

        # Check column alignment - first column should be padded
        self.assertTrue(result[1].startswith("John "))
        self.assertTrue(result[2].startswith("Jane "))

        # Check that columns are properly aligned
        name_col_end = result[0].find(" & ")
        john_col_end = result[1].find(" & ")
        jane_col_end = result[2].find(" & ")

        self.assertEqual(name_col_end, john_col_end)
        self.assertEqual(name_col_end, jane_col_end)

    def test_uneven_column_widths(self):
        """Test alignment with uneven column widths."""
        rows = ["A & B & C", "VeryLongName & Short & Medium", "X & VeryLongCity & Y"]

        result = self.formatter.align_table_rows(rows)

        # Check that all columns are properly aligned
        for row in result:
            self.assertIn(" & ", row)

        # First column should be padded to accommodate "VeryLongName"
        self.assertTrue(result[0].startswith("A            "))  # A should be padded
        self.assertTrue(result[2].startswith("X            "))  # X should be padded

    def test_single_column_table(self):
        """Test handling of single-column table."""
        rows = ["SingleColumn", "AnotherValue", "ThirdValue"]

        result = self.formatter.align_table_rows(rows)

        # Should return rows unchanged for single column
        self.assertEqual(result, rows)

    def test_empty_cells(self):
        """Test handling of empty table cells."""
        rows = [
            "Name & Age & City",
            "John &  & NYC",
            " & 30 & ",
            "Jane & 25 & Los Angeles",
        ]

        result = self.formatter.align_table_rows(rows)

        # Should handle empty cells gracefully
        self.assertTrue(all(" & " in row for row in result))

        # Empty cells should still be aligned
        for row in result:
            parts = row.split(" & ")
            self.assertEqual(len(parts), 3)  # Should have 3 columns

    def test_numeric_data_alignment(self):
        """Test alignment of tables with numeric data."""
        rows = [
            "Parameter & Value & Unit",
            "Speed & 15.5 & m/s",
            "Acceleration & 9.81 & m/s²",
            "Time & 123.456 & seconds",
        ]

        result = self.formatter.align_table_rows(rows)

        # Check proper alignment
        self.assertTrue(all(" & " in row for row in result))

        # Numeric values should be properly spaced
        self.assertIn("Speed        & 15.5", result[1])
        self.assertIn("Acceleration & 9.81", result[2])


class TestTableAlignmentWithComments(unittest.TestCase):
    """Test table alignment while preserving comments."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_comments_between_rows(self):
        """Test preservation of comments between table rows."""
        rows = [
            "% Table header",
            "Name & Age & City",
            "% Data rows below",
            "John & 25 & NYC",
            "Jane & 30 & LA",
            "% End of table",
        ]

        result = self.formatter.align_table_rows(rows)

        # Comments should be preserved exactly
        self.assertEqual(result[0], "% Table header")
        self.assertEqual(result[2], "% Data rows below")
        self.assertEqual(result[5], "% End of table")

        # Data rows should be aligned
        self.assertIn(" & ", result[1])
        self.assertIn(" & ", result[3])
        self.assertIn(" & ", result[4])

    def test_inline_comments_in_rows(self):
        """Test handling of inline comments within table rows."""
        rows = [
            "Name & Age & City  % Header row",
            "John & 25 & NYC   % First person",
            "Jane & 30 & LA    % Second person",
        ]

        result = self.formatter.align_table_rows(rows)

        # Should preserve inline comments
        for row in result:
            self.assertIn("%", row)

        # Should still align the table parts
        for row in result:
            table_part = row.split("%")[0].strip()
            if "&" in table_part:
                self.assertIn(" & ", table_part)

    def test_mixed_comments_and_data(self):
        """Test complex mixing of comments and data rows."""
        rows = [
            "% Complex table example",
            "Parameter & Value & Unit & Notes",
            "% Physical constants",
            "c & 299792458 & m/s & Speed of light",
            "h & 6.626e-34 & J⋅s & Planck constant",
            "% Mathematical constants",
            "π & 3.14159 & dimensionless & Pi",
            "e & 2.71828 & dimensionless & Euler's number",
            "% End of constants",
        ]

        result = self.formatter.align_table_rows(rows)

        # Comments should be unchanged
        comment_indices = [0, 2, 5, 8]
        for i in comment_indices:
            self.assertTrue(result[i].startswith("%"))

        # Data rows should be aligned
        data_indices = [1, 3, 4, 6, 7]
        for i in data_indices:
            self.assertIn(" & ", result[i])
            # Check that columns are properly aligned
            parts = result[i].split(" & ")
            self.assertEqual(len(parts), 4)


class TestComplexTableStructures(unittest.TestCase):
    """Test alignment of complex table structures."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_tables_with_multicolumn(self):
        """Test handling of tables with multicolumn commands."""
        rows = [
            "\\multicolumn{2}{c}{Group A} & \\multicolumn{2}{c}{Group B}",
            "Name & Age & Name & Age",
            "John & 25 & Jane & 30",
            "Bob & 35 & Alice & 28",
        ]

        result = self.formatter.align_table_rows(rows)

        # Should handle multicolumn commands
        self.assertIn("\\multicolumn{2}{c}{Group A}", result[0])

        # Regular rows should be aligned
        for i in range(1, len(result)):
            self.assertIn(" & ", result[i])

    def test_tables_with_hlines(self):
        """Test handling of tables with horizontal lines."""
        rows = [
            "\\hline",
            "Name & Age & City",
            "\\hline",
            "John & 25 & NYC",
            "Jane & 30 & LA",
            "\\hline",
        ]

        result = self.formatter.align_table_rows(rows)

        # Hlines should be preserved
        self.assertEqual(result[0], "\\hline")
        self.assertEqual(result[2], "\\hline")
        self.assertEqual(result[5], "\\hline")

        # Data rows should be aligned
        self.assertIn(" & ", result[1])
        self.assertIn(" & ", result[3])
        self.assertIn(" & ", result[4])

    def test_tables_with_mathematical_content(self):
        """Test alignment of tables containing mathematical expressions."""
        rows = [
            "Function & Derivative & Integral",
            "$x^2$ & $2x$ & $\\frac{x^3}{3}$",
            "$\\sin(x)$ & $\\cos(x)$ & $-\\cos(x)$",
            "$e^x$ & $e^x$ & $e^x$",
        ]

        result = self.formatter.align_table_rows(rows)

        # Mathematical expressions should be preserved
        self.assertIn("$x^2$", result[1])
        self.assertIn("$\\sin(x)$", result[2])
        self.assertIn("$\\frac{x^3}{3}$", result[1])

        # Alignment should work despite math content
        for row in result:
            self.assertIn(" & ", row)

    def test_tables_with_line_breaks(self):
        """Test handling of tables with manual line breaks."""
        rows = [
            "Long Content & Another Column",
            "This is very long \\\\ content spanning \\\\ multiple lines & Short",
            "Normal & Also \\\\ multi-line",
        ]

        result = self.formatter.align_table_rows(rows)

        # Line breaks should be preserved
        self.assertIn("\\\\", result[1])
        self.assertIn("\\\\", result[2])

        # Alignment should still work
        for row in result:
            self.assertIn(" & ", row)

    def test_booktabs_style_tables(self):
        """Test handling of booktabs-style tables."""
        rows = [
            "\\toprule",
            "Method & Accuracy & Time",
            "\\midrule",
            "Approach A & 94.5\\% & 12.3s",
            "Approach B & 96.2\\% & 18.7s",
            "\\bottomrule",
        ]

        result = self.formatter.align_table_rows(rows)

        # Booktabs commands should be preserved
        self.assertEqual(result[0], "\\toprule")
        self.assertEqual(result[2], "\\midrule")
        self.assertEqual(result[5], "\\bottomrule")

        # Data rows should be aligned
        self.assertIn(" & ", result[1])
        self.assertIn(" & ", result[3])
        self.assertIn(" & ", result[4])


class TestTableAlignmentEdgeCases(unittest.TestCase):
    """Test edge cases in table alignment."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_empty_table_rows(self):
        """Test handling of empty table row list."""
        result = self.formatter.align_table_rows([])
        self.assertEqual(result, [])

    def test_single_row_table(self):
        """Test handling of single row table."""
        rows = ["Name & Age & City"]
        result = self.formatter.align_table_rows(rows)

        # Should return the single row properly formatted
        self.assertEqual(len(result), 1)
        self.assertIn(" & ", result[0])

    def test_inconsistent_column_counts(self):
        """Test handling of rows with different column counts."""
        rows = [
            "A & B & C",  # 3 columns
            "X & Y",  # 2 columns
            "P & Q & R & S",  # 4 columns
            "M & N & O",  # 3 columns
        ]

        result = self.formatter.align_table_rows(rows)

        # Should handle gracefully without crashing
        self.assertEqual(len(result), 4)

        # Each row should maintain its structure
        self.assertEqual(len(result[0].split(" & ")), 3)
        self.assertEqual(len(result[1].split(" & ")), 2)
        self.assertEqual(len(result[2].split(" & ")), 4)
        self.assertEqual(len(result[3].split(" & ")), 3)

    def test_very_wide_columns(self):
        """Test handling of very wide columns."""
        rows = [
            "Short & VeryVeryVeryVeryVeryLongColumnContent & Short",
            "A & B & C",
            "X & Y & Z",
        ]

        result = self.formatter.align_table_rows(rows)

        # Should align properly even with very wide columns
        for row in result:
            self.assertIn(" & ", row)

        # Check that short columns are padded appropriately
        self.assertTrue(result[1].startswith("A     "))
        self.assertTrue(result[2].startswith("X     "))

    def test_special_characters_in_tables(self):
        """Test handling of special characters in table content."""
        rows = [
            "Symbol & Description & Usage",
            "α & Alpha & Greek letter",
            "© & Copyright & Legal symbol",
            "€ & Euro & Currency",
        ]

        result = self.formatter.align_table_rows(rows)

        # Special characters should be preserved
        self.assertIn("α", result[1])
        self.assertIn("©", result[2])
        self.assertIn("€", result[3])

        # Alignment should still work
        for row in result:
            self.assertIn(" & ", row)

    def test_tabs_and_mixed_whitespace(self):
        """Test handling of tabs and mixed whitespace in tables."""
        rows = [
            "Name\t&\tAge\t&\tCity",  # Tabs
            "John  &  25  &  NYC",  # Multiple spaces
            "Jane\t& 30 &\tLA",  # Mixed
        ]

        result = self.formatter.align_table_rows(rows)

        # Should normalize to consistent spacing
        for row in result:
            self.assertIn(" & ", row)
            self.assertNotIn("\t", row)  # Tabs should be normalized


class TestTableAlignmentIntegration(unittest.TestCase):
    """Test table alignment in context of full document formatting."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_table_alignment_in_document(self):
        """Test table alignment within a complete document."""
        content = """\\documentclass{article}
\\usepackage{booktabs}
\\begin{document}
\\section{Results}

\\begin{table}[htbp]
\\centering
\\caption{Experimental results}
\\begin{tabular}{lcc}
\\toprule
Method&Accuracy&Time\\\\
\\midrule
Approach A&94.5\\%&12.3s\\\\
Approach B&96.2\\%&18.7s\\\\
\\bottomrule
\\end{tabular}
\\end{table}

\\end{document}"""

        result = self.formatter.format_content(content)

        # Table should be properly aligned
        self.assertIn("Method & Accuracy & Time", result)
        self.assertIn("Approach A & 94.5\\% & 12.3s", result)
        self.assertIn("Approach B & 96.2\\% & 18.7s", result)

        # Other document structure should be preserved
        self.assertIn("\\documentclass{article}", result)
        self.assertIn("\\begin{table}", result)
        self.assertIn("\\caption{Experimental results}", result)

    def test_multiple_tables_in_document(self):
        """Test alignment of multiple tables in a document."""
        content = """\\documentclass{article}
\\begin{document}

\\begin{tabular}{cc}
A&B\\\\
C&D
\\end{tabular}

Text between tables.

\\begin{tabular}{ccc}
X&Y&Z\\\\
1&2&3\\\\
4&5&6
\\end{tabular}

\\end{document}"""

        result = self.formatter.format_content(content)

        # Both tables should be aligned
        self.assertIn("A & B", result)
        self.assertIn("C & D", result)
        self.assertIn("X & Y & Z", result)
        self.assertIn("1 & 2 & 3", result)
        self.assertIn("4 & 5 & 6", result)

        # Text between should be preserved
        self.assertIn("Text between tables.", result)

    def test_table_alignment_with_disabled_option(self):
        """Test that table alignment can be disabled via configuration."""
        config = self.formatter.config.copy()
        config["align_ampersands"] = False
        formatter = LaTeXFormatter(config)

        content = """\\begin{tabular}{cc}
Name&Age\\\\
John&25
\\end{tabular}"""

        result = formatter.format_content(content)

        # Should NOT be aligned when disabled
        self.assertIn("Name&Age", result)
        self.assertIn("John&25", result)

    def test_table_alignment_performance(self):
        """Test performance of table alignment with large tables."""
        # Generate a large table
        rows = ["Col1 & Col2 & Col3 & Col4 & Col5"]
        for i in range(100):
            rows.append(f"Data{i} & Value{i} & Result{i} & Status{i} & Note{i}")

        # Should complete without performance issues
        result = self.formatter.align_table_rows(rows)

        self.assertEqual(len(result), 101)  # Header + 100 data rows

        # Check that alignment was applied
        for row in result:
            self.assertIn(" & ", row)
            parts = row.split(" & ")
            self.assertEqual(len(parts), 5)


if __name__ == "__main__":
    unittest.main()
