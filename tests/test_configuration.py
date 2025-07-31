#!/usr/bin/env python3
"""
Configuration handling tests for LaTeX Formatter
Tests configuration loading, validation, merging, and error handling
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from latex_formatter import LaTeXFormatter
from latex_formatter_advanced import AdvancedLaTeXFormatter


class TestConfigurationLoading(unittest.TestCase):
    """Test configuration file loading from various sources."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_default_configuration(self):
        """Test default configuration values."""
        formatter = LaTeXFormatter()
        config = formatter.config

        # Check required keys exist
        required_keys = [
            "line_length",
            "indent_size",
            "normalize_whitespace",
            "sort_packages",
            "align_environments",
            "fix_spacing",
            "normalize_commands",
            "remove_trailing_whitespace",
            "ensure_final_newline",
            "compress_empty_lines",
            "max_empty_lines",
            "align_ampersands",
            "normalize_quotes",
            "fix_math_spacing",
        ]

        for key in required_keys:
            self.assertIn(key, config, f"Missing required config key: {key}")

        # Check default values
        self.assertEqual(config["line_length"], 80)
        self.assertEqual(config["indent_size"], 2)
        self.assertEqual(config["max_empty_lines"], 2)
        self.assertTrue(config["sort_packages"])
        self.assertTrue(config["normalize_quotes"])
        self.assertTrue(config["align_environments"])

    def test_load_json_configuration(self):
        """Test loading JSON configuration file."""
        config_file = Path(self.test_dir) / "config.json"
        config_data = {
            "line_length": 100,
            "indent_size": 4,
            "sort_packages": False,
            "normalize_quotes": True,
            "max_empty_lines": 3,
            "custom_option": "custom_value",
        }

        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

        config = LaTeXFormatter.load_config(str(config_file))

        # Check loaded values override defaults
        self.assertEqual(config["line_length"], 100)
        self.assertEqual(config["indent_size"], 4)
        self.assertEqual(config["sort_packages"], False)
        self.assertEqual(config["normalize_quotes"], True)
        self.assertEqual(config["max_empty_lines"], 3)
        self.assertEqual(config["custom_option"], "custom_value")

        # Check defaults are preserved for unspecified values
        self.assertTrue(config["align_environments"])  # Default value
        self.assertTrue(config["fix_spacing"])  # Default value

    def test_load_toml_configuration(self):
        """Test loading TOML configuration file."""
        try:
            import toml

            config_file = Path(self.test_dir) / "pyproject.toml"
            config_content = """[build-system]
requires = ["setuptools", "wheel"]

[tool.latex-formatter]
line_length = 120
indent_size = 3
sort_packages = true
normalize_quotes = false
align_ampersands = true
custom_setting = "test_value"

[tool.latex-formatter.environments]
no_indent = ["verbatim", "lstlisting", "minted"]
blank_lines_around = ["section", "subsection", "chapter"]

[tool.other-tool]
setting = "ignored"
"""

            with open(config_file, "w") as f:
                f.write(config_content)

            config = LaTeXFormatter.load_config(str(config_file))

            # Check that tool.latex-formatter section is loaded
            self.assertEqual(config["line_length"], 120)
            self.assertEqual(config["indent_size"], 3)
            self.assertTrue(config["sort_packages"])
            self.assertFalse(config["normalize_quotes"])
            self.assertTrue(config["align_ampersands"])
            self.assertEqual(config["custom_setting"], "test_value")

            # Check that nested configuration is loaded
            self.assertIn("environments", config)
            self.assertIn("no_indent", config["environments"])
            self.assertEqual(
                config["environments"]["no_indent"],
                ["verbatim", "lstlisting", "minted"],
            )

            # Check that other tool sections are ignored
            self.assertNotIn("setting", config)

        except ImportError:
            self.skipTest("TOML library not available")

    def test_load_toml_without_tool_section(self):
        """Test loading TOML without tool.latex-formatter section."""
        try:
            import toml

            config_file = Path(self.test_dir) / "config.toml"
            config_content = """line_length = 90
indent_size = 2
sort_packages = false
"""

            with open(config_file, "w") as f:
                f.write(config_content)

            config = LaTeXFormatter.load_config(str(config_file))

            # Should load direct TOML format
            self.assertEqual(config["line_length"], 90)
            self.assertEqual(config["indent_size"], 2)
            self.assertFalse(config["sort_packages"])

        except ImportError:
            self.skipTest("TOML library not available")

    def test_load_configuration_file_priority(self):
        """Test configuration file loading priority and fallback."""
        # Test with non-existent file
        config = LaTeXFormatter.load_config("/nonexistent/config.json")
        self.assertEqual(config["line_length"], 80)  # Should use defaults

        # Test with existing file
        config_file = Path(self.test_dir) / "existing.json"
        with open(config_file, "w") as f:
            json.dump({"line_length": 150}, f)

        config = LaTeXFormatter.load_config(str(config_file))
        self.assertEqual(config["line_length"], 150)

    def test_load_configuration_with_none_path(self):
        """Test loading configuration with None path."""
        config = LaTeXFormatter.load_config(None)

        # Should return default configuration
        self.assertEqual(config["line_length"], 80)
        self.assertEqual(config["indent_size"], 2)
        self.assertTrue(config["sort_packages"])


