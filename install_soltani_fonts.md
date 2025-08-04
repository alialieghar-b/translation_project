# Installing Soltani Persian Fonts Collection

## Download the Collection

### Method 1: Git Clone
```bash
git clone https://github.com/soltaneghar-b/AllFontsSoltani.git
cd AllFontsSoltani
```

### Method 2: Direct Download
1. Visit: https://github.com/soltaneghar-b/AllFontsSoltani
2. Click "Code" → "Download ZIP"
3. Extract the downloaded file

## Installation Instructions

### Windows
1. Navigate to the downloaded folder
2. Select all `.ttf` font files
3. Right-click → "Install" or "Install for all users"
4. Restart your LaTeX editor

### macOS
1. Open the downloaded folder
2. Select all `.ttf` files
3. Double-click to open Font Book
4. Click "Install Font" for each
5. Restart your LaTeX editor

### Linux (Ubuntu/Debian)
```bash
# Create fonts directory if it doesn't exist
mkdir -p ~/.local/share/fonts

# Copy all fonts to the fonts directory
cp AllFontsSoltani/*.ttf ~/.local/share/fonts/

# Refresh font cache
fc-cache -fv

# Verify installation
fc-list | grep -i "font_name"
```

## Popular Fonts in This Collection

### For Books and Documents
- **B Nazanin** - Classic, widely used
- **B Mitra** - Clean and readable
- **IRANSans** - Professional, modern
- **Sahel** - Clean, good for long texts

### For Titles and Headers
- **B Titr** - Bold, good for titles
- **B Yekan** - Modern sans-serif

### Elegant Options
- **B Lotus** - Elegant style
- **Shabnam** - Beautiful, elegant
- **Tanha** - Unique, artistic

## Testing Fonts

Use the provided `soltani_fonts_test.tex` file:

1. Open the file
2. Uncomment one font at a time:
   ```latex
   \settextfont{B Nazanin}  % Uncomment this line
   % \settextfont{B Mitra}  % Comment others
   ```
3. Compile with XeLaTeX:
   ```bash
   xelatex soltani_fonts_test.tex
   ```
4. Check the output PDF
5. Try different fonts until you find your favorite

## Recommended Fonts for Different Uses

### Academic Books
```latex
\settextfont{B Nazanin}
% or
\settextfont{IRANSans}
```

### Modern Documents
```latex
\settextfont{Sahel}
% or
\settextfont{Samim}
```

### Elegant Publications
```latex
\settextfont{Shabnam}
% or
\settextfont{B Lotus}
```

## Updating Your Persian Template

Once you've chosen a font, update your Persian book template:

```latex
\usepackage{fontspec}
\usepackage{xepersian}

% Replace "YourChosenFont" with the font name you selected
\settextfont[Scale=1.2]{YourChosenFont}
\setdigitfont{YourChosenFont}
\setlatintextfont{Times New Roman}
```

## Troubleshooting

### Font Not Found Error
1. Verify the font is installed:
   ```bash
   fc-list | grep -i "font_name"
   ```
2. Check exact font name spelling
3. Try restarting your LaTeX editor
4. Ensure you're using XeLaTeX (not pdfLaTeX)

### Display Issues
1. Make sure you're compiling with XeLaTeX or LuaLaTeX
2. Check that xepersian package is loaded
3. Verify the font supports Persian characters

## Font Recommendations by Priority

1. **B Nazanin** - Most compatible, widely supported
2. **IRANSans** - Professional, modern look
3. **Sahel** - Clean, good readability
4. **B Mitra** - Classic, reliable
5. **Shabnam** - Elegant, beautiful

Choose based on your document type and personal preference!