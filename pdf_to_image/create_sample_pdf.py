#!/usr/bin/env python3
"""
Create a sample PDF for testing the converter.
This script creates a simple multi-page PDF for testing purposes.
"""

import os
import sys
from pathlib import Path

def create_simple_pdf(filename="sample.pdf"):
    """Create a simple PDF using reportlab if available, otherwise provide instructions."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Create a simple multi-page PDF
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Page 1
        c.drawString(100, height - 100, "PDF to Image Converter - Test Document")
        c.drawString(100, height - 150, "Page 1 of 3")
        c.drawString(100, height - 200, "This is a sample PDF created for testing.")
        c.drawString(100, height - 250, "It contains multiple pages with different content.")
        c.showPage()
        
        # Page 2
        c.drawString(100, height - 100, "Page 2 of 3")
        c.drawString(100, height - 150, "This page contains some additional text.")
        c.drawString(100, height - 200, "Testing different DPI settings:")
        c.drawString(100, height - 250, "• 150 DPI (web quality)")
        c.drawString(100, height - 300, "• 300 DPI (print quality)")
        c.drawString(100, height - 350, "• 600 DPI (high quality)")
        c.showPage()
        
        # Page 3
        c.drawString(100, height - 100, "Page 3 of 3")
        c.drawString(100, height - 150, "Final page for testing.")
        c.drawString(100, height - 200, "Test different output formats:")
        c.drawString(100, height - 250, "• PNG (default)")
        c.drawString(100, height - 300, "• JPEG (compressed)")
        c.drawString(100, height - 350, "• TIFF (archival)")
        c.drawString(100, height - 400, "• BMP (uncompressed)")
        
        c.save()
        print(f"✓ Created sample PDF: {filename}")
        return True
        
    except ImportError:
        print("reportlab not installed. Install with: pip install reportlab")
        print("\nAlternative methods to create a test PDF:")
        print("1. Use any word processor to create and export a PDF")
        print("2. Use online PDF generators")
        print("3. Install pandoc and run: echo 'Test content' | pandoc -o sample.pdf")
        return False

def main():
    """Main function to create sample PDF."""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "sample.pdf"
    
    if Path(filename).exists():
        response = input(f"File {filename} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    success = create_simple_pdf(filename)
    
    if success:
        print(f"\nNow you can test the converter with:")
        print(f"python pdf_converter.py {filename} --output-dir ./test_output")
        print(f"python pdf_converter.py {filename} --preset high")
        print(f"python pdf_converter.py {filename} --format JPEG --dpi 150")

if __name__ == "__main__":
    main()