class TestConfigurationValidation(unittest.TestCase):
    """Test configuration parameter validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_invalid_json_syntax(self):
        """Test handling of invalid JSON syntax."""
        config_file = Path(self.test_dir) / "invalid.json"

        # Write invalid JSON
        with open(config_file, "w") as f:
            f.write('{ "line_length": 80, "invalid": }')

        # Should not raise exception, should fall back to defaults
        config = LaTeXFormatter.load_config(str(config_file))

        self.assertEqual(config["line_length"], 80)  # Default value
        self.assertEqual(config["indent_size"], 2)  # Default value

    def test_empty_configuration_file(self):
        """Test handling of empty configuration file."""
        config_file = Path(self.test_dir) / "empty.json"

        with open(config_file, "w") as f:
            f.write("{}")

        config = LaTeXFormatter.load_config(str(config_file))

        # Should use all default values
        self.assertEqual(config["line_length"], 80)
        self.assertEqual(config["indent_size"], 2)
        self.assertTrue(config["sort_packages"])

    def test_invalid_parameter_types(self):
        """Test handling of invalid parameter types."""
        config_data = {
            "line_length": "not_a_number",  # Should be int
            "indent_size": -5,  # Should be positive
            "sort_packages": "yes",  # Should be boolean
            "max_empty_lines": 0.5,  # Should be int
        }

        # Create formatter with invalid config
        formatter = LaTeXFormatter(config_data)

        # Should handle gracefully and use provided values
        # (validation could be added in future versions)
        self.assertEqual(formatter.config["line_length"], "not_a_number")
        self.assertEqual(formatter.config["indent_size"], -5)
        self.assertEqual(formatter.config["sort_packages"], "yes")
        self.assertEqual(formatter.config["max_empty_lines"], 0.5)

    def test_partial_configuration_override(self):
        """Test partial configuration override behavior."""
        base_config = LaTeXFormatter().default_config()

        partial_config = {"line_length": 120, "normalize_quotes": False}

        # Merge configurations
        merged_config = base_config.copy()
        merged_config.update(partial_config)

        formatter = LaTeXFormatter(merged_config)

        # Check overridden values
        self.assertEqual(formatter.config["line_length"], 120)
        self.assertFalse(formatter.config["normalize_quotes"])

        # Check preserved defaults
        self.assertEqual(formatter.config["indent_size"], 2)
        self.assertTrue(formatter.config["sort_packages"])

    def test_unknown_configuration_keys(self):
        """Test handling of unknown configuration keys."""
        config_data = {
            "line_length": 100,
            "unknown_option": "value",
            "another_unknown": 42,
            "nested_unknown": {"key": "value"},
        }

        formatter = LaTeXFormatter(config_data)

        # Known options should work
        self.assertEqual(formatter.config["line_length"], 100)

        # Unknown options should be preserved (for extensibility)
        self.assertEqual(formatter.config["unknown_option"], "value")
        self.assertEqual(formatter.config["another_unknown"], 42)
        self.assertEqual(formatter.config["nested_unknown"], {"key": "value"})


class TestConfigurationMerging(unittest.TestCase):
    """Test configuration merging from multiple sources."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_file_config_plus_runtime_override(self):
        """Test merging file configuration with runtime overrides."""
        # Create base configuration file
        config_file = Path(self.test_dir) / "base.json"
        file_config = {
            "line_length": 90,
            "indent_size": 3,
            "sort_packages": True,
            "normalize_quotes": True,
        }

        with open(config_file, "w") as f:
            json.dump(file_config, f)

        # Load base config
        config = LaTeXFormatter.load_config(str(config_file))

        # Apply runtime overrides
        runtime_overrides = {
            "line_length": 110,  # Override file setting
            "normalize_quotes": False,  # Override file setting
            "new_option": "added",  # Add new option
        }

        config.update(runtime_overrides)
        formatter = LaTeXFormatter(config)

        # Check that runtime overrides take precedence
        self.assertEqual(formatter.config["line_length"], 110)
        self.assertFalse(formatter.config["normalize_quotes"])
        self.assertEqual(formatter.config["new_option"], "added")

        # Check that non-overridden file settings are preserved
        self.assertEqual(formatter.config["indent_size"], 3)
        self.assertTrue(formatter.config["sort_packages"])

    def test_multiple_configuration_sources(self):
        """Test merging from multiple configuration sources."""
        # Base defaults
        base_config = LaTeXFormatter().default_config()

        # File configuration
        file_config = {"line_length": 100, "sort_packages": False}

        # Environment-like configuration
        env_config = {"indent_size": 4, "line_length": 120}  # Override file setting

        # CLI-like configuration
        cli_config = {
            "normalize_quotes": False,
            "line_length": 80,  # Override everything else
        }

        # Merge in order: base -> file -> env -> CLI
        final_config = base_config.copy()
        final_config.update(file_config)
        final_config.update(env_config)
        final_config.update(cli_config)

        formatter = LaTeXFormatter(final_config)

        # Check final precedence
        self.assertEqual(formatter.config["line_length"], 80)  # CLI wins
        self.assertEqual(formatter.config["indent_size"], 4)  # From env
        self.assertFalse(formatter.config["sort_packages"])  # From file
        self.assertFalse(formatter.config["normalize_quotes"])  # From CLI

        # Check base defaults are preserved
        self.assertTrue(formatter.config["align_environments"])  # Base default

    def test_nested_configuration_merging(self):
        """Test merging of nested configuration structures."""
        base_config = {
            "line_length": 80,
            "environments": {
                "no_indent": ["verbatim"],
                "preserve_formatting": ["lstlisting"],
            },
            "packages": {"math": ["amsmath", "amsfonts"]},
        }

        override_config = {
            "line_length": 100,
            "environments": {
                "no_indent": ["verbatim", "minted"],  # Extend list
                "blank_lines_around": ["section"],  # Add new key
            },
            "packages": {"graphics": ["graphicx", "tikz"]},  # Add new category
        }

        # Manual deep merge (LaTeX formatter might do shallow merge)
        merged_config = base_config.copy()
        merged_config.update(override_config)

        # For nested dicts, Python's update does shallow merge
        self.assertEqual(merged_config["line_length"], 100)
        self.assertEqual(
            merged_config["environments"]["no_indent"], ["verbatim", "minted"]
        )
        self.assertIn("blank_lines_around", merged_config["environments"])

        # Note: shallow merge means original nested keys may be lost
        # This tests the current behavior, not necessarily ideal behavior


