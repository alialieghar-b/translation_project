#!/usr/bin/env python3
"""
Enhanced CLI for LaTeX Formatter with advanced features
"""

import json
import sys
from pathlib import Path
from typing import Optional, Tuple, Union

import click

from latex_formatter import LaTeXFormatter
from latex_formatter_advanced import (
    AdvancedLaTeXFormatter,
    analyze_latex_project,
    format_files_parallel,
)


@click.group()
@click.version_option(version="1.0.0", prog_name="LaTeX Formatter")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option(
    "--config", "-c", type=click.Path(exists=True), help="Configuration file path"
)
@click.option(
    "--pattern-config", type=click.Path(exists=True), help="Pattern configuration directory path"
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, config: Optional[str], pattern_config: Optional[str]) -> None:
    """LaTeX Formatter - A Black/Ruff-style formatter for LaTeX files."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["config"] = config
    ctx.obj["pattern_config"] = pattern_config


@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True), required=True)
@click.option(
    "--check",
    is_flag=True,
    help="Check if files need formatting without modifying them",
)
@click.option("--diff", is_flag=True, help="Show diff of changes")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be changed without modifying files"
)
@click.option("--parallel", "-p", is_flag=True, help="Process files in parallel")
@click.option("--advanced", "-a", is_flag=True, help="Use advanced formatting features")
@click.option("--line-length", type=int, default=80, help="Maximum line length")
@click.option("--indent-size", type=int, default=2, help="Indentation size")
@click.pass_context
def format(
    ctx: click.Context,
    files: Tuple[str, ...],
    check: bool,
    diff: bool,
    dry_run: bool,
    parallel: bool,
    advanced: bool,
    line_length: int,
    indent_size: int,
) -> None:
    """Format LaTeX files."""
    config = {}

    # Load config file if provided
    if ctx.obj["config"]:
        config = LaTeXFormatter.load_config(ctx.obj["config"])

    # Override with CLI options
    config.update(
        {
            "line_length": line_length,
            "indent_size": indent_size,
        }
    )

    # Choose formatter
    formatter: Union[LaTeXFormatter, AdvancedLaTeXFormatter]
    if advanced:
        formatter = AdvancedLaTeXFormatter(config, pattern_config_dir=ctx.obj.get("pattern_config"))
        click.echo("Using advanced formatter with extended features")
    else:
        # Ensure config has all required keys by merging with default
        if config:
            default_config = LaTeXFormatter().default_config()
            default_config.update(config)
            config = default_config
        formatter = LaTeXFormatter(config, pattern_config_dir=ctx.obj.get("pattern_config"))

    formatter.setup_logging(verbose=ctx.obj["verbose"])

    file_paths = [Path(f) for f in files]

    # Filter LaTeX files
    latex_files = [f for f in file_paths if f.suffix.lower() in [".tex", ".latex"]]
    if len(latex_files) != len(file_paths):
        non_latex = [f for f in file_paths if f not in latex_files]
        click.echo(
            f"Warning: Skipping non-LaTeX files: {', '.join(str(f) for f in non_latex)}"
        )

    if not latex_files:
        click.echo("No LaTeX files to process")
        return

    # Process files
    if parallel and len(latex_files) > 1:
        click.echo(f"Processing {len(latex_files)} files in parallel...")
        if isinstance(formatter, AdvancedLaTeXFormatter):
            results = format_files_parallel(latex_files, formatter)
        else:
            # Fall back to sequential for basic formatter
            results = {}
            for file_path in latex_files:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    formatted = formatter.format_content(content)
                    results[str(file_path)] = formatted
                except Exception:
                    results[str(file_path)] = ""

        changed_files = []
        for file_path_str, result in results.items():
            file_path = Path(file_path_str)
            if result == "":
                click.echo(f"Error processing {file_path}", err=True)
                continue

            # Read original content
            with open(file_path_str, "r", encoding="utf-8") as f:
                original = f.read()

            if original != result:
                changed_files.append(file_path)
                if check or dry_run:
                    click.echo(f"would reformat {file_path}")
                elif diff:
                    import difflib

                    diff_output = difflib.unified_diff(
                        original.splitlines(keepends=True),
                        result.splitlines(keepends=True),
                        fromfile=f"a/{file_path}",
                        tofile=f"b/{file_path}",
                        n=3,
                    )
                    click.echo("".join(diff_output), nl=False)
                else:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(result)
                    click.echo(f"reformatted {file_path}")

        if changed_files and (check or dry_run):
            click.echo(f"\nWould reformat {len(changed_files)} files")
            if check:
                sys.exit(1)
        elif changed_files:
            click.echo(f"\nReformatted {len(changed_files)} files")
        else:
            click.echo("All files already formatted")

    else:
        # Sequential processing (reuse existing logic from main formatter)
        changed_files = []
        error_files = []

        for latex_file in latex_files:
            file_path_str = str(latex_file)
            try:
                with open(latex_file, "r", encoding="utf-8") as f:
                    original_content = f.read()

                formatted_content = formatter.format_content(original_content)

                if original_content != formatted_content:
                    changed_files.append(latex_file)

                    if check or dry_run:
                        click.echo(f"would reformat {file_path_str}")
                    elif diff:
                        import difflib

                        diff_output = difflib.unified_diff(
                            original_content.splitlines(keepends=True),
                            formatted_content.splitlines(keepends=True),
                            fromfile=f"a/{file_path_str}",
                            tofile=f"b/{file_path_str}",
                            n=3,
                        )
                        click.echo("".join(diff_output), nl=False)
                    else:
                        with open(latex_file, "w", encoding="utf-8") as f:
                            f.write(formatted_content)
                        click.echo(f"reformatted {file_path_str}")

                        # Run syntax check
                        issues = formatter.check_syntax(formatted_content)
                        if issues:
                            click.echo(
                                f"Warning: Syntax issues in {file_path_str}:", err=True
                            )
                            for issue in issues:
                                click.echo(f"  {issue}", err=True)
                else:
                    if ctx.obj["verbose"]:
                        click.echo(f"{file_path_str} already formatted")

            except Exception as e:
                click.echo(f"Error processing {file_path_str}: {e}", err=True)
                error_files.append(file_path_str)

        # Summary
        if changed_files:
            if check or dry_run:
                click.echo(f"\nWould reformat {len(changed_files)} files")
                if check:
                    sys.exit(1)
            else:
                click.echo(f"\nReformatted {len(changed_files)} files")
        else:
            click.echo("All files already formatted")

        if error_files:
            click.echo(f"Errors in {len(error_files)} files", err=True)
            sys.exit(1)


@cli.command()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    "--output",
    "-o",
    type=click.File("w"),
    default="-",
    help="Output file (default: stdout)",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "text"]),
    default="text",
    help="Output format",
)
@click.pass_context
def analyze(
    ctx: click.Context, directory: str, output: str, output_format: str
) -> None:
    """Analyze a LaTeX project for formatting issues and suggestions."""
    project_dir = Path(directory)

    # Only show status message for non-JSON output
    if output_format != "json":
        click.echo(f"Analyzing LaTeX project in {project_dir}...")
    analysis = analyze_latex_project(project_dir)

    if output_format == "json":
        # Convert Path objects to strings for JSON serialization
        analysis_json = analysis.copy()
        analysis_json["tex_files"] = [str(f) for f in analysis_json["tex_files"]]
        if hasattr(output, "write"):
            json.dump(analysis_json, output, indent=2)
        else:
            with open(output, "w") as f:
                json.dump(analysis_json, f, indent=2)
    else:
        # Text format
        if hasattr(output, "write"):
            output.write("LaTeX Project Analysis\n")
            output.write("=====================\n\n")
            output.write(f"Total LaTeX files: {analysis['total_files']}\n")
            output.write(
                f"Total lines: {analysis['statistics'].get('total_lines', 0)}\n"
            )
            output.write(
                f"Total characters: "
                f"{analysis['statistics'].get('total_characters', 0)}\n"
            )
            output.write(
                f"Average file size: "
                f"{analysis['statistics'].get('average_file_size', 0):.1f} "
                f"lines\n"
            )

            if analysis["issues"]:
                output.write(f"Issues Found ({len(analysis['issues'])}):\n")
                output.write("-" * 20 + "\n")
                for issue in analysis["issues"]:
                    output.write(f"• {issue}\n")
                output.write("\n")

            if analysis["suggestions"]:
                output.write(f"Suggestions ({len(analysis['suggestions'])}):\n")
                output.write("-" * 20 + "\n")
                for suggestion in analysis["suggestions"]:
                    output.write(f"• {suggestion}\n")
                output.write("\n")

            if not analysis["issues"] and not analysis["suggestions"]:
                output.write("No issues or suggestions found. Great job!\n")
        else:
            # Handle string output path
            with open(output, "w") as f:
                f.write("LaTeX Project Analysis\n")
                f.write("=====================\n\n")
                f.write(f"Total LaTeX files: {analysis['total_files']}\n")
                f.write(
                    f"Total lines: {analysis['statistics'].get('total_lines', 0)}\n"
                )
                f.write(
                    f"Total characters: "
                    f"{analysis['statistics'].get('total_characters', 0)}\n"
                )
                f.write(
                    f"Average file size: "
                    f"{analysis['statistics'].get('average_file_size', 0):.1f} "
                    f"lines\\n\\n"
                )

                if analysis["issues"]:
                    f.write(f"Issues Found ({len(analysis['issues'])}):\n")
                    f.write("-" * 20 + "\n")
                    for issue in analysis["issues"]:
                        f.write(f"• {issue}\n")
                    f.write("\n")

                if analysis["suggestions"]:
                    f.write(f"Suggestions ({len(analysis['suggestions'])}):\n")
                    f.write("-" * 20 + "\n")
                    for suggestion in analysis["suggestions"]:
                        f.write(f"• {suggestion}\n")
                    f.write("\n")

                if not analysis["issues"] and not analysis["suggestions"]:
                    f.write("No issues or suggestions found. Great job!\n")


@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True), required=True)
@click.pass_context
def check_syntax(ctx: click.Context, files: Tuple[str, ...]) -> None:
    """Check LaTeX files for syntax issues."""
    formatter = LaTeXFormatter()
    formatter.setup_logging(verbose=ctx.obj["verbose"])

    total_issues = 0

    for file_path_str in files:
        file_path = Path(file_path_str)

        if file_path.suffix.lower() not in [".tex", ".latex"]:
            click.echo(f"Skipping non-LaTeX file: {file_path}")
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            issues = formatter.check_syntax(content)

            if issues:
                click.echo(f"\n{file_path}:")
                for issue in issues:
                    click.echo(f"  ❌ {issue}")
                total_issues += len(issues)
            else:
                if ctx.obj["verbose"]:
                    click.echo(f"✅ {file_path}: No syntax issues")

        except Exception as e:
            click.echo(f"❌ Error reading {file_path}: {e}", err=True)
            total_issues += 1

    if total_issues > 0:
        click.echo(f"\nFound {total_issues} syntax issues")
        sys.exit(1)
    else:
        click.echo("\n✅ All files passed syntax check")


@cli.command()
@click.option(
    "--output",
    "-o",
    type=click.File("w"),
    default="-",
    help="Output file (default: stdout)",
)
def config_template(output: str) -> None:
    """Generate a configuration template."""
    template = """# LaTeX Formatter Configuration
