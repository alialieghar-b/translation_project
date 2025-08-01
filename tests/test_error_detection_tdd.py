#!/usr/bin/env python3
"""
TDD Tests for Enhanced Error Detection in LaTeX Formatter
Tests for detecting undefined commands, package compatibility, and other issues found in the real-world file.
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from latex_formatter import LaTeXFormatter
from latex_formatter_advanced import AdvancedLaTeXFormatter


class TestUndefinedCommandDetection(unittest.TestCase):
    """Test detection of undefined commands like \\farsifontbold."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_detect_undefined_farsifontbold(self):
        """Test detection of undefined \\farsifontbold command."""
        content = """
\\documentclass{article}
\\usepackage{fontspec}
\\newfontfamily\\farsifont[Script=Arabic]{Noto Sans Arabic}
\\newcommand{\\farsibold}[1]{{\\farsifontbold{#1}}}
\\begin{document}
\\farsibold{Test}
\\end{document}
"""
        # This should fail initially - formatter doesn't detect undefined commands yet
        issues = self.formatter.detect_undefined_commands(content)
        self.assertIn("farsifontbold", [issue["command"] for issue in issues])
        self.assertEqual(issues[0]["type"], "undefined_command")
        self.assertEqual(issues[0]["line"], 5)

    def test_detect_undefined_command_in_newcommand(self):
        """Test detection of undefined commands within \\newcommand definitions."""
        content = """
\\newcommand{\\mybold}[1]{{\\unknowncommand{#1}}}
"""
        issues = self.formatter.detect_undefined_commands(content)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["command"], "unknowncommand")

    def test_no_false_positives_for_defined_commands(self):
        """Test that defined commands are not flagged as undefined."""
        content = """
\\documentclass{article}
\\usepackage{fontspec}
\\newfontfamily\\farsifont[Script=Arabic]{Noto Sans Arabic}
\\newcommand{\\farsibold}[1]{{\\farsifont\\bfseries #1}}
\\begin{document}
\\farsibold{Test}
\\end{document}
"""
        issues = self.formatter.detect_undefined_commands(content)
        self.assertEqual(len(issues), 0)


class TestPackageCompatibilityDetection(unittest.TestCase):
    """Test detection of package compatibility issues."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_detect_fontspec_with_pdflatex(self):
        """Test detection of fontspec package incompatibility with pdfLaTeX."""
        content = """
\\documentclass{article}
\\usepackage{fontspec}
\\usepackage[utf8]{inputenc}
\\begin{document}
Test
\\end{document}
"""
        issues = self.formatter.detect_engine_compatibility_issues(content)
        self.assertTrue(any("fontspec" in issue["message"] for issue in issues))
        self.assertTrue(any("XeLaTeX" in issue["message"] or "LuaLaTeX" in issue["message"] for issue in issues))

    def test_detect_redundant_inputenc_with_unicode_engines(self):
        """Test detection of redundant inputenc package with Unicode engines."""
        content = """
\\documentclass{article}
\\usepackage{fontspec}
\\usepackage[utf8]{inputenc}
\\begin{document}
Test
\\end{document}
"""
        issues = self.formatter.detect_redundant_packages(content)
        self.assertTrue(any("inputenc" in issue["package"] for issue in issues))
        self.assertTrue(any("redundant" in issue["message"].lower() for issue in issues))

    def test_detect_missing_geometry_package(self):
        """Test detection of missing geometry package when margin commands are used."""
        content = """
\\documentclass{article}
\\usepackage[margin=2cm]{geometry}
\\begin{document}
Test
\\end{document}
"""
        # This should pass - geometry is properly loaded
        issues = self.formatter.detect_missing_packages(content)
        self.assertFalse(any("geometry" in issue["package"] for issue in issues))

        # This should fail - geometry commands used without package
        content_missing = """
\\documentclass{article}
\\geometry{margin=2cm}
\\begin{document}
Test
\\end{document}
"""
        issues = self.formatter.detect_missing_packages(content_missing)
        self.assertTrue(any("geometry" in issue["package"] for issue in issues))


class TestFontDefinitionValidation(unittest.TestCase):
    """Test validation of font family definitions."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_detect_incomplete_font_definitions(self):
        """Test detection of incomplete font family definitions."""
        content = """
\\usepackage{fontspec}
\\newfontfamily\\farsifont[Script=Arabic]{Noto Sans Arabic}
\\newcommand{\\farsibold}[1]{{\\farsifontbold{#1}}}
"""
        issues = self.formatter.validate_font_definitions(content)
        self.assertTrue(any("bold variant" in issue["message"].lower() for issue in issues))

    def test_suggest_font_definition_fixes(self):
        """Test suggestion of fixes for font definition issues."""
        content = """
\\newfontfamily\\farsifont[Script=Arabic]{Noto Sans Arabic}
\\newcommand{\\farsibold}[1]{{\\farsifontbold{#1}}}
"""
        fixes = self.formatter.suggest_font_definition_fixes(content)
        self.assertTrue(any("\\farsifont\\bfseries" in fix["suggestion"] for fix in fixes))


