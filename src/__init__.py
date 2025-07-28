"""
Adobe India Hackathon 2025 - Challenge 1A
PDF Structure Extraction Package
"""

__version__ = "1.0.0"
__author__ = "Adobe Hackathon Team"
__description__ = "Multilingual PDF structure extraction with intelligent heading detection"

# Package-level imports for easier access
from .pdf_processor import PDFProcessor
from .heading_detector import HeadingDetector
from .multilingual_handler import MultilingualHandler
from .utils import clean_text, is_likely_heading

__all__ = [
    'PDFProcessor',
    'HeadingDetector', 
    'MultilingualHandler',
    'clean_text',
    'is_likely_heading'
]
