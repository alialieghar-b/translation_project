#!/usr/bin/env python3
"""
High-Quality PDF to Image Converter

A robust Python utility for converting PDF files to high-quality images
with configurable output settings.

Author: Mohammad Hossein Soltani (github.com/soltanegharb)
License: MIT
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional
import logging

try:
    from pdf2image import convert_from_path
    from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError
except ImportError:
    print("Error: pdf2image not installed. Run: pip install pdf2image")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFConverter:
    """High-quality PDF to image converter with configurable settings."""
    
    SUPPORTED_FORMATS = ['PNG', 'JPEG', 'TIFF', 'BMP']
    QUALITY_PRESETS = {
        'web': {'dpi': 150, 'format': 'PNG'},
        'print': {'dpi': 300, 'format': 'PNG'},
        'high': {'dpi': 600, 'format': 'PNG'},
        'archive': {'dpi': 600, 'format': 'TIFF'}
    }
    
    def __init__(self, dpi: int = 300, output_format: str = 'PNG', 
                 thread_count: int = 1):
        """
        Initialize the PDF converter.
        
        Args:
            dpi: Dots per inch for output images (150-600)
            output_format: Output image format (PNG, JPEG, TIFF, BMP)
            thread_count: Number of threads for parallel processing
        """
        # Validate DPI range
        if not 150 <= dpi <= 600:
            raise ValueError(f"DPI must be between 150 and 600, got: {dpi}")
        
        # Validate thread count
        if thread_count < 1:
            raise ValueError(f"Thread count must be at least 1, got: {thread_count}")
        
        self.dpi = dpi
        self.output_format = output_format.upper()
        self.thread_count = thread_count
        
        if self.output_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {output_format}. Supported: {', '.join(self.SUPPORTED_FORMATS)}")
    
    def convert_pdf(self, pdf_path: str, output_dir: str, 
                   filename_prefix: Optional[str] = None) -> List[str]:
        """
        Convert a PDF file to images.
        
        Args:
            pdf_path: Path to the input PDF file
            output_dir: Directory to save output images
            filename_prefix: Optional prefix for output filenames
            
        Returns:
            List of paths to generated image files
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            PDFInfoNotInstalledError: If poppler-utils not installed
            PDFPageCountError: If PDF is corrupted or unreadable
        """
        pdf_path = Path(pdf_path)
        output_dir = Path(output_dir)
        
        # Validate inputs
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.suffix.lower() == '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set filename prefix
        if filename_prefix is None:
            filename_prefix = pdf_path.stem
        
        logger.info(f"Converting {pdf_path} to {self.output_format} at {self.dpi} DPI")
        
        try:
            # Convert PDF to images
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                output_folder=None,  # We'll handle saving manually
                fmt=self.output_format.lower(),
                thread_count=self.thread_count,
                poppler_path=None  # Use system poppler
            )
            
            output_paths = []
            
            # Save images with proper naming
            for i, image in enumerate(images, 1):
                filename = f"{filename_prefix}_page_{i:03d}.{self.output_format.lower()}"
                output_path = output_dir / filename
                
                # Save with optimal quality settings
                save_kwargs = {'format': self.output_format}
                if self.output_format == 'JPEG':
                    save_kwargs['quality'] = 95
                    save_kwargs['optimize'] = True
                elif self.output_format == 'PNG':
                    save_kwargs['optimize'] = True
                
                image.save(output_path, **save_kwargs)
                output_paths.append(str(output_path))
                logger.info(f"Saved: {output_path}")
            
            logger.info(f"Successfully converted {len(images)} pages")
            return output_paths
            
        except PDFInfoNotInstalledError:
            logger.error("Poppler not installed. Please install poppler-utils")
            raise
        except PDFPageCountError as e:
            logger.error(f"PDF appears to be corrupted: {e}")
            raise
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            raise
    
    def convert_directory(self, input_dir: str, output_dir: str) -> dict:
        """
        Convert all PDF files in a directory.
        
        Args:
            input_dir: Directory containing PDF files
            output_dir: Directory to save output images
            
        Returns:
            Dictionary mapping PDF paths to their output image paths
        """
        input_dir = Path(input_dir)
        results = {}
        
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        pdf_files = list(input_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {input_dir}")
            return results
        
        logger.info(f"Found {len(pdf_files)} PDF files to convert")
        
        for pdf_file in pdf_files:
            try:
                output_paths = self.convert_pdf(pdf_file, output_dir)
                results[str(pdf_file)] = output_paths
            except Exception as e:
                logger.error(f"Failed to convert {pdf_file}: {e}")
                results[str(pdf_file)] = []
        
        return results


def main():
    """Command-line interface for the PDF converter."""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to high-quality images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf --output-dir ./images
  %(prog)s input.pdf --dpi 600 --format TIFF
  %(prog)s --input-dir ./pdfs --output-dir ./images --preset high
  %(prog)s input.pdf --output-dir ./images --prefix document
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        'input_file', nargs='?',
        help='Path to input PDF file'
    )
    input_group.add_argument(
        '--input-dir',
        help='Directory containing PDF files to convert'
    )
    
    # Output options
    parser.add_argument(
        '--output-dir', '-o',
        default='./output',
        help='Output directory for images (default: ./output)'
    )
    parser.add_argument(
        '--prefix',
        help='Filename prefix for output images (default: PDF filename)'
    )
    
    # Quality options
    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='Output resolution in DPI (default: 300)'
    )
    parser.add_argument(
        '--format',
        choices=['PNG', 'JPEG', 'TIFF', 'BMP'],
        default='PNG',
        help='Output image format (default: PNG)'
    )
    parser.add_argument(
        '--preset',
        choices=['web', 'print', 'high', 'archive'],
        help='Quality preset (overrides --dpi and --format)'
    )
    
    # Performance options
    parser.add_argument(
        '--threads',
        type=int,
        default=1,
        help='Number of threads for parallel processing (default: 1)'
    )
    
    # Utility options
    parser.add_argument(
        '--version',
        action='version',
        version='PDF Converter 1.0.0'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Apply quality preset if specified
    if args.preset:
        preset = PDFConverter.QUALITY_PRESETS[args.preset]
        args.dpi = preset['dpi']
        args.format = preset['format']
        logger.info(f"Using {args.preset} preset: {args.dpi} DPI, {args.format}")
    
    try:
        # Initialize converter
        converter = PDFConverter(
            dpi=args.dpi,
            output_format=args.format,
            thread_count=args.threads
        )
        
        # Convert files
        if args.input_file:
            # Single file conversion
            output_paths = converter.convert_pdf(
                args.input_file,
                args.output_dir,
                args.prefix
            )
            print(f"✓ Converted {len(output_paths)} pages")
            for path in output_paths:
                print(f"  → {path}")
        
        elif args.input_dir:
            # Directory conversion
            results = converter.convert_directory(args.input_dir, args.output_dir)
            
            total_pages = sum(len(paths) for paths in results.values())
            successful_files = sum(1 for paths in results.values() if paths)
            
            print(f"✓ Processed {len(results)} PDF files")
            print(f"✓ Successfully converted {successful_files} files")
            print(f"✓ Generated {total_pages} images")
            
            # Show failed conversions
            failed_files = [pdf for pdf, paths in results.items() if not paths]
            if failed_files:
                print(f"✗ Failed to convert {len(failed_files)} files:")
                for pdf in failed_files:
                    print(f"  → {pdf}")
    
    except KeyboardInterrupt:
        logger.info("Conversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()