class TestConfigurationErrorHandling(unittest.TestCase):
    """Test error handling in configuration loading."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_permission_denied_config_file(self):
        """Test handling of config file with permission denied."""
        config_file = Path(self.test_dir) / "restricted.json"

        # Create config file
        with open(config_file, "w") as f:
            json.dump({"line_length": 100}, f)

        # Mock permission error
        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            config = LaTeXFormatter.load_config(str(config_file))

            # Should fall back to defaults without crashing
            self.assertEqual(config["line_length"], 80)  # Default value

    def test_corrupted_config_file(self):
        """Test handling of corrupted configuration file."""
        config_file = Path(self.test_dir) / "corrupted.json"

        # Write corrupted JSON (truncated file)
        with open(config_file, "w") as f:
            f.write('{"line_length": 100, "indent_')  # Truncated

        config = LaTeXFormatter.load_config(str(config_file))

        # Should handle gracefully and use defaults
        self.assertEqual(config["line_length"], 80)  # Default
        self.assertEqual(config["indent_size"], 2)  # Default

    def test_binary_file_as_config(self):
        """Test handling of binary file passed as config."""
        binary_file = Path(self.test_dir) / "binary.json"

        # Write binary content
        with open(binary_file, "wb") as f:
            f.write(b"\x00\x01\x02\x03\xff\xfe\xfd")

        # Should handle gracefully
        config = LaTeXFormatter.load_config(str(binary_file))

        self.assertEqual(config["line_length"], 80)  # Default

    def test_directory_as_config_file(self):
        """Test handling of directory path passed as config file."""
        config_dir = Path(self.test_dir) / "config_dir"
        config_dir.mkdir()

        # Should handle gracefully
        config = LaTeXFormatter.load_config(str(config_dir))

        self.assertEqual(config["line_length"], 80)  # Default

    @patch("latex_formatter.logging")
    def test_config_loading_warnings(self, mock_logging):
        """Test that configuration loading issues generate appropriate warnings."""
        config_file = Path(self.test_dir) / "invalid.json"

        with open(config_file, "w") as f:
            f.write("invalid json content")

        LaTeXFormatter.load_config(str(config_file))

        # Should have logged a warning
        mock_logging.warning.assert_called()


class TestAdvancedConfigurationFeatures(unittest.TestCase):
    """Test advanced configuration features."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_advanced_formatter_specific_config(self):
        """Test configuration specific to advanced formatter."""
        config_data = {
            "line_length": 100,
            "format_bibliography": True,
            "format_citations": True,
            "wrap_long_lines": True,
            "align_comments": True,
            "optimize_whitespace": True,
            "comment_column": 60,
        }

        advanced_formatter = AdvancedLaTeXFormatter(config_data)

        # Check that advanced-specific configs are available
        self.assertEqual(advanced_formatter.config["comment_column"], 60)
        self.assertTrue(advanced_formatter.config["format_bibliography"])
        self.assertTrue(advanced_formatter.config["wrap_long_lines"])

        # Check that basic configs still work
        self.assertEqual(advanced_formatter.config["line_length"], 100)

    def test_environment_specific_configuration(self):
        """Test environment-specific configuration."""
        config_data = {
            "environments": {
                "no_indent": ["verbatim", "lstlisting", "minted"],
                "blank_lines_around": ["section", "subsection", "chapter"],
                "preserve_formatting": ["verbatim", "lstlisting"],
            }
        }

        formatter = AdvancedLaTeXFormatter(config_data)

        # Check environment configuration
        env_config = formatter.config.get("environments", {})
        self.assertEqual(env_config["no_indent"], ["verbatim", "lstlisting", "minted"])
        self.assertEqual(
            env_config["blank_lines_around"], ["section", "subsection", "chapter"]
        )

    def test_package_grouping_configuration(self):
        """Test package grouping configuration."""
        config_data = {
            "packages": {
                "math": ["amsmath", "amssymb", "amsfonts"],
                "graphics": ["graphicx", "tikz", "pgfplots"],
                "formatting": ["geometry", "fancyhdr", "setspace"],
                "references": ["hyperref", "cleveref", "natbib"],
            }
        }

        formatter = LaTeXFormatter(config_data)

        # Check package configuration
        pkg_config = formatter.config.get("packages", {})
        self.assertEqual(pkg_config["math"], ["amsmath", "amssymb", "amsfonts"])
        self.assertEqual(pkg_config["graphics"], ["graphicx", "tikz", "pgfplots"])

    def test_configuration_inheritance(self):
        """Test configuration inheritance from base to advanced formatter."""
        base_config = {"line_length": 90, "indent_size": 3, "sort_packages": False}

        # Create base formatter
        base_formatter = LaTeXFormatter(base_config)

        # Create advanced formatter with same config
        advanced_formatter = AdvancedLaTeXFormatter(base_config)

        # Both should have same base configuration
        self.assertEqual(base_formatter.config["line_length"], 90)
        self.assertEqual(advanced_formatter.config["line_length"], 90)
        self.assertEqual(base_formatter.config["indent_size"], 3)
        self.assertEqual(advanced_formatter.config["indent_size"], 3)

        # Advanced formatter should have additional capabilities
        self.assertIsInstance(advanced_formatter, AdvancedLaTeXFormatter)
        self.assertIsInstance(base_formatter, LaTeXFormatter)


