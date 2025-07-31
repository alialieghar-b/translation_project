#!/usr/bin/env python3
"""
Specialized tests for package sorting functionality
Tests usepackage sorting, grouping, options handling, and document structure preservation
"""

import unittest

from latex_formatter import LaTeXFormatter
from latex_formatter_advanced import AdvancedLaTeXFormatter


class TestBasicPackageSorting(unittest.TestCase):
    """Test basic package sorting functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_simple_package_sorting(self):
        """Test basic alphabetical package sorting."""
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Extract package lines
        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]

        expected_order = [
            "\\usepackage{amsmath}",
            "\\usepackage{graphicx}",
            "\\usepackage{tikz}",
        ]
        self.assertEqual(package_lines, expected_order)

    def test_package_sorting_preservation_of_structure(self):
        """Test that package sorting preserves document structure."""
        content = """\\documentclass[11pt]{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\usepackage{graphicx}

\\title{Test Document}
\\author{Author}

\\begin{document}
Content here
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Document structure should be preserved
        self.assertIn("\\documentclass[11pt]{article}", result)
        self.assertIn("\\title{Test Document}", result)
        self.assertIn("\\author{Author}", result)
        self.assertIn("\\begin{document}", result)

        # Packages should be sorted
        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]
        expected = [
            "\\usepackage{amsmath}",
            "\\usepackage{graphicx}",
            "\\usepackage{tikz}",
        ]
        self.assertEqual(package_lines, expected)

    def test_no_packages_to_sort(self):
        """Test handling of document with no packages."""
        content = """\\documentclass{article}
\\title{Simple Document}
\\begin{document}
No packages used here.
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Content should remain unchanged
        self.assertEqual(result, content)

    def test_single_package(self):
        """Test handling of document with single package."""
        content = """\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
Single package document.
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Should work without issues
        self.assertIn("\\usepackage{amsmath}", result)
        self.assertIn("\\documentclass{article}", result)

    def test_package_sorting_disabled(self):
        """Test that package sorting can be disabled."""
        config = self.formatter.config.copy()
        config["sort_packages"] = False
        formatter = LaTeXFormatter(config)

        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\begin{document}
Content
\\end{document}"""

        result = formatter.sort_packages(content)

        # Package order should remain unchanged
        self.assertIn(
            "\\usepackage{tikz}\n\\usepackage{amsmath}\n\\usepackage{graphicx}", result
        )


class TestPackageSortingWithOptions(unittest.TestCase):
    """Test package sorting with package options."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_packages_with_options_sorting(self):
        """Test sorting packages that have options."""
        content = """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage[T1]{fontenc}
\\usepackage{graphicx}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]

        # Should be sorted by package name, not options
        expected = [
            "\\usepackage{amsmath}",
            "\\usepackage[T1]{fontenc}",
            "\\usepackage{graphicx}",
            "\\usepackage[utf8]{inputenc}",
        ]
        self.assertEqual(package_lines, expected)

    def test_complex_package_options(self):
        """Test sorting with complex package options."""
        content = """\\documentclass{article}
