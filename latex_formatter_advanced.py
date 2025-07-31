#!/usr/bin/env python3
"""
Advanced LaTeX Formatter - Extended features for production use
"""

import concurrent.futures
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Match, Optional

from latex_formatter import LaTeXFormatter


class AdvancedLaTeXFormatter(LaTeXFormatter):
    """Extended LaTeX formatter with advanced features."""

    def __init__(self, config: Optional[Dict] = None):
        # Ensure we have all required config keys
        if config is None:
            config = self.default_config()
        else:
            # Merge with default config to ensure all keys are present
            default_config = self.default_config()
            default_config.update(config)
            config = default_config
        super().__init__(config)
        self.bibliography_styles = {
            "natbib": ["\\cite", "\\citep", "\\citet", "\\citeauthor"],
            "biblatex": ["\\autocite", "\\textcite", "\\parencite", "\\footcite"],
            "basic": ["\\cite", "\\ref", "\\pageref"],
        }

    def format_content(self, content: str) -> str:
        """Enhanced formatting pipeline with advanced features."""
        self.logger.debug("Starting advanced formatting pipeline")

        # Basic formatting first
        content = super().format_content(content)

        # Advanced formatting
        content = self.format_bibliography(content)
        content = self.format_citations(content)
        content = self.wrap_long_lines(content)
        content = self.align_comments(content)
        content = self.format_custom_environments(content)
        content = self.optimize_whitespace(content)

        self.logger.debug("Advanced formatting pipeline completed")
        return content

    def format_bibliography(self, content: str) -> str:
        """Format bibliography entries consistently."""
        if not self.config.get("format_bibliography", True):
            return content

        # Find bibliography environment
        bib_pattern = r"(\\begin\{thebibliography\}.*?\\end\{thebibliography\})"

        def format_bib_block(match: Match[str]) -> str:
            bib_content = match.group(1)
            lines = bib_content.split("\n")
            formatted_lines = []

            for line in lines:
                stripped = line.strip()
                if stripped.startswith("\\bibitem"):
                    # Format bibitem entries
                    formatted_lines.append(f"  {stripped}")
                elif stripped.startswith("\\begin") or stripped.startswith("\\end"):
                    formatted_lines.append(stripped)
                elif stripped.startswith("%"):
                    # Preserve comment formatting but don't indent
                    formatted_lines.append(stripped)
                elif stripped:
                    # Indent bibliography content
                    formatted_lines.append(f"    {stripped}")
                else:
                    formatted_lines.append(line)

            return "\n".join(formatted_lines)

        return re.sub(bib_pattern, format_bib_block, content, flags=re.DOTALL)

    def format_citations(self, content: str) -> str:
        """Format citation commands consistently."""
        if not self.config.get("format_citations", True):
            return content

        # Normalize citation spacing
        for style_commands in self.bibliography_styles.values():
            for cmd in style_commands:
                # Fix spacing around citations
                pattern = rf"({re.escape(cmd)})\s*\{{"
                content = re.sub(pattern, r"\1{", content)

                # Fix spacing inside citation braces and normalize comma-separated refs
                pattern = rf"({re.escape(cmd)})\{{\s*([^}}]+)\s*\}}"

                def fix_citation_content(match: Match[str]) -> str:
                    cmd_part = match.group(1)
                    refs_part = match.group(2)
                    # Clean up spaces around commas and normalize reference list
                    refs_clean = re.sub(r"\s*,\s*", ",", refs_part.strip())
                    return f"{cmd_part}{{{refs_clean}}}"

                content = re.sub(pattern, fix_citation_content, content)

        return content

    def wrap_long_lines(self, content: str) -> str:
        """Wrap long lines while preserving LaTeX structure."""
        if not self.config.get("wrap_long_lines", False):
            return content

        max_length = self.config.get("line_length", 80)
        lines = content.split("\n")
        wrapped_lines = []

        for line in lines:
            if len(line) <= max_length:
                wrapped_lines.append(line)
                continue

            # Don't wrap certain lines
            if (
                line.strip().startswith("%")
                or line.strip().startswith("\\")
                or "\\begin{" in line
                or "\\end{" in line
            ):
                wrapped_lines.append(line)
                continue

            # Wrap at word boundaries
            words = line.split()
            current_line = ""
            indent = len(line) - len(line.lstrip())

            for word in words:
                if len(current_line + " " + word) <= max_length:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = " " * indent + word.lstrip()
                else:
                    if current_line:
                        wrapped_lines.append(current_line)
                    current_line = " " * indent + word.lstrip()

            if current_line:
                wrapped_lines.append(current_line)

        return "\n".join(wrapped_lines)

    def align_comments(self, content: str) -> str:
        """Align inline comments consistently."""
        if not self.config.get("align_comments", False):
            return content

        lines = content.split("\n")
        aligned_lines = []
        comment_column = self.config.get("comment_column", 50)

        for line in lines:
            if "%" in line and not line.strip().startswith("%"):
                # Find inline comment
                comment_pos = line.find("%")
                code_part = line[:comment_pos].rstrip()
                comment_part = line[comment_pos:].strip()

                if len(code_part) < comment_column:
                    # Align comment to column
                    spaces_needed = comment_column - len(code_part)
                    aligned_line = code_part + " " * spaces_needed + comment_part
                else:
                    # Comment too close, add minimal spacing
                    aligned_line = code_part + "  " + comment_part

                aligned_lines.append(aligned_line)
            else:
                aligned_lines.append(line)

        return "\n".join(aligned_lines)

    def format_custom_environments(self, content: str) -> str:
        """Format custom environments based on configuration."""
        env_config = self.config.get("environments", {})

        # Handle no-indent environments
        no_indent_envs = env_config.get("no_indent", [])
        for env in no_indent_envs:
            pattern = rf"(\\begin\{{{env}\}}.*?\\end\{{{env}\}})"

            def preserve_formatting(match: Match[str]) -> str:
                return match.group(1)  # Return as-is

            content = re.sub(pattern, preserve_formatting, content, flags=re.DOTALL)

        # Handle blank lines around environments
        blank_line_envs = env_config.get("blank_lines_around", [])
        for env in blank_line_envs:
            # This feature is not fully implemented yet
            # Just return content as-is for now
            pass

        return content

    def optimize_whitespace(self, content: str) -> str:
        """Advanced whitespace optimization."""
        if not self.config.get("optimize_whitespace", True):
            return content

        # Fix spacing around math delimiters
        # Remove spaces inside math delimiters while preserving
        # spaces between text and math
        content = re.sub(r"\$ ([^$]+?) \$", r"$\1$", content)

        # Remove spaces before punctuation (but not between words and math)
        content = re.sub(r"\s+([,.;!?])", r"\1", content)

        # Fix spacing in math environments
        content = re.sub(
            r"(\\begin\{(?:equation|align|gather)\})\s+", r"\1\n  ", content
        )
        content = re.sub(r"\s+(\\end\{(?:equation|align|gather)\})", r"\n\1", content)

        return content

    def detect_language_and_encoding(self, content: str) -> Dict[str, Optional[str]]:
        """Detect document language and encoding."""
        info: Dict[str, Optional[str]] = {"language": "english", "encoding": "utf8"}

        # Detect language packages
        if re.search(r"\\usepackage.*\{babel\}", content):
            babel_match = re.search(r"\\usepackage\[([^\]]+)\]\{babel\}", content)
            if babel_match:
                info["language"] = babel_match.group(1)

        if re.search(r"\\usepackage.*\{polyglossia\}", content):
            info["language"] = "multilingual"

        # Detect encoding
        encoding_match = re.search(r"\\usepackage\[([^\]]+)\]\{inputenc\}", content)
        if encoding_match:
            info["encoding"] = encoding_match.group(1)

        return info

    def suggest_improvements(self, content: str) -> List[str]:
        """Suggest improvements for LaTeX document."""
        suggestions = []

        # Check for common issues
        if "\\usepackage{graphicx}" not in content and "\\includegraphics" in content:
            suggestions.append(
                "Consider adding \\usepackage{graphicx} for image support"
            )

        if "\\usepackage{hyperref}" not in content and (
            "\\ref{" in content or "\\cite{" in content
        ):
            suggestions.append(
                "Consider adding \\usepackage{hyperref} for clickable references"
            )

        if "\\usepackage{booktabs}" not in content and "\\begin{tabular}" in content:
            suggestions.append(
                "Consider using \\usepackage{booktabs} for better table formatting"
            )

        # Check for outdated commands
        if "\\bf" in content:
            suggestions.append("Replace \\bf with \\textbf{} or \\bfseries")

        if "\\it" in content:
            suggestions.append("Replace \\it with \\textit{} or \\itshape")

        # Check for missing packages based on commands
        commands_packages = {
            "\\url{": "url",
            "\\href{": "hyperref",
            "\\includegraphics": "graphicx",
            "\\toprule": "booktabs",
            "\\midrule": "booktabs",
            "\\bottomrule": "booktabs",
        }

        for cmd, pkg in commands_packages.items():
            if cmd in content and f"\\usepackage{{{pkg}}}" not in content:
                suggestions.append(
                    f"Consider adding \\usepackage{{{pkg}}} for {cmd} support"
                )

        return suggestions


