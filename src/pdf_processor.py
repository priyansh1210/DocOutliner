import fitz  # PyMuPDF
import re
from typing import Dict, List
from .heading_detector import HeadingDetector
from .multilingual_handler import MultilingualHandler
from .utils import clean_text

class PDFProcessor:
    def __init__(self):
        self.heading_detector = HeadingDetector()
        self.multilingual_handler = MultilingualHandler()
        self.document_language = "en"
    
    def extract_structure(self, pdf_path: str) -> Dict:
        """Extract title and hierarchical structure from PDF."""
        doc = fitz.open(pdf_path)
        
        try:
            # Detect document language
            self.document_language = self._detect_document_language(doc)
            
            # Extract document title
            title = self._extract_title(doc)
            
            # Extract outline structure
            outline = self._extract_outline(doc)
            
            return {
                "title": title,
                "outline": outline
            }
        
        finally:
            doc.close()
    
    def _detect_document_language(self, doc) -> str:
        """Detect primary language of document."""
        sample_text = ""
        pages_to_sample = min(3, len(doc))
        
        for page_num in range(pages_to_sample):
            page = doc[page_num]
            page_text = page.get_text()
            sample_text += page_text[:1000]
            
            if len(sample_text) > 2000:
                break
        
        if sample_text.strip():
            return self.multilingual_handler.detect_language(sample_text)
        
        return "en"
    
    def _extract_title(self, doc) -> str:
        """Extract document title from metadata or content."""
        # Try metadata first
        metadata = doc.metadata
        if metadata.get('title') and len(metadata['title'].strip()) > 0:
            title = metadata['title']
            return self.multilingual_handler.normalize_text(title, self.document_language)
        
        # Try first page content analysis
        if len(doc) > 0:
            page = doc[0]
            blocks = page.get_text("dict")["blocks"]
            
            largest_font_size = 0
            title_candidate = ""
            
            for block in blocks:
                if block.get("type") == 0:  # Text block
                    for line in block.get("lines", []):
                        line_text = ""
                        max_font_size = 0
                        
                        for span in line.get("spans", []):
                            font_size = span.get("size", 0)
                            text = span.get("text", "").strip()
                            
                            line_text += text + " "
                            max_font_size = max(max_font_size, font_size)
                        
                        line_text = line_text.strip()
                        
                        # Check if this could be title (large font, reasonable length)
                        if (max_font_size > largest_font_size and 
                            len(line_text) > 5 and len(line_text) < 200 and
                            not self._is_likely_heading_pattern(line_text)):
                            largest_font_size = max_font_size
                            title_candidate = line_text
            
            if title_candidate:
                return self.multilingual_handler.normalize_text(title_candidate, self.document_language)
        
        # Fallback title
        return self._get_fallback_title()
    
    def _is_likely_heading_pattern(self, text: str) -> bool:
        """Check if text matches common heading patterns."""
        patterns = [
            r'^\d+\.?\s+',           # "1. " or "1 "
            r'^\d+\.\d+\.?\s+',      # "1.1. " or "1.1 "
            r'^Chapter\s+\d+',       # "Chapter 1"
            r'^Section\s+\d+',       # "Section 1"
        ]
        
        for pattern in patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _get_fallback_title(self) -> str:
        """Get fallback title based on detected language."""
        fallback_titles = {
            "en": "Untitled Document",
            "es": "Documento Sin Título",
            "fr": "Document Sans Titre",
            "de": "Unbenanntes Dokument",
            "ru": "Документ Без Названия",
            "zh": "无标题文档",
            "ja": "タイトルなしのドキュメント",
            "ar": "وثيقة بلا عنوان",
            "hi": "शीर्षकहीन दस्तावेज़",
        }
        return fallback_titles.get(self.document_language, fallback_titles["en"])
    
    def _extract_outline(self, doc) -> List[Dict]:
        """Extract hierarchical outline from PDF."""
        outline = []
        
        # Try built-in TOC first
        toc = doc.get_toc()
        if toc:
            for entry in toc:
                level, title, page_num = entry
                heading_level = f"H{min(level, 3)}"
                normalized_title = self.multilingual_handler.normalize_text(title, self.document_language)
                outline.append({
                    "level": heading_level,
                    "text": normalized_title,
                    "page": page_num
                })
        else:
            # Extract from content analysis
            outline = self._extract_from_content(doc)
        
        return outline
    
    def _extract_from_content(self, doc) -> List[Dict]:
        """Extract headings by analyzing content."""
        headings = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            
            page_headings = self.heading_detector.detect_headings(
                blocks, page_num + 1, self.document_language
            )
            headings.extend(page_headings)
        
        return self._post_process_headings(headings)
    
    def _post_process_headings(self, headings: List[Dict]) -> List[Dict]:
        """Post-process headings for consistency."""
        processed_headings = []
        
        for heading in headings:
            processed_heading = {
                "level": heading["level"],
                "text": heading["text"],
                "page": heading["page"]
            }
            processed_headings.append(processed_heading)
        
        return processed_headings