# Save as pyproject.toml or latex-formatter.json

[tool.latex-formatter]
line_length = 80
indent_size = 2
normalize_whitespace = true
sort_packages = true
align_environments = true
fix_spacing = true
normalize_commands = true
remove_trailing_whitespace = true
ensure_final_newline = true
compress_empty_lines = true
max_empty_lines = 2
align_ampersands = true
normalize_quotes = true
fix_math_spacing = true

# Advanced features
format_bibliography = true
format_citations = true
wrap_long_lines = false
align_comments = false
optimize_whitespace = true
comment_column = 50

# File patterns
include = "*.tex"
exclude = [
    "build/",
    "dist/",
    ".git/",
    "__pycache__/",
    "*.aux",
    "*.log",
    "*.out",
]

# Environment-specific rules
[tool.latex-formatter.environments]
no_indent = ["verbatim", "lstlisting", "minted"]
blank_lines_around = ["section", "subsection", "chapter"]
preserve_formatting = ["verbatim", "lstlisting", "minted"]

# Package grouping
[tool.latex-formatter.packages]
math = ["amsmath", "amssymb", "amsfonts", "mathtools"]
graphics = ["graphicx", "tikz", "pgfplots", "subcaption"]
formatting = ["geometry", "fancyhdr", "setspace", "parskip"]
fonts = ["fontspec", "polyglossia", "babel", "inputenc"]
"""

    if hasattr(output, "write"):
        output.write(template)
        if hasattr(output, "name") and output.name != "<stdout>":
            click.echo(f"Configuration template written to {output.name}")
    else:
        with open(output, "w") as f:
            f.write(template)
        click.echo(f"Configuration template written to {output}")


@cli.group()
@click.pass_context
def patterns(ctx: click.Context) -> None:
    """Manage formula and pattern configurations."""
    pass


@patterns.command()
@click.argument("category", type=str)
@click.argument("pattern", type=str)
@click.option("--file", "-f", default="scientific_patterns.json", help="Pattern file to modify")
@click.pass_context
def add(ctx: click.Context, category: str, pattern: str, file: str) -> None:
    """Add a new pattern to the specified category."""
    try:
        from config.formulas.pattern_loader import PatternLoader
        
        config_dir = ctx.obj.get("pattern_config") or "config/formulas"
        loader = PatternLoader(config_dir)
        
        if loader.add_pattern(category, pattern, file):
            click.echo(f"Added pattern '{pattern}' to category '{category}' in {file}")
        else:
            click.echo(f"Pattern '{pattern}' already exists in category '{category}'")
            
    except Exception as e:
        click.echo(f"Error adding pattern: {e}", err=True)


@patterns.command()
@click.argument("category", type=str)
@click.argument("pattern", type=str)
@click.option("--file", "-f", default="scientific_patterns.json", help="Pattern file to modify")
@click.pass_context
def remove(ctx: click.Context, category: str, pattern: str, file: str) -> None:
    """Remove a pattern from the specified category."""
    try:
        from config.formulas.pattern_loader import PatternLoader
        
        config_dir = ctx.obj.get("pattern_config") or "config/formulas"
        loader = PatternLoader(config_dir)
        
        if loader.remove_pattern(category, pattern, file):
            click.echo(f"Removed pattern '{pattern}' from category '{category}' in {file}")
        else:
            click.echo(f"Pattern '{pattern}' not found in category '{category}'")
            
    except Exception as e:
        click.echo(f"Error removing pattern: {e}", err=True)


@patterns.command()
@click.option("--file", "-f", default="scientific_patterns.json", help="Pattern file to list")
@click.pass_context
def list(ctx: click.Context, file: str) -> None:
    """List all patterns in the specified file."""
    try:
        from config.formulas.pattern_loader import PatternLoader
        
        config_dir = ctx.obj.get("pattern_config") or "config/formulas"
        loader = PatternLoader(config_dir)
        
        patterns = loader.list_patterns(file)
        
        if patterns:
            click.echo(f"Patterns in {file}:")
            for category, pattern_list in patterns.items():
                click.echo(f"\n{category}:")
                for pattern in pattern_list:
                    click.echo(f"  - {pattern}")
        else:
            click.echo(f"No patterns found in {file}")
            
    except Exception as e:
        click.echo(f"Error listing patterns: {e}", err=True)


@patterns.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize pattern configuration directory with default files."""
    try:
        import os
        import json
        
        config_dir = ctx.obj.get("pattern_config") or "config/formulas"
        os.makedirs(config_dir, exist_ok=True)
        
        # Create default scientific patterns
        scientific_patterns = {
            "chemical_formulas": ["Li-S", "Li₂S₆", "CoSe₂", "Ti₃C₂Tₓ", "HKUST-1"],
            "compound_terms": ["roll-to-roll", "X-ray", "charge-discharge", "two-dimensional"],
            "reference_patterns": ["References?\\s+\\d+-\\d+", "pages?\\s+\\d+-\\d+"],
            "numerical_ranges": ["\\d+\\.?\\d*-\\d+\\.?\\d*"],
            "package_options": ["\\[[^=\\]]*=[^=\\]]*\\]"],
            "comment_patterns": ["%.*?---.*?---.*", "%.*?-{10,}.*"],
            "general_patterns": ["[A-Z][a-z]?[₀-₉]*-[A-Z][a-z]?[₀-₉]*"]
        }
        
        # Create default math patterns
        math_patterns = {
            "operators": ["=", "+", "-", "*", "/", "\\pm", "\\mp"],
            "functions": ["\\sin", "\\cos", "\\tan", "\\log", "\\ln", "\\sqrt", "\\frac"],
            "symbols": ["\\alpha", "\\beta", "\\gamma", "\\delta", "\\pi", "\\sigma"],
            "environments": ["equation", "align", "gather", "multline", "split"]
        }
        
        # Write files
        with open(os.path.join(config_dir, "scientific_patterns.json"), "w") as f:
            json.dump(scientific_patterns, f, indent=2, ensure_ascii=False)
            
        with open(os.path.join(config_dir, "math_patterns.json"), "w") as f:
            json.dump(math_patterns, f, indent=2, ensure_ascii=False)
            
        click.echo(f"Initialized pattern configuration in {config_dir}")
        
    except Exception as e:
        click.echo(f"Error initializing patterns: {e}", err=True)


if __name__ == "__main__":
    cli()
