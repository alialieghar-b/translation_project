#!/usr/bin/env python3
"""
Test suite for PDF to Image Converter

Validates the functionality and quality of the PDF conversion utility.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import os
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pdf_converter import PDFConverter
except ImportError as e:
    print(f"Error importing pdf_converter: {e}")
    print("Make sure pdf2image is installed: pip install pdf2image")
    sys.exit(1)


class TestPDFConverter(unittest.TestCase):
    """Test cases for PDFConverter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.converter = PDFConverter(dpi=150, output_format='PNG')
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_converter_initialization(self):
        """Test converter initialization with various parameters."""
        # Test default initialization
        converter = PDFConverter()
        self.assertEqual(converter.dpi, 300)
        self.assertEqual(converter.output_format, 'PNG')
        self.assertEqual(converter.thread_count, 1)
        
        # Test custom initialization
        converter = PDFConverter(dpi=600, output_format='JPEG', thread_count=2)
        self.assertEqual(converter.dpi, 600)
        self.assertEqual(converter.output_format, 'JPEG')
        self.assertEqual(converter.thread_count, 2)
    
    def test_invalid_format(self):
        """Test that invalid formats raise ValueError."""
        with self.assertRaises(ValueError):
            PDFConverter(output_format='INVALID')
    
    def test_invalid_dpi(self):
        """Test that invalid DPI values raise ValueError."""
        with self.assertRaises(ValueError):
            PDFConverter(dpi=100)  # Too low
        with self.assertRaises(ValueError):
            PDFConverter(dpi=700)  # Too high
    
    def test_invalid_thread_count(self):
        """Test that invalid thread counts raise ValueError."""
        with self.assertRaises(ValueError):
            PDFConverter(thread_count=0)
        with self.assertRaises(ValueError):
            PDFConverter(thread_count=-1)
    
    def test_quality_presets(self):
        """Test quality preset configurations."""
        presets = PDFConverter.QUALITY_PRESETS
        
        # Verify all presets exist
        expected_presets = ['web', 'print', 'high', 'archive']
        for preset in expected_presets:
            self.assertIn(preset, presets)
            self.assertIn('dpi', presets[preset])
            self.assertIn('format', presets[preset])
        
        # Verify preset values
        self.assertEqual(presets['web']['dpi'], 150)
        self.assertEqual(presets['print']['dpi'], 300)
        self.assertEqual(presets['high']['dpi'], 600)
        self.assertEqual(presets['archive']['dpi'], 600)
    
    def test_nonexistent_file(self):
        """Test handling of non-existent PDF files."""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert_pdf('nonexistent.pdf', self.test_dir)
    
    def test_non_pdf_file(self):
        """Test handling of non-PDF files."""
        # Create a dummy text file
        dummy_file = Path(self.test_dir) / 'dummy.txt'
        dummy_file.write_text('This is not a PDF')
        
        with self.assertRaises(ValueError):
            self.converter.convert_pdf(str(dummy_file), self.test_dir)
    
    def test_output_directory_creation(self):
        """Test that output directories are created automatically."""
        output_dir = Path(self.test_dir) / 'new_output_dir'
        self.assertFalse(output_dir.exists())
        
        # Create a dummy PDF file for testing
        dummy_pdf = Path(self.test_dir) / 'dummy.pdf'
        dummy_pdf.write_text('%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n')
        
        # This should create the directory even if conversion fails
        try:
            self.converter.convert_pdf(str(dummy_pdf), str(output_dir))
        except Exception:
            pass  # Expected to fail with invalid PDF, but directory should be created
        
        self.assertTrue(output_dir.exists())


class TestCLIInterface(unittest.TestCase):
    """Test cases for command-line interface."""
    
    def test_argument_parsing(self):
        """Test command-line argument parsing."""
        # This would require more complex testing with subprocess
        # For now, we'll just verify the main function exists
        from pdf_converter import main
        self.assertTrue(callable(main))


def create_sample_pdf():
    """
    Create a simple sample PDF for testing.
    Note: This requires reportlab or similar library for PDF creation.
    For now, we'll provide instructions for manual testing.
    """
    print("\n" + "="*60)
    print("MANUAL TESTING INSTRUCTIONS")
    print("="*60)
    print("To fully test the converter, you'll need a sample PDF file.")
    print("You can:")
    print("1. Create a simple PDF using any application")
    print("2. Download a sample PDF from the internet")
    print("3. Use the following command to create a test PDF:")
    print("   echo 'Test content' | pandoc -o test.pdf")
    print("\nThen run:")
    print("   python pdf_converter.py test.pdf --output-dir ./test_output")
    print("="*60)


def run_integration_tests():
    """Run integration tests if sample PDFs are available."""
    print("\n" + "="*60)
    print("INTEGRATION TEST SUGGESTIONS")
    print("="*60)
    
    test_cases = [
        {
            'name': 'Basic Conversion',
            'command': 'python pdf_converter.py sample.pdf --output-dir ./output',
            'expected': 'PNG files at 300 DPI'
        },
        {
            'name': 'High Quality',
            'command': 'python pdf_converter.py sample.pdf --preset high',
            'expected': 'PNG files at 600 DPI'
        },
        {
            'name': 'JPEG Output',
            'command': 'python pdf_converter.py sample.pdf --format JPEG --dpi 150',
            'expected': 'JPEG files at 150 DPI'
        },
        {
            'name': 'Directory Processing',
            'command': 'python pdf_converter.py --input-dir ./pdfs --output-dir ./images',
            'expected': 'All PDFs in directory converted'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"{i}. {test['name']}")
        print(f"   Command: {test['command']}")
        print(f"   Expected: {test['expected']}")
        print()
    
    print("Run these commands with actual PDF files to verify functionality.")
    print("="*60)


if __name__ == '__main__':
    print("PDF to Image Converter - Test Suite")
    print("="*50)
    
    # Run unit tests
    print("\nRunning unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Provide manual testing instructions
    create_sample_pdf()
    run_integration_tests()