# LaTeX Formatter Configuration

This directory contains external configuration files for the LaTeX Formatter, allowing you to customize formula patterns and mathematical expressions without modifying the source code.

## Directory Structure

```
config/
├── formulas/
│   ├── scientific_patterns.json    # Scientific and chemical formulas
│   ├── math_patterns.json          # Mathematical symbols and operators
│   ├── pattern_loader.py           # Pattern loading utilities
│   └── __init__.py                 # Package initialization
└── README.md                       # This file
```

## Configuration Files

### scientific_patterns.json

Contains patterns for protecting scientific content during formatting:

- **chemical_formulas**: Chemical compounds (e.g., Li-S, CoSe₂, Ti₃C₂Tₓ)
- **compound_terms**: Hyphenated scientific terms (e.g., roll-to-roll, X-ray)
- **reference_patterns**: Reference ranges (e.g., "References 1-10")
- **numerical_ranges**: Number ranges (e.g., "1.5-2.0")
- **package_options**: LaTeX package options with equals signs
- **comment_patterns**: Comment line patterns with dashes
- **general_patterns**: General chemical/material name patterns

### math_patterns.json

Contains mathematical symbols and operators:

- **operators**: Mathematical operators (=, +, -, *, /, ∓, ±)
- **functions**: Mathematical functions (\sin, \cos, \log, \sqrt, \frac)
- **symbols**: Greek letters and symbols (\alpha, \beta, \pi, \sigma)
- **environments**: Math environments (equation, align, gather)

## Usage

### Command Line Interface

Initialize pattern configuration:
```bash
python cli.py patterns init
```

List all patterns:
```bash
python cli.py patterns list
python cli.py patterns list --file math_patterns.json
```

Add a new pattern:
```bash
python cli.py patterns add chemical_formulas "NiCo₂O₄"
python cli.py patterns add compound_terms "state-of-the-art"
```

Remove a pattern:
```bash
python cli.py patterns remove chemical_formulas "old-formula"
```

### Using Custom Pattern Directory

Specify a custom pattern configuration directory:
```bash
python cli.py --pattern-config /path/to/custom/config format file.tex
```

### Programmatic Usage

```python
from latex_formatter import LaTeXFormatter

# Use default config directory
formatter = LaTeXFormatter()

# Use custom config directory
formatter = LaTeXFormatter(pattern_config_dir="/path/to/config")

# Load patterns manually
from config.formulas.pattern_loader import PatternLoader
loader = PatternLoader("/path/to/config")
patterns = loader.load_scientific_patterns()
```

## Pattern Categories

### Chemical Formulas
Protect chemical compound names and formulas from being reformatted:
- Simple compounds: Li-S, NaCl
- Complex compounds: Li₂S₆, CoSe₂, Ti₃C₂Tₓ
- Named compounds: HKUST-1, PPy@S/GA-VD

### Compound Terms
Protect hyphenated scientific and technical terms:
- Process terms: roll-to-roll, charge-discharge
- Measurement terms: X-ray, two-dimensional
- Technical terms: solid-liquid-solid, state-of-the-art

### Reference Patterns
Protect reference ranges and citations:
- Page ranges: "pages 1-10", "pp. 15-20"
- Reference ranges: "References 1-5"
- Equation ranges: "equations 2.1-2.5"

## Best Practices

1. **Order Matters**: Patterns are applied in order of specificity (most specific first)
2. **Regex Syntax**: Use proper regex escaping for special characters
3. **Testing**: Test new patterns with sample documents before deployment
4. **Backup**: Keep backups of working configurations
5. **Documentation**: Document custom patterns for team collaboration

## Examples

### Adding Chemical Formulas
```bash
# Add a new battery material
python cli.py patterns add chemical_formulas "LiFePO₄"

# Add a catalyst compound
python cli.py patterns add chemical_formulas "Pt/C"
```

### Adding Technical Terms
```bash
# Add manufacturing process
python cli.py patterns add compound_terms "layer-by-layer"

# Add measurement technique
python cli.py patterns add compound_terms "in-situ"
```

### Custom Regex Patterns
```bash
# Add pattern for DOI references
python cli.py patterns add reference_patterns "doi:\\d+\\.\\d+/[\\w\\.-]+"

# Add pattern for temperature ranges
python cli.py patterns add numerical_ranges "\\d+°C-\\d+°C"
```

## Troubleshooting

### Pattern Not Working
1. Check regex syntax with online regex tester
2. Verify pattern is in correct category
3. Ensure pattern order (specific before general)
4. Test with simple examples first

### Performance Issues
1. Avoid overly complex regex patterns
2. Use specific patterns instead of broad ones
3. Monitor pattern compilation warnings
4. Consider pattern optimization

### Configuration Errors
1. Validate JSON syntax
2. Check file permissions
3. Verify directory structure
4. Review error logs for details