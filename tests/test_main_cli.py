#!/usr/bin/env python3
"""
Tests for the main CLI function in latex_formatter.py
"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from latex_formatter import main


class TestMainCLI(unittest.TestCase):
    """Test the main CLI function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.tex"
        self.test_file.write_text(
            """\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
This is"bad quotes"text.
\\end{document}"""
        )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_main_basic_formatting(self):
        """Test basic file formatting through main()."""
        with patch("sys.argv", ["latex-formatter", str(self.test_file)]):
            with patch("builtins.print"):
                main()

    def test_main_check_mode(self):
        """Test main() with --check flag."""
        with patch("sys.argv", ["latex-formatter", "--check", str(self.test_file)]):
            with patch("builtins.print"):
                with patch("sys.exit") as mock_exit:
                    main()
                    mock_exit.assert_called_with(1)  # Should exit with 1 for changes

    def test_main_dry_run_mode(self):
        """Test main() with --dry-run flag."""
        with patch("sys.argv", ["latex-formatter", "--dry-run", str(self.test_file)]):
            with patch("builtins.print"):
                main()

    def test_main_diff_mode(self):
        """Test main() with --diff flag."""
        with patch("sys.argv", ["latex-formatter", "--diff", str(self.test_file)]):
            with patch("builtins.print"):
                main()

    def test_main_verbose_mode(self):
        """Test main() with --verbose flag."""
        # First format the file so it's already formatted
        with patch("sys.argv", ["latex-formatter", str(self.test_file)]):
            main()

        # Now run with verbose on already formatted file
        with patch("sys.argv", ["latex-formatter", "--verbose", str(self.test_file)]):
            with patch("builtins.print"):
                main()

    def test_main_nonexistent_file(self):
        """Test main() with non-existent file."""
        nonexistent = str(Path(self.temp_dir) / "nonexistent.tex")
        with patch("sys.argv", ["latex-formatter", nonexistent]):
            with patch("builtins.print"):
                with patch("sys.exit") as mock_exit:
                    main()
                    mock_exit.assert_called_with(1)  # Should exit with error

    def test_main_non_latex_file(self):
        """Test main() with non-LaTeX file."""
        txt_file = Path(self.temp_dir) / "test.txt"
        txt_file.write_text("This is not LaTeX")

        with patch("sys.argv", ["latex-formatter", str(txt_file)]):
            with patch("builtins.print"):
                main()

    def test_main_with_config_file(self):
        """Test main() with config file."""
        config_file = Path(self.temp_dir) / "config.json"
        config_file.write_text('{"line_length": 100, "indent_size": 4}')

        with patch(
            "sys.argv",
            ["latex-formatter", "--config", str(config_file), str(self.test_file)],
        ):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called()

    def test_main_with_log_file(self):
        """Test main() with log file."""
        log_file = Path(self.temp_dir) / "test.log"

        with patch(
            "sys.argv",
            ["latex-formatter", "--logfile", str(log_file), str(self.test_file)],
        ):
            main()
            self.assertTrue(log_file.exists())

    def test_main_with_custom_options(self):
        """Test main() with custom line length and indent size."""
        with patch(
            "sys.argv",
            [
                "latex-formatter",
                "--line-length",
                "100",
                "--indent-size",
                "4",
                str(self.test_file),
            ],
        ):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called()

    def test_main_file_processing_error(self):
        """Test main() when file processing raises an exception."""
        # Create a file that will cause an error during processing
        with patch("sys.argv", ["latex-formatter", str(self.test_file)]):
            with patch(
                "latex_formatter.LaTeXFormatter.format_content",
                side_effect=Exception("Test error"),
            ):
                with patch("builtins.print"):
                    with patch("sys.exit") as mock_exit:
                        main()
                        mock_exit.assert_called_with(1)

    def test_main_syntax_check_with_issues(self):
        """Test main() when syntax check finds issues."""
        # Create content that will have syntax issues
        bad_content = (
            "\\begin{document}\\n\\begin{itemize}\\nTest\\n" "\\end{document}"
        )  # Missing \\end{itemize}
        self.test_file.write_text(bad_content)

        with patch("sys.argv", ["latex-formatter", str(self.test_file)]):
            with patch("builtins.print"):
                main()

    def test_main_multiple_files(self):
        """Test main() with multiple files."""
        file2 = Path(self.temp_dir) / "test2.tex"
        file2.write_text(
            "\\documentclass{article}\n\\begin{document}\nTest2\n\\end{document}"
        )

        with patch("sys.argv", ["latex-formatter", str(self.test_file), str(file2)]):
            with patch("builtins.print"):
                main()

    def test_main_no_changes_needed(self):
        """Test main() when no files need formatting."""
        # First format the file
        with patch("sys.argv", ["latex-formatter", str(self.test_file)]):
            main()

        # Run again - should report no changes needed
        with patch("sys.argv", ["latex-formatter", str(self.test_file)]):
            with patch("builtins.print"):
                main()

    def test_main_version_flag(self):
        """Test main() with --version flag."""
        with patch("sys.argv", ["latex-formatter", "--version"]):
            with self.assertRaises(SystemExit):
                main()


class TestMainCLIErrorCases(unittest.TestCase):
    """Test error cases in main CLI function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_main_file_read_error(self):
        """Test main() when file cannot be read."""
        test_file = Path(self.temp_dir) / "unreadable.tex"
        test_file.write_text("\\documentclass{article}")
        test_file.chmod(0o000)  # Make unreadable

        try:
            with patch("sys.argv", ["latex-formatter", str(test_file)]):
                with patch("builtins.print"):
                    with patch("sys.exit") as mock_exit:
                        main()
                        mock_exit.assert_called_with(1)
        finally:
            test_file.chmod(0o644)  # Restore for cleanup

    def test_main_file_write_error(self):
        """Test main() when file cannot be written."""
        test_file = Path(self.temp_dir) / "readonly.tex"
        test_file.write_text(
            "\\documentclass{article}\n\\begin{document}\nTest\n\\end{document}"
        )

        # Mock open to raise PermissionError on write
        original_open = open

        def mock_open_func(*args, **kwargs):
            if len(args) > 1 and "w" in args[1]:
                raise PermissionError("Permission denied")
            return original_open(*args, **kwargs)

        with patch("sys.argv", ["latex-formatter", str(test_file)]):
            with patch("builtins.open", side_effect=mock_open_func):
                with patch("builtins.print"):
                    with patch("sys.exit") as mock_exit:
                        main()
                        mock_exit.assert_called_with(1)

    def test_main_mixed_success_and_error_files(self):
        """Test main() with mix of successful and error files."""
        good_file = Path(self.temp_dir) / "good.tex"
        good_file.write_text(
            "\\documentclass{article}\n\\begin{document}\nTest\n\\end{document}"
        )

        bad_file = Path(self.temp_dir) / "nonexistent.tex"

        with patch("sys.argv", ["latex-formatter", str(good_file), str(bad_file)]):
            with patch("builtins.print"):
                with patch("sys.exit") as mock_exit:
                    main()
                    mock_exit.assert_called_with(
                        1
                    )  # Should exit with error due to bad file


if __name__ == "__main__":
    unittest.main()
