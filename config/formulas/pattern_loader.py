#!/usr/bin/env python3
"""
Pattern Loader for LaTeX Formatter
Loads scientific and mathematical patterns from external configuration files.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class PatternLoader:
    """Loads and manages patterns from external configuration files."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize pattern loader with configuration directory."""
        if config_dir is None:
            # Default to config/formulas directory relative to this file
            self.config_dir = Path(__file__).parent
        else:
            self.config_dir = Path(config_dir)
    
    def load_scientific_patterns(self) -> List[re.Pattern]:
        """Load scientific patterns from configuration file."""
        patterns = []
        config_file = self.config_dir / "scientific_patterns.json"
        
        if not config_file.exists():
            return self._get_default_scientific_patterns()
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Process patterns in order of specificity (most specific first)
            pattern_groups = [
                config.get("chemical_formulas", []),
                config.get("compound_terms", []),
                config.get("reference_patterns", []),
                config.get("numerical_ranges", []),
                config.get("package_options", []),
                config.get("comment_patterns", []),
                config.get("general_patterns", [])
            ]
            
            for group in pattern_groups:
                for pattern_str in group:
                    try:
                        patterns.append(re.compile(pattern_str))
                    except re.error as e:
                        print(f"Warning: Invalid regex pattern '{pattern_str}': {e}")
            
            return patterns
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load scientific patterns: {e}")
            return self._get_default_scientific_patterns()
    
    def load_math_patterns(self) -> Dict[str, List[str]]:
        """Load mathematical patterns from configuration file."""
        config_file = self.config_dir / "math_patterns.json"
        
        if not config_file.exists():
            return self._get_default_math_patterns()
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load math patterns: {e}")
            return self._get_default_math_patterns()
    
    def add_pattern(self, category: str, pattern: str, pattern_file: str = "scientific_patterns.json") -> bool:
        """Add a new pattern to the specified category."""
        config_file = self.config_dir / pattern_file
        
        try:
            # Load existing config
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            # Add pattern to category
            if category not in config:
                config[category] = []
            
            if pattern not in config[category]:
                config[category].append(pattern)
                
                # Save updated config
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
                return True
            
            return False  # Pattern already exists
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error adding pattern: {e}")
            return False
    
    def remove_pattern(self, category: str, pattern: str, pattern_file: str = "scientific_patterns.json") -> bool:
        """Remove a pattern from the specified category."""
        config_file = self.config_dir / pattern_file
        
        try:
            if not config_file.exists():
                return False
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if category in config and pattern in config[category]:
                config[category].remove(pattern)
                
                # Save updated config
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
                return True
            
            return False
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error removing pattern: {e}")
            return False
    
    def list_patterns(self, pattern_file: str = "scientific_patterns.json") -> Dict[str, List[str]]:
        """List all patterns in the specified file."""
        config_file = self.config_dir / pattern_file
        
        try:
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error listing patterns: {e}")
            return {}
    
    def _get_default_scientific_patterns(self) -> List[re.Pattern]:
        """Get default scientific patterns as fallback."""
        default_patterns = [
            r'Li-S',
            r'Li₂S₆',
            r'CoSe₂',
            r'Ti₃C₂Tₓ',
            r'HKUST-1',
            r'PPy@S/GA-VD',
            r'Ni-HAB',
            r'USTB-27-Co',
            r'roll-to-roll',
            r'X-ray',
            r'charge-discharge',
            r'solid-liquid-solid',
            r'two-column',
            r'two-dimensional',
            r'References?\s+\d+-\d+',
            r'pages?\s+\d+-\d+',
            r'equations?\s+\d+-\d+',
            r'\d+\.?\d*-\d+\.?\d*',
            r'\[[^=\]]*=[^=\]]*\]',
            r'%.*?---.*?---.*',
            r'%.*?-{10,}.*',
            r'%.*?-\s*-\s*-.*',
            r'[A-Z][a-z]?[₀-₉]*-[A-Z][a-z]?[₀-₉]*',
            r'[A-Z][A-Za-z]*-[A-Za-z0-9]+'
        ]
        
        patterns = []
        for pattern_str in default_patterns:
            try:
                patterns.append(re.compile(pattern_str))
            except re.error:
                pass  # Skip invalid patterns
        
        return patterns
    
    def _get_default_math_patterns(self) -> Dict[str, List[str]]:
        """Get default mathematical patterns as fallback."""
        return {
            "operators": ["=", "+", "-", "*", "/", "\\pm", "\\mp", "\\times", "\\div"],
            "functions": ["\\sin", "\\cos", "\\tan", "\\log", "\\ln", "\\exp", "\\sqrt", "\\frac"],
            "symbols": ["\\alpha", "\\beta", "\\gamma", "\\delta", "\\epsilon", "\\theta", "\\lambda", "\\mu", "\\pi", "\\sigma", "\\omega"],
            "environments": ["equation", "align", "gather", "multline", "split", "alignat", "eqnarray"]
        }