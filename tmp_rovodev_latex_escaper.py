#!/usr/bin/env python3
"""
LaTeX Special Character Escaper
Similar to Python's escape characters, but for LaTeX special characters.

This module provides functions to automatically escape special characters
in LaTeX documents, making it easier to write technical documentation
with shell commands, code snippets, and special symbols.
"""

import re
from typing import Dict, List, Tuple

class LaTeXEscaper:
    """
    A class to handle LaTeX special character escaping similar to Python's escape sequences.
    """
    
    def __init__(self):
        # LaTeX special characters that need escaping
        self.special_chars = {
            # Basic special characters
            '#': r'\#',
            '$': r'\$', 
            '%': r'\%',
            '&': r'\&',
            '_': r'\_',
            '^': r'\textasciicircum{}',
            '~': r'\textasciitilde{}',
            '\\': r'\textbackslash{}',
            '{': r'\{',
            '}': r'\}',
            
            # Extended special characters
            '<': r'\textless{}',
            '>': r'\textgreater{}',
            '|': r'\textbar{}',
            '"': r'\textquotedbl{}',
            "'": r'\textquotesingle{}',
            '`': r'\textasciigrave{}',
            
            # Mathematical symbols that might cause issues
            '±': r'\textpm{}',
            '×': r'\texttimes{}',
            '÷': r'\textdiv{}',
            '°': r'\textdegree{}',
            
            # Common programming symbols
            '@': r'\textasciiat{}',
            '[': r'\textlbrack{}',
            ']': r'\textrbrack{}',
        }
        
        # Environment-specific escaping rules
        self.env_rules = {
            'verbatim': {},  # No escaping needed in verbatim
            'lstlisting': {
                # Only escape what's absolutely necessary in listings
                '\\': r'\\',
                '{': r'\{',
                '}': r'\}',
            },
            'math': {
                # Math mode has different rules
                '$': '',  # Don't escape $ in math mode
                '_': '_',  # Subscripts are normal in math
                '^': '^',  # Superscripts are normal in math
            },
            'url': {
                # URLs have special handling
                '#': '#',  # Don't escape # in URLs
                '%': '%',  # Don't escape % in URLs
            }
        }
    
    def escape_text(self, text: str, environment: str = 'normal') -> str:
        """
        Escape special characters in text for LaTeX.
        
        Args:
            text: The text to escape
            environment: The LaTeX environment context ('normal', 'verbatim', 'lstlisting', 'math', 'url')
        
        Returns:
            Escaped text safe for LaTeX
        """
        if environment == 'verbatim':
            return text  # No escaping needed in verbatim
        
        # Get the appropriate character mapping
        char_map = self.env_rules.get(environment, self.special_chars)
        
        # Escape characters
        escaped_text = text
        for char, replacement in char_map.items():
            escaped_text = escaped_text.replace(char, replacement)
        
        return escaped_text
    
    def escape_shell_command(self, command: str) -> str:
        """
        Escape a shell command for use in LaTeX.
        
        Args:
            command: Shell command string
            
        Returns:
            LaTeX-safe shell command
        """
        # Special handling for shell commands
        escaped = command
        
        # Escape basic special characters
        for char, replacement in self.special_chars.items():
            escaped = escaped.replace(char, replacement)
        
        return escaped
    
    def escape_code_block(self, code: str, language: str = 'bash') -> str:
        """
        Escape code for use in LaTeX code blocks.
        
        Args:
            code: Code string
            language: Programming language
            
        Returns:
            LaTeX-safe code block
        """
        # Use lstlisting rules for code blocks
        return self.escape_text(code, 'lstlisting')
    
    def escape_url(self, url: str) -> str:
        """
        Escape URL for LaTeX.
        
        Args:
            url: URL string
            
        Returns:
            LaTeX-safe URL
        """
        return self.escape_text(url, 'url')
    
    def create_latex_command(self, command_name: str, content: str, 
                           environment: str = 'normal') -> str:
        """
        Create a LaTeX command with properly escaped content.
        
        Args:
            command_name: LaTeX command name (without backslash)
            content: Content to include in the command
            environment: Environment context for escaping
            
        Returns:
            Complete LaTeX command string
        """
        escaped_content = self.escape_text(content, environment)
        return f"\\{command_name}{{{escaped_content}}}"
    
    def create_environment(self, env_name: str, content: str, 
                          options: str = None) -> str:
        """
        Create a LaTeX environment with properly escaped content.
        
        Args:
            env_name: Environment name
            content: Content for the environment
            options: Optional environment options
            
        Returns:
            Complete LaTeX environment
        """
        escaped_content = self.escape_text(content, env_name)
        
        if options:
            begin_line = f"\\begin{{{env_name}}}{{{options}}}"
        else:
            begin_line = f"\\begin{{{env_name}}}"
        
        return f"{begin_line}\n{escaped_content}\n\\end{{{env_name}}}"