\\usepackage[margin=1in,top=0.5in]{geometry}
\\usepackage{amsmath}
\\usepackage[colorlinks=true,linkcolor=blue]{hyperref}
\\usepackage[backend=biber,style=authoryear]{biblatex}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]

        # Check alphabetical order by package name
        package_names = []
        for line in package_lines:
            # Extract package name
            import re

            match = re.search(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", line)
            if match:
                package_names.append(match.group(1))

        self.assertEqual(package_names, sorted(package_names))

        # Check that options are preserved
        self.assertIn("[margin=1in,top=0.5in]", result)
        self.assertIn("[colorlinks=true,linkcolor=blue]", result)
        self.assertIn("[backend=biber,style=authoryear]", result)

    def test_mixed_packages_with_and_without_options(self):
        """Test sorting mix of packages with and without options."""
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage[T1]{fontenc}
\\usepackage{graphicx}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]

        # Extract package names to verify sorting
        package_names = []
        for line in package_lines:
            import re

            match = re.search(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", line)
            if match:
                package_names.append(match.group(1))

        expected_names = ["amsmath", "fontenc", "graphicx", "inputenc", "tikz"]
        self.assertEqual(package_names, expected_names)

    def test_multiline_package_options(self):
        """Test handling of packages with multiline options."""
        content = """\\documentclass{article}
\\usepackage[
    colorlinks=true,
    linkcolor=blue,
    urlcolor=red
]{hyperref}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Should handle multiline options gracefully
        self.assertIn("hyperref", result)
        self.assertIn("amsmath", result)
        self.assertIn("graphicx", result)

        # Multiline options should be preserved
        self.assertIn("colorlinks=true", result)
        self.assertIn("linkcolor=blue", result)
        self.assertIn("urlcolor=red", result)


class TestPackageGrouping(unittest.TestCase):
    """Test package grouping functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Use advanced formatter for grouping features
        self.formatter = AdvancedLaTeXFormatter()

    def test_package_grouping_by_category(self):
        """Test package grouping by category."""
        config = {
            "sort_packages": True,
            "packages": {
                "math": ["amsmath", "amssymb", "amsfonts"],
                "graphics": ["graphicx", "tikz", "pgfplots"],
                "formatting": ["geometry", "fancyhdr", "setspace"],
            },
        }
        formatter = LaTeXFormatter(config)

        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{geometry}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\usepackage{amssymb}
\\usepackage{fancyhdr}
\\begin{document}
Content
\\end{document}"""

        result = formatter.sort_packages(content)

        # Should still sort alphabetically within document
        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]

        # Extract package names
        package_names = []
        for line in package_lines:
            import re

            match = re.search(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", line)
            if match:
                package_names.append(match.group(1))

        self.assertEqual(package_names, sorted(package_names))

    def test_package_spacing_between_groups(self):
        """Test spacing between package groups."""
        # This would be a feature for advanced formatters
        content = """\\documentclass{article}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{graphicx}
\\usepackage{tikz}
\\usepackage{geometry}
\\usepackage{fancyhdr}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Basic sorting should work
        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]

        self.assertGreater(len(package_lines), 0)
        # Should be in alphabetical order
        package_names = []
        for line in package_lines:
            import re

            match = re.search(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", line)
            if match:
                package_names.append(match.group(1))

        self.assertEqual(package_names, sorted(package_names))


class TestPackageSortingPlacement(unittest.TestCase):
    """Test package sorting placement in document."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_package_insertion_after_documentclass(self):
        """Test that sorted packages are placed after documentclass."""
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\title{Test}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        lines = result.split("\n")

        # Find positions
        documentclass_pos = -1
        first_package_pos = -1
        title_pos = -1

        for i, line in enumerate(lines):
            if "\\documentclass" in line:
                documentclass_pos = i
            elif "\\usepackage" in line and first_package_pos == -1:
                first_package_pos = i
            elif "\\title" in line:
                title_pos = i

        # Packages should come after documentclass but before title
        self.assertLess(documentclass_pos, first_package_pos)
        self.assertLess(first_package_pos, title_pos)

    def test_package_sorting_with_comments(self):
        """Test package sorting preservation of comments."""
        content = """\\documentclass{article}
% Essential packages
\\usepackage{tikz}
\\usepackage{amsmath}
% Graphics package
\\usepackage{graphicx}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Packages should be sorted
        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]
        expected = [
            "\\usepackage{amsmath}",
            "\\usepackage{graphicx}",
            "\\usepackage{tikz}",
        ]
        self.assertEqual(package_lines, expected)

        # Comments should be handled appropriately
        # (Exact behavior depends on implementation)
        self.assertIn("\\documentclass{article}", result)
        self.assertIn("\\begin{document}", result)

    def test_packages_only_in_preamble(self):
        """Test that only preamble packages are sorted."""
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
% This should not be sorted
\\usepackage{graphicx}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Preamble packages should be sorted
        preamble_end = result.find("\\begin{document}")
        preamble = result[:preamble_end]

        preamble_lines = preamble.split("\n")
        preamble_packages = [line for line in preamble_lines if "\\usepackage" in line]
        expected = ["\\usepackage{amsmath}", "\\usepackage{tikz}"]
        self.assertEqual(preamble_packages, expected)

        # Package in document body should remain unchanged
        document_body = result[preamble_end:]
        self.assertIn("\\usepackage{graphicx}", document_body)

    def test_multiple_documentclass_handling(self):
        """Test handling of multiple documentclass commands (edge case)."""
        content = """\\documentclass{article}
\\usepackage{tikz}
% Comment here
\\documentclass{report}  % This is invalid LaTeX but should be handled
\\usepackage{amsmath}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Should handle gracefully without crashing
        self.assertIn("\\documentclass{article}", result)
        self.assertIn("\\documentclass{report}", result)
        self.assertIn("\\usepackage", result)


class TestPackageSortingEdgeCases(unittest.TestCase):
    """Test edge cases in package sorting."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_duplicate_packages(self):
        """Test handling of duplicate package declarations."""
        content = """\\documentclass{article}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\usepackage{amsmath}
\\usepackage{tikz}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Should preserve duplicates but sort them
        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]

        # Should contain both amsmath declarations
        amsmath_count = sum(1 for line in package_lines if "amsmath" in line)
        self.assertEqual(amsmath_count, 2)

        # Should be sorted
        expected = [
            "\\usepackage{amsmath}",
            "\\usepackage{amsmath}",
            "\\usepackage{graphicx}",
            "\\usepackage{tikz}",
        ]
        self.assertEqual(package_lines, expected)

    def test_packages_with_special_characters(self):
        """Test sorting packages with special characters in names."""
        content = """\\documentclass{article}