class TestConfigurationInRealScenarios(unittest.TestCase):
    """Test configuration handling in realistic usage scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_project_specific_config(self):
        """Test project-specific configuration workflow."""
        # Create project directory structure
        project_dir = Path(self.test_dir) / "latex_project"
        project_dir.mkdir()

        # Create project-specific configuration
        config_file = project_dir / "latex-formatter.json"
        project_config = {
            "line_length": 120,
            "indent_size": 4,
            "sort_packages": True,
            "normalize_quotes": False,  # Project doesn't want quote normalization
            "align_ampersands": True,
            "max_empty_lines": 1,
        }

        with open(config_file, "w") as f:
            json.dump(project_config, f, indent=2)

        # Create test LaTeX file
        tex_file = project_dir / "main.tex"
        tex_content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
This has "quotes" that should not be normalized.


\\begin{tabular}{cc}
Name&Age
John&25
\\end{tabular}
\\end{document}"""

        with open(tex_file, "w") as f:
            f.write(tex_content)

        # Load project config and format
        config = LaTeXFormatter.load_config(str(config_file))
        formatter = LaTeXFormatter(config)
        result = formatter.format_file(tex_file)

        # Check that project config was applied
        self.assertIn('"quotes"', result)  # Quotes NOT normalized
        self.assertNotIn("\n\n\n", result)  # Max 1 empty line

        # Check table alignment
        self.assertIn("Name & Age", result)
        self.assertIn("John & 25", result)

        # Check package sorting
        amsmath_pos = result.find("\\usepackage{amsmath}")
        tikz_pos = result.find("\\usepackage{tikz}")
        self.assertLess(amsmath_pos, tikz_pos)

    def test_user_global_config(self):
        """Test user global configuration scenario."""
        # Simulate user's global config file
        global_config_file = Path(self.test_dir) / "global_config.json"
        global_config = {
            "line_length": 88,  # User prefers Black's line length
            "indent_size": 2,
            "normalize_quotes": True,
            "sort_packages": True,
            "align_ampersands": True,
            "ensure_final_newline": True,
        }

        with open(global_config_file, "w") as f:
            json.dump(global_config, f, indent=2)

        # Load global config
        config = LaTeXFormatter.load_config(str(global_config_file))

        # User wants to override some settings for specific task
        task_overrides = {
            "line_length": 60,  # Narrow format for slides
            "normalize_quotes": False,  # Preserve original quotes
        }

        config.update(task_overrides)
        formatter = LaTeXFormatter(config)

        # Test that overrides work
        self.assertEqual(formatter.config["line_length"], 60)
        self.assertFalse(formatter.config["normalize_quotes"])

        # Test that global settings are preserved
        self.assertEqual(formatter.config["indent_size"], 2)
        self.assertTrue(formatter.config["sort_packages"])
        self.assertTrue(formatter.config["align_ampersands"])

    def test_team_shared_config(self):
        """Test team shared configuration scenario."""
        # Create team configuration
        team_config_file = Path(self.test_dir) / "team_config.json"
        team_config = {
            "line_length": 100,
            "indent_size": 2,
            "sort_packages": True,
            "normalize_quotes": True,
            "align_ampersands": True,
            "max_empty_lines": 2,
            "ensure_final_newline": True,
            "compress_empty_lines": True,
            # Team-specific preferences
            "custom_team_setting": "value",
            "project_standards": {
                "citation_style": "natbib",
                "reference_format": "author-year",
            },
        }

        with open(team_config_file, "w") as f:
            json.dump(team_config, f, indent=2)

        # Multiple team members should get consistent results
        formatter1 = LaTeXFormatter(LaTeXFormatter.load_config(str(team_config_file)))
        formatter2 = LaTeXFormatter(LaTeXFormatter.load_config(str(team_config_file)))

        # Same configuration
        self.assertEqual(
            formatter1.config["line_length"], formatter2.config["line_length"]
        )
        self.assertEqual(
            formatter1.config["indent_size"], formatter2.config["indent_size"]
        )

        # Custom team settings preserved
        self.assertEqual(formatter1.config["custom_team_setting"], "value")
        self.assertEqual(
            formatter1.config["project_standards"]["citation_style"], "natbib"
        )

        # Test consistent formatting
        test_content = """\\documentclass{article}
\\begin{document}
\\section{Test}
This is"quoted"text.
\\end{document}"""

        result1 = formatter1.format_content(test_content)
        result2 = formatter2.format_content(test_content)

        # Should produce identical results
        self.assertEqual(result1, result2)


if __name__ == "__main__":
    unittest.main()