class LaTeXDocumentBuilder:
    """
    A builder class for creating LaTeX documents with automatic escaping.
    """
    
    def __init__(self):
        self.escaper = LaTeXEscaper()
        self.content = []
        self.preamble = []
    
    def add_package(self, package_name: str, options: str = None):
        """Add a package to the preamble."""
        if options:
            self.preamble.append(f"\\usepackage[{options}]{{{package_name}}}")
        else:
            self.preamble.append(f"\\usepackage{{{package_name}}}")
    
    def add_title(self, title: str):
        """Add document title with escaping."""
        escaped_title = self.escaper.escape_text(title)
        self.content.append(f"\\title{{{escaped_title}}}")
    
    def add_section(self, title: str, level: int = 1):
        """Add a section with escaped title."""
        escaped_title = self.escaper.escape_text(title)
        
        section_commands = {
            1: "section",
            2: "subsection", 
            3: "subsubsection",
            4: "paragraph",
            5: "subparagraph"
        }
        
        command = section_commands.get(level, "section")
        self.content.append(f"\\{command}{{{escaped_title}}}")
    
    def add_text(self, text: str):
        """Add regular text with escaping."""
        escaped_text = self.escaper.escape_text(text)
        self.content.append(escaped_text)
    
    def add_shell_command(self, command: str, use_verbatim: bool = True):
        """Add a shell command with proper escaping."""
        if use_verbatim:
            self.content.append(f"\\begin{{verbatim}}\n{command}\n\\end{{verbatim}}")
        else:
            escaped_command = self.escaper.escape_shell_command(command)
            self.content.append(f"\\texttt{{{escaped_command}}}")
    
    def add_code_block(self, code: str, language: str = "bash"):
        """Add a code block with syntax highlighting."""
        # Use verbatim for simplicity, or lstlisting for syntax highlighting
        self.content.append(f"\\begin{{lstlisting}}[language={language}]\n{code}\n\\end{{lstlisting}}")
    
    def add_url(self, url: str, text: str = None):
        """Add a URL with proper escaping."""
        if text:
            escaped_text = self.escaper.escape_text(text)
            self.content.append(f"\\href{{{url}}}{{{escaped_text}}}")
        else:
            self.content.append(f"\\url{{{url}}}")
    
    def build_document(self, document_class: str = "article") -> str:
        """Build the complete LaTeX document."""
        doc_parts = [
            f"\\documentclass{{{document_class}}}",
            "",
            # Add preamble
            *self.preamble,
            "",
            "\\begin{document}",
            "",
            # Add content
            *self.content,
            "",
            "\\end{document}"
        ]
        
        return "\n".join(doc_parts)


# Convenience functions for quick escaping
def escape_latex(text: str, environment: str = 'normal') -> str:
    """Quick function to escape text for LaTeX."""
    escaper = LaTeXEscaper()
    return escaper.escape_text(text, environment)

def escape_shell(command: str) -> str:
    """Quick function to escape shell commands."""
    escaper = LaTeXEscaper()
    return escaper.escape_shell_command(command)

def escape_code(code: str, language: str = 'bash') -> str:
    """Quick function to escape code blocks."""
    escaper = LaTeXEscaper()
    return escaper.escape_code_block(code, language)


# Example usage and testing
if __name__ == "__main__":
    # Test the escaper
    escaper = LaTeXEscaper()
    
    print("=== LaTeX Escaper Test ===")
    
    # Test basic escaping
    test_text = "This has special chars: # $ % & _ ^ ~ \\ { }"
    print(f"Original: {test_text}")
    print(f"Escaped:  {escaper.escape_text(test_text)}")
    print()
    
    # Test shell command escaping
    shell_cmd = 'sudo chsh -s $(which zsh) $(whoami)'
    print(f"Shell command: {shell_cmd}")
    print(f"Escaped:       {escaper.escape_shell_command(shell_cmd)}")
    print()
    
    # Test document builder
    builder = LaTeXDocumentBuilder()
    builder.add_package("fontspec")
    builder.add_package("xcolor")
    builder.add_package("listings")
    builder.add_package("hyperref")
    
    builder.add_title("Oh My Zsh Installation Guide")
    builder.add_section("Introduction")
    builder.add_text("This guide shows how to install Oh My Zsh with special characters: #, $, %, &")
    
    builder.add_section("Shell Commands", 2)
    builder.add_shell_command('sudo chsh -s $(which zsh) $(whoami)')
    
    builder.add_section("Code Example", 2)
    builder.add_code_block('export ZSH="$HOME/.oh-my-zsh"\n# This is a comment\necho "Hello $USER"')
    
    builder.add_url("https://github.com/ohmyzsh/ohmyzsh", "Oh My Zsh GitHub")
    
    document = builder.build_document()
    print("=== Generated LaTeX Document ===")
    print(document)