def format_files_parallel(
    file_paths: List[Path],
    formatter: AdvancedLaTeXFormatter,
    max_workers: Optional[int] = None,
) -> Dict[str, str]:
    """Format multiple files in parallel."""
    results: Dict[str, str] = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all formatting tasks
        future_to_file = {
            executor.submit(formatter.format_file, file_path): file_path
            for file_path in file_paths
        }

        # Collect results
        for future in concurrent.futures.as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                result = future.result()
                results[str(file_path)] = result or ""
            except Exception as exc:
                logging.error(f"File {file_path} generated an exception: {exc}")
                results[str(file_path)] = ""

    return results


def analyze_latex_project(project_dir: Path) -> Dict[str, Any]:
    """Analyze a LaTeX project for formatting recommendations."""
    analysis: Dict = {
        "total_files": 0,
        "tex_files": [],
        "issues": [],
        "suggestions": [],
        "statistics": {},
    }

    # Find all LaTeX files
    for pattern in ["*.tex", "*.latex"]:
        tex_files = list(project_dir.rglob(pattern))
        analysis["tex_files"].extend(tex_files)

    analysis["total_files"] = len(analysis["tex_files"])

    if analysis["total_files"] == 0:
        analysis["issues"].append("No LaTeX files found in project")
        return analysis

    formatter = AdvancedLaTeXFormatter()

    # Analyze each file
    total_lines = 0
    total_chars = 0

    for tex_file in analysis["tex_files"]:
        try:
            with open(tex_file, "r", encoding="utf-8") as f:
                content = f.read()

            lines = len(content.split("\n"))
            chars = len(content)
            total_lines += lines
            total_chars += chars

            # Check for syntax issues
            issues = formatter.check_syntax(content)
            if issues:
                analysis["issues"].extend(
                    [f"{tex_file.name}: {issue}" for issue in issues]
                )

            # Get suggestions
            suggestions = formatter.suggest_improvements(content)
            if suggestions:
                analysis["suggestions"].extend(
                    [f"{tex_file.name}: {sugg}" for sugg in suggestions]
                )

        except Exception as e:
            analysis["issues"].append(f"Could not analyze {tex_file.name}: {e}")

    analysis["statistics"] = {
        "total_lines": total_lines,
        "total_characters": total_chars,
        "average_file_size": (
            total_lines / analysis["total_files"] if analysis["total_files"] > 0 else 0
        ),
    }

    return analysis


if __name__ == "__main__":
    # Example usage
    formatter = AdvancedLaTeXFormatter(
        {
            "format_bibliography": True,
            "format_citations": True,
            "wrap_long_lines": True,
            "align_comments": True,
            "optimize_whitespace": True,
            "line_length": 80,
            "comment_column": 50,
        }
    )

    # Test with sample content
    sample_content = """
\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
This is a very long line that should be wrapped because it exceeds the maximum
line length specified in the configuration.
\\cite{reference1,reference2}  % This is a comment
\\begin{equation}
x + y = z
\\end{equation}
\\end{document}
"""

    result = formatter.format_content(sample_content)
    print("Formatted content:")
    print(result)

    suggestions = formatter.suggest_improvements(sample_content)
    if suggestions:
        print("\nSuggestions:")
        for suggestion in suggestions:
            print(f"- {suggestion}")
