import re
from typing import List, Dict
from .utils import clean_text, is_likely_heading
from .multilingual_handler import MultilingualHandler

class HeadingDetector:
    def __init__(self):
        self.multilingual_handler = MultilingualHandler()
    
    def detect_headings(self, blocks: List, page_num: int, document_language: str = "en") -> List[Dict]:
        """Detect headings from page blocks with multilingual support."""
        headings = []
        font_sizes = []
        
        # Collect all font sizes for relative comparison
        for block in blocks:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        font_sizes.append(span.get("size", 12))
        
        if not font_sizes:
            return headings
        
        avg_font_size = sum(font_sizes) / len(font_sizes)
        
        # Analyze each text block
        for block in blocks:
            if block.get("type") == 0:
                for line in block.get("lines", []):
                    line_text = ""
                    max_font_size = 0
                    is_bold = False
                    
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        font_size = span.get("size", 12)
                        flags = span.get("flags", 0)
                        
                        line_text += text + " "
                        max_font_size = max(max_font_size, font_size)
                        is_bold = is_bold or (flags & 2**4)  # Bold flag
                    
                    line_text = line_text.strip()
                    
                    if self._is_heading_candidate(line_text, max_font_size, avg_font_size, is_bold, document_language):
                        level = self._determine_heading_level(line_text, max_font_size, avg_font_size, document_language)
                        cleaned_text = self.multilingual_handler.normalize_text(line_text, document_language)
                        
                        headings.append({
                            "level": level,
                            "text": cleaned_text,
                            "page": page_num
                        })
        
        return headings
    
    def _is_heading_candidate(self, text: str, font_size: float, avg_font_size: float, is_bold: bool, language: str) -> bool:
        """Determine if text is likely a heading."""
        if not text or len(text.strip()) < 2:
            return False
        
        # Adjust length limits for different languages
        min_length = 2 if language in ['zh', 'ja', 'ko'] else 3
        max_length = 300 if language in ['zh', 'ja', 'ko'] else 200
        
        if len(text.strip()) < min_length or len(text) > max_length:
            return False
        
        # Check formatting and pattern criteria
        size_threshold = font_size > avg_font_size * 1.1
        pattern_match = self.multilingual_handler.is_heading_by_pattern(text, language)
        structure_indicators = is_likely_heading(text)
        
        return (size_threshold and (is_bold or pattern_match)) or structure_indicators or pattern_match
    
    def _determine_heading_level(self, text: str, font_size: float, avg_font_size: float, language: str) -> str:
        """Determine heading level H1, H2, or H3."""
        size_ratio = font_size / avg_font_size if avg_font_size > 0 else 1.0
        
        # Extract heading number for level determination
        heading_number = self.multilingual_handler.extract_heading_number(text, language)
        
        if heading_number:
            if '.' not in heading_number:
                return "H1"
            elif heading_number.count('.') == 1:
                return "H2"
            else:
                return "H3"
        
        # Font size based classification
        if size_ratio >= 1.5:
            return "H1"
        elif size_ratio >= 1.2:
            return "H2"
        else:
            return "H3"