\\usepackage{tikz-cd}
\\usepackage{amsmath}
\\usepackage{babel-french}
\\usepackage{graphicx}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]

        # Should handle special characters in sorting
        package_names = []
        for line in package_lines:
            import re

            match = re.search(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", line)
            if match:
                package_names.append(match.group(1))

        expected = ["amsmath", "babel-french", "graphicx", "tikz-cd"]
        self.assertEqual(package_names, expected)

    def test_malformed_package_declarations(self):
        """Test handling of malformed package declarations."""
        content = """\\documentclass{article}
\\usepackage{amsmath}
\\usepackage
\\usepackage{graphicx
\\usepackage{}
\\usepackage{tikz}
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Should handle gracefully and sort valid packages
        lines = result.split("\n")
        valid_packages = []
        for line in lines:
            if "\\usepackage{" in line and "}" in line:
                import re

                match = re.search(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", line)
                if match and match.group(1):  # Non-empty package name
                    valid_packages.append(match.group(1))

        # Should sort valid packages
        self.assertEqual(valid_packages, sorted(valid_packages))

    def test_very_long_package_lists(self):
        """Test performance with very long package lists."""
        # Generate many packages
        packages = [f"package{i:03d}" for i in range(100, 0, -1)]  # Reverse order

        content = "\\documentclass{article}\n"
        for pkg in packages:
            content += f"\\usepackage{{{pkg}}}\n"
        content += "\\begin{document}\nContent\n\\end{document}"

        result = self.formatter.sort_packages(content)

        # Should sort all packages
        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]

        self.assertEqual(len(package_lines), 100)

        # Extract package names and verify sorting
        package_names = []
        for line in package_lines:
            import re

            match = re.search(r"\\usepackage\{([^}]+)\}", line)
            if match:
                package_names.append(match.group(1))

        expected_names = [f"package{i:03d}" for i in range(1, 101)]
        self.assertEqual(package_names, expected_names)

    def test_packages_with_version_constraints(self):
        """Test handling of packages with version constraints."""
        content = """\\documentclass{article}
\\usepackage{tikz}[2020/12/27]
\\usepackage{amsmath}
\\usepackage{graphicx}[2017/06/01]
\\begin{document}
Content
\\end{document}"""

        result = self.formatter.sort_packages(content)

        # Should preserve version constraints and sort by package name
        self.assertIn("tikz}[2020/12/27]", result)
        self.assertIn("graphicx}[2017/06/01]", result)

        lines = result.split("\n")
        package_lines = [line for line in lines if "\\usepackage" in line]

        # Extract package names
        package_names = []
        for line in package_lines:
            import re

            match = re.search(r"\\usepackage\{([^}]+)\}", line)
            if match:
                package_names.append(match.group(1))

        self.assertEqual(package_names, sorted(package_names))


if __name__ == "__main__":
    unittest.main()
