# LaTeX Book Templates

This folder contains two comprehensive LaTeX templates for creating professional books in Persian and English.

## Files Included

1. **`persian_book_template.tex`** - Complete template for Persian books
2. **`english_book_template.tex`** - Complete template for English books
3. **`README_Templates.md`** - This documentation file

## Persian Template Features

### Requirements
- **Compiler**: XeLaTeX or LuaLaTeX (NOT pdfLaTeX)
- **Packages**: xepersian, bidi, fontspec
- **Fonts**: Vazir (recommended), B Nazanin, IRLotus, or XB Niloofar

### Key Features
- ✅ Right-to-left (RTL) text support
- ✅ Persian fonts with proper scaling
- ✅ Persian numbering and date formatting
- ✅ Translated section names (فهرست مطالب, منابع, etc.)
- ✅ Proper Persian typography
- ✅ Support for mixed Persian/English text
- ✅ Professional book layout

### Compilation
```bash
xelatex persian_book_template.tex
xelatex persian_book_template.tex  # Run twice for references
```

## English Template Features

### Requirements
- **Compiler**: pdfLaTeX, XeLaTeX, or LuaLaTeX
- **Packages**: Standard LaTeX packages included

### Key Features
- ✅ Professional typography with microtype
- ✅ Flexible font options (Times, Palatino, Charter, etc.)
- ✅ Proper spacing and formatting
- ✅ Complete book structure
- ✅ Cross-referencing system
- ✅ Bibliography support
- ✅ Multiple table styles

### Compilation
```bash
pdflatex english_book_template.tex
pdflatex english_book_template.tex  # Run twice for references
```

## How to Use These Templates

### For Translation Projects

1. **Start with the appropriate template**
   - Use `persian_book_template.tex` for Persian output
   - Use `english_book_template.tex` for English output

2. **Customize the front matter**
   - Update title, author, translator information
   - Modify copyright page
   - Add dedication if needed

3. **Replace content**
   - Replace chapter titles and content
   - Add your translated text
   - Include images, tables, and figures as needed

4. **Compile and review**
   - Use the correct compiler for each template
   - Check formatting and make adjustments

### Template Structure

Both templates include:

```
Front Matter:
├── Title Page
├── Copyright Page
├── Dedication (optional)
├── Preface
├── Table of Contents
├── List of Figures (optional)
└── List of Tables (optional)

Main Matter:
├── Chapter 1
├── Chapter 2
└── ... (add more chapters)

Back Matter:
├── Bibliography
├── Appendices (optional)
└── Index (optional)
```

## Customization Options

### Persian Template
- **Fonts**: Change `\settextfont{Vazir}` to your preferred Persian font
- **Layout**: Modify geometry settings for different page sizes
- **Colors**: Adjust hyperlink colors in hyperref setup

### English Template
- **Fonts**: Uncomment font packages (times, palatino, charter)
- **Spacing**: Change from `\onehalfspacing` to `\doublespacing` if needed
- **Style**: Modify chapter and section formatting

## Common Issues and Solutions

### Persian Template Issues

**Problem**: Font not found
```
Solution: Install Persian fonts or change to available font:
\settextfont{B Nazanin}  % or another installed font
```

**Problem**: Compilation errors with pdfLaTeX
```
Solution: Use XeLaTeX or LuaLaTeX instead:
xelatex persian_book_template.tex
```

**Problem**: English text appears incorrectly
```
Solution: Wrap English text with \lr{} command:
\lr{English text here}
```

### English Template Issues

**Problem**: References showing as ??
```
Solution: Compile twice:
pdflatex english_book_template.tex
pdflatex english_book_template.tex
```

**Problem**: Images not displaying
```
Solution: Ensure image files are in the same directory and uncomment:
\includegraphics[width=0.8\textwidth]{your_image.png}
```

## Tips for AI Translation Workflow

1. **Extract text from PDF** using tools like:
   - Adobe Acrobat
   - Online PDF converters
   - Python scripts (PyPDF2, pdfplumber)

2. **Translate in chunks** with AI tools:
   - Give AI Studio/ChatGPT manageable sections
   - Maintain context between sections
   - Review and edit translations

3. **Use these templates** to format the final output:
   - Copy translated text into appropriate chapters
   - Maintain original structure and formatting
   - Add cross-references and citations

4. **Quality control**:
   - Proofread translations
   - Check formatting consistency
   - Verify all references work correctly

## Advanced Features

### Both Templates Include
- Automatic chapter/section numbering
- Cross-referencing system
- Professional table formatting
- Figure and table captions
- Bibliography support
- Hyperlinked table of contents
- Print-ready formatting

### Persian-Specific Features
- Proper Persian punctuation handling
- Persian quote marks: `\persianquote{متن}`
- Mixed language support
- Persian mathematical notation

### English-Specific Features
- Microtype for better typography
- Multiple citation styles
- Advanced table formatting with booktabs
- Code listing support
- Professional quotation handling

## Getting Help

If you encounter issues:
1. Check the LaTeX log file for specific errors
2. Ensure you're using the correct compiler
3. Verify all required packages are installed
4. Test with a minimal example first

For Persian-specific issues, ensure your system has proper Persian font support and you're using XeLaTeX or LuaLaTeX.