class TestAdvancedErrorRecovery(unittest.TestCase):
    """Test advanced error recovery and automatic fixes."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = AdvancedLaTeXFormatter()

    def test_auto_fix_undefined_farsifontbold(self):
        """Test automatic fixing of undefined \\farsifontbold command."""
        content = """
\\newfontfamily\\farsifont[Script=Arabic]{Noto Sans Arabic}
\\newcommand{\\farsibold}[1]{{\\farsifontbold{#1}}}
"""
        fixed_content = self.formatter.auto_fix_undefined_commands(content)
        self.assertIn("\\farsifont\\bfseries", fixed_content)
        self.assertNotIn("\\farsifontbold", fixed_content)

    def test_auto_remove_redundant_packages(self):
        """Test automatic removal of redundant packages."""
        content = """
\\documentclass{article}
\\usepackage{fontspec}
\\usepackage[utf8]{inputenc}
\\begin{document}
Test
\\end{document}
"""
        fixed_content = self.formatter.auto_fix_redundant_packages(content)
        # Should comment out or remove inputenc when fontspec is present
        self.assertTrue(
            "% \\usepackage[utf8]{inputenc}" in fixed_content or
            "\\usepackage[utf8]{inputenc}" not in fixed_content
        )

    def test_comprehensive_error_detection_and_fixing(self):
        """Test comprehensive error detection and fixing on real-world content."""
        # This is the actual problematic content from the file
        content = """
\\documentclass[12pt,a4paper,twocolumn]{article}
\\usepackage{fontspec}
\\usepackage[utf8]{inputenc}
\\newfontfamily\\farsifont[Script=Arabic]{Noto Sans Arabic}
\\newcommand{\\farsibold}[1]{{\\farsifontbold{#1}}}
\\usepackage[margin=2cm]{geometry}
\\begin{document}
\\farsibold{Test}
\\end{document}
"""
        
        # Detect all issues
        all_issues = self.formatter.comprehensive_error_detection(content)
        
        # Should detect undefined command
        undefined_issues = [i for i in all_issues if i["type"] == "undefined_command"]
        self.assertTrue(len(undefined_issues) > 0)
        
        # Should detect redundant package
        redundant_issues = [i for i in all_issues if i["type"] == "redundant_package"]
        self.assertTrue(len(redundant_issues) > 0)
        
        # Auto-fix all issues
        fixed_content = self.formatter.auto_fix_all_issues(content)
        
        # Verify fixes
        self.assertNotIn("\\farsifontbold", fixed_content)
        self.assertIn("\\farsifont\\bfseries", fixed_content)
        # inputenc should be commented out or removed
        self.assertTrue(
            "% \\usepackage[utf8]{inputenc}" in fixed_content or
            "\\usepackage[utf8]{inputenc}" not in fixed_content
        )


class TestErrorReporting(unittest.TestCase):
    """Test comprehensive error reporting capabilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = AdvancedLaTeXFormatter()

    def test_generate_error_report(self):
        """Test generation of comprehensive error report."""
        content = """
\\documentclass{article}
\\usepackage{fontspec}
\\usepackage[utf8]{inputenc}
\\newcommand{\\farsibold}[1]{{\\farsifontbold{#1}}}
\\begin{document}
\\farsibold{Test}
\\end{document}
"""
        
        report = self.formatter.generate_comprehensive_error_report(content)
        
        # Should have different categories of issues
        self.assertIn("undefined_commands", report)
        self.assertIn("redundant_packages", report)
        self.assertIn("engine_compatibility", report)
        self.assertIn("suggestions", report)
        
        # Should have actionable suggestions
        self.assertTrue(len(report["suggestions"]) > 0)

    def test_error_severity_classification(self):
        """Test classification of errors by severity."""
        content = """
\\newcommand{\\farsibold}[1]{{\\farsifontbold{#1}}}
\\usepackage{fontspec}
\\usepackage[utf8]{inputenc}
"""
        
        classified = self.formatter.classify_errors_by_severity(content)
        
        self.assertIn("critical", classified)
        self.assertIn("warning", classified)
        self.assertIn("info", classified)
        
        # Undefined command should be critical
        critical_issues = classified["critical"]
        self.assertTrue(any("undefined" in issue["type"] for issue in critical_issues))


if __name__ == "__main__":
    unittest.main()