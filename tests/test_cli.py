#!/usr/bin/env python3
"""
Unit tests for LaTeX Formatter CLI interface
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from cli import cli


class TestCLIFormatCommand(unittest.TestCase):
    """Test CLI format command functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.test_dir = tempfile.mkdtemp()

        # Create test LaTeX file
        self.test_file = Path(self.test_dir) / "test.tex"
        with open(self.test_file, "w") as f:
            f.write(
                """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
This is"bad quotes"text.
\\end{document}"""
            )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir)

    def test_format_basic(self):
        """Test basic format command."""
        result = self.runner.invoke(cli, ["format", str(self.test_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("reformatted", result.output)

        # Check that file was actually formatted
        with open(self.test_file, "r") as f:
            content = f.read()

        self.assertIn("``bad quotes''", content)
        # amsmath should come before tikz (alphabetical)
        amsmath_pos = content.find("\\usepackage{amsmath}")
        tikz_pos = content.find("\\usepackage{tikz}")
        self.assertLess(amsmath_pos, tikz_pos)

    def test_format_check_mode(self):
        """Test format command in check mode."""
        result = self.runner.invoke(cli, ["format", "--check", str(self.test_file)])

        self.assertEqual(result.exit_code, 1)  # Should exit with 1 when changes needed
        self.assertIn("would reformat", result.output)

        # File should not be modified
        with open(self.test_file, "r") as f:
            content = f.read()
        self.assertIn('"bad quotes"', content)  # Original quotes should remain

    def test_format_dry_run_mode(self):
        """Test format command in dry-run mode."""
        result = self.runner.invoke(cli, ["format", "--dry-run", str(self.test_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("would reformat", result.output)

        # File should not be modified
        with open(self.test_file, "r") as f:
            content = f.read()
        self.assertIn('"bad quotes"', content)

    def test_format_diff_mode(self):
        """Test format command in diff mode."""
        result = self.runner.invoke(cli, ["format", "--diff", str(self.test_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("---", result.output)  # Diff header
        self.assertIn("+++", result.output)  # Diff header
        self.assertIn("-", result.output)  # Removed lines
        self.assertIn("+", result.output)  # Added lines

    def test_format_with_config(self):
        """Test format command with configuration file."""
        # Create config file
        config_file = Path(self.test_dir) / "config.json"
        config_data = {"line_length": 120, "indent_size": 4, "sort_packages": False}

        with open(config_file, "w") as f:
            json.dump(config_data, f)

        result = self.runner.invoke(
            cli, ["--config", str(config_file), "format", str(self.test_file)]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("reformatted", result.output)

    def test_format_advanced_mode(self):
        """Test format command with advanced formatter."""
        result = self.runner.invoke(cli, ["format", "--advanced", str(self.test_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Using advanced formatter", result.output)
        self.assertIn("reformatted", result.output)

    def test_format_parallel_mode(self):
        """Test format command with parallel processing."""
        # Create additional test files
        test_files = [str(self.test_file)]
        for i in range(2):
            additional_file = Path(self.test_dir) / f"test{i}.tex"
            with open(additional_file, "w") as f:
                f.write(
                    f"\\documentclass{{article}}\n\\section{{Test {i}}}\n\\end{{document}}"
                )
            test_files.append(str(additional_file))

        result = self.runner.invoke(cli, ["format", "--parallel"] + test_files)

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Processing", result.output)
        self.assertIn("files in parallel", result.output)

    def test_format_custom_options(self):
        """Test format command with custom line length and indent size."""
        result = self.runner.invoke(
            cli,
            [
                "format",
                "--line-length",
                "100",
                "--indent-size",
                "4",
                str(self.test_file),
            ],
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("reformatted", result.output)

    def test_format_nonexistent_file(self):
        """Test format command with non-existent file."""
        nonexistent = Path(self.test_dir) / "nonexistent.tex"

        result = self.runner.invoke(cli, ["format", str(nonexistent)])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("does not exist", result.output)

    def test_format_non_latex_file(self):
        """Test format command with non-LaTeX file."""
        txt_file = Path(self.test_dir) / "test.txt"
        with open(txt_file, "w") as f:
            f.write("This is not a LaTeX file")

        result = self.runner.invoke(cli, ["format", str(txt_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Skipping non-LaTeX files", result.output)

    def test_format_already_formatted_file(self):
        """Test format command with already formatted file."""
        # First format the file
        self.runner.invoke(cli, ["format", str(self.test_file)])

        # Then format again
        result = self.runner.invoke(cli, ["--verbose", "format", str(self.test_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("already formatted", result.output)

    def test_format_with_syntax_issues(self):
        """Test format command with file containing syntax issues."""
        # Create file with syntax issues
        bad_file = Path(self.test_dir) / "bad.tex"
        with open(bad_file, "w") as f:
            f.write("\\section{Missing brace\n\\begin{document}\nContent")

        result = self.runner.invoke(cli, ["format", str(bad_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Syntax issues", result.output)


class TestCLIAnalyzeCommand(unittest.TestCase):
    """Test CLI analyze command functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.test_dir = tempfile.mkdtemp()

        # Create test LaTeX project
        main_tex = Path(self.test_dir) / "main.tex"
        with open(main_tex, "w") as f:
            f.write(
                """\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
\\section{Introduction}
\\includegraphics{image.png}
\\end{document}"""
            )

        chapter_tex = Path(self.test_dir) / "chapter1.tex"
        with open(chapter_tex, "w") as f:
            f.write("\\chapter{First Chapter}\nContent here.")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir)

    def test_analyze_basic(self):
        """Test basic analyze command."""
        result = self.runner.invoke(cli, ["analyze", str(self.test_dir)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("LaTeX Project Analysis", result.output)
        self.assertIn("Total LaTeX files: 2", result.output)
        self.assertIn("Total lines:", result.output)
        self.assertIn("Total characters:", result.output)

    def test_analyze_json_output(self):
        """Test analyze command with JSON output."""
        result = self.runner.invoke(
            cli, ["analyze", "--format", "json", str(self.test_dir)]
        )

        self.assertEqual(result.exit_code, 0)

        # Should be valid JSON
        try:
            data = json.loads(result.output)
            self.assertIn("total_files", data)
            self.assertIn("tex_files", data)
            self.assertIn("statistics", data)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    def test_analyze_output_to_file(self):
        """Test analyze command with file output."""
        output_file = Path(self.test_dir) / "analysis.txt"

        result = self.runner.invoke(
            cli, ["analyze", "--output", str(output_file), str(self.test_dir)]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(output_file.exists())

        with open(output_file, "r") as f:
            content = f.read()

        self.assertIn("LaTeX Project Analysis", content)
        self.assertIn("Total LaTeX files", content)

    def test_analyze_with_suggestions(self):
        """Test analyze command that generates suggestions."""
        result = self.runner.invoke(cli, ["analyze", str(self.test_dir)])

        self.assertEqual(result.exit_code, 0)
        # Should suggest graphicx package for includegraphics
        self.assertIn("Suggestions", result.output)
        self.assertIn("graphicx", result.output)

    def test_analyze_empty_directory(self):
        """Test analyze command on directory with no LaTeX files."""
        empty_dir = Path(self.test_dir) / "empty"
        empty_dir.mkdir()

        result = self.runner.invoke(cli, ["analyze", str(empty_dir)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Total LaTeX files: 0", result.output)

    def test_analyze_nonexistent_directory(self):
        """Test analyze command with non-existent directory."""
        nonexistent = Path(self.test_dir) / "nonexistent"

        result = self.runner.invoke(cli, ["analyze", str(nonexistent)])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("does not exist", result.output)


class TestCLICheckSyntaxCommand(unittest.TestCase):
    """Test CLI check-syntax command functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir)

    def test_check_syntax_valid_file(self):
        """Test syntax checking with valid LaTeX file."""
        valid_file = Path(self.test_dir) / "valid.tex"
        with open(valid_file, "w") as f:
            f.write(
                """\\documentclass{article}
\\begin{document}
\\section{Test}
Content here.
\\end{document}"""
            )

        result = self.runner.invoke(cli, ["check-syntax", str(valid_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("All files passed syntax check", result.output)

    def test_check_syntax_invalid_file(self):
        """Test syntax checking with invalid LaTeX file."""
        invalid_file = Path(self.test_dir) / "invalid.tex"
        with open(invalid_file, "w") as f:
            f.write("\\section{Missing brace\n\\begin{document}\nNo end document")

        result = self.runner.invoke(cli, ["check-syntax", str(invalid_file)])

        self.assertEqual(result.exit_code, 1)
        self.assertIn("syntax issues", result.output)
        self.assertIn("❌", result.output)

    def test_check_syntax_multiple_files(self):
        """Test syntax checking with multiple files."""
        valid_file = Path(self.test_dir) / "valid.tex"
        with open(valid_file, "w") as f:
            f.write("\\documentclass{article}\n\\begin{document}\n\\end{document}")

        invalid_file = Path(self.test_dir) / "invalid.tex"
        with open(invalid_file, "w") as f:
            f.write("\\section{Missing brace")

        result = self.runner.invoke(
            cli, ["check-syntax", str(valid_file), str(invalid_file)]
        )

        self.assertEqual(result.exit_code, 1)
        self.assertIn("Found", result.output)
        self.assertIn("syntax issues", result.output)

    def test_check_syntax_verbose(self):
        """Test syntax checking with verbose output."""
        valid_file = Path(self.test_dir) / "valid.tex"
        with open(valid_file, "w") as f:
            f.write("\\documentclass{article}\n\\begin{document}\n\\end{document}")

        result = self.runner.invoke(cli, ["--verbose", "check-syntax", str(valid_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("✅", result.output)
        self.assertIn("No syntax issues", result.output)

    def test_check_syntax_non_latex_file(self):
        """Test syntax checking with non-LaTeX file."""
        txt_file = Path(self.test_dir) / "test.txt"
        with open(txt_file, "w") as f:
            f.write("This is not LaTeX")

        result = self.runner.invoke(cli, ["check-syntax", str(txt_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Skipping non-LaTeX file", result.output)

    def test_check_syntax_unreadable_file(self):
        """Test syntax checking with unreadable file."""
        # Create file and make it unreadable
        test_file = Path(self.test_dir) / "test.tex"
        with open(test_file, "w") as f:
            f.write("content")

        # Mock file reading to raise exception
        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            result = self.runner.invoke(cli, ["check-syntax", str(test_file)])

            self.assertEqual(result.exit_code, 1)
            self.assertIn("Error reading", result.output)


class TestCLIConfigTemplateCommand(unittest.TestCase):
    """Test CLI config-template command functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir)

    def test_config_template_stdout(self):
        """Test config template output to stdout."""
        result = self.runner.invoke(cli, ["config-template"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("[tool.latex-formatter]", result.output)
        self.assertIn("line_length = 80", result.output)
        self.assertIn("indent_size = 2", result.output)
        self.assertIn('no_indent = ["verbatim"', result.output)

    def test_config_template_to_file(self):
        """Test config template output to file."""
        output_file = Path(self.test_dir) / "config.toml"

        result = self.runner.invoke(
            cli, ["config-template", "--output", str(output_file)]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configuration template written", result.output)
        self.assertTrue(output_file.exists())

        with open(output_file, "r") as f:
            content = f.read()

        self.assertIn("[tool.latex-formatter]", content)
        self.assertIn("line_length = 80", content)


class TestCLIGlobalOptions(unittest.TestCase):
    """Test CLI global options functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.test_dir = tempfile.mkdtemp()

        # Create test file
        self.test_file = Path(self.test_dir) / "test.tex"
        with open(self.test_file, "w") as f:
            f.write(
                "\\documentclass{article}\n\\begin{document}\nContent\n\\end{document}"
            )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir)

    def test_version_option(self):
        """Test version option."""
        result = self.runner.invoke(cli, ["--version"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("LaTeX Formatter", result.output)
        self.assertIn("1.0.0", result.output)

    def test_verbose_option(self):
        """Test verbose option."""
        result = self.runner.invoke(cli, ["--verbose", "format", str(self.test_file)])

        self.assertEqual(result.exit_code, 0)
        # Verbose mode should show more detailed output
        # The exact output depends on logging configuration

    def test_config_option_with_valid_file(self):
        """Test config option with valid configuration file."""
        config_file = Path(self.test_dir) / "config.json"
        config_data = {"line_length": 120}

        with open(config_file, "w") as f:
            json.dump(config_data, f)

        result = self.runner.invoke(
            cli, ["--config", str(config_file), "format", str(self.test_file)]
        )

        self.assertEqual(result.exit_code, 0)

    def test_config_option_with_invalid_file(self):
        """Test config option with invalid configuration file."""
        config_file = Path(self.test_dir) / "invalid_config.json"
        with open(config_file, "w") as f:
            f.write("invalid json content")

        result = self.runner.invoke(
            cli, ["--config", str(config_file), "format", str(self.test_file)]
        )

        # Should still work with default config
        self.assertEqual(result.exit_code, 0)

    def test_help_option(self):
        """Test help option."""
        result = self.runner.invoke(cli, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("LaTeX Formatter", result.output)
        self.assertIn("format", result.output)
        self.assertIn("analyze", result.output)
        self.assertIn("check-syntax", result.output)
        self.assertIn("config-template", result.output)


class TestCLIErrorHandling(unittest.TestCase):
    """Test CLI error handling scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir)

    def test_format_no_files(self):
        """Test format command with no files specified."""
        result = self.runner.invoke(cli, ["format"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing argument", result.output)

    def test_analyze_no_directory(self):
        """Test analyze command with no directory specified."""
        result = self.runner.invoke(cli, ["analyze"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing argument", result.output)

    def test_check_syntax_no_files(self):
        """Test check-syntax command with no files specified."""
        result = self.runner.invoke(cli, ["check-syntax"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing argument", result.output)

    def test_invalid_command(self):
        """Test invalid command."""
        result = self.runner.invoke(cli, ["invalid-command"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("No such command", result.output)

    def test_invalid_option(self):
        """Test invalid option."""
        result = self.runner.invoke(cli, ["format", "--invalid-option", "file.tex"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("No such option", result.output)


if __name__ == "__main__":
    unittest.main()
