import re
import json
from typing import Dict, List
from pathlib import Path
from langdetect import detect, LangDetectError

class MultilingualHandler:
    def __init__(self):
        self.heading_patterns = self._load_heading_patterns()
        
    def _load_heading_patterns(self) -> Dict:
        """Load multilingual heading patterns."""
        patterns_path = Path(__file__).parent.parent / "data" / "heading_patterns.json"
        if patterns_path.exists():
            with open(patterns_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_default_patterns()
    
    def _get_default_patterns(self) -> Dict:
        """Default heading patterns for multiple languages."""
        return {
            "universal": [
                r'^\d+\.?\s+.*',
                r'^\d+\.\d+\.?\s+.*',
                r'^\d+\.\d+\.\d+\.?\s+.*',
                r'^[IVX]+\.?\s+.*',
                r'^[A-Z]\.?\s+.*'
            ],
            "en": [
                r'^\s*Chapter\s+\d+',
                r'^\s*Section\s+\d+',
                r'^\s*(Introduction|Conclusion|Abstract|Summary)'
            ],
            "es": [
                r'^\s*Capítulo\s+\d+',
                r'^\s*(Introducción|Conclusión|Resumen)'
            ],
            "fr": [
                r'^\s*Chapitre\s+\d+',
                r'^\s*(Introduction|Conclusion|Résumé)'
            ],
            "de": [
                r'^\s*Kapitel\s+\d+',
                r'^\s*(Einleitung|Zusammenfassung)'
            ],
            "zh": [
                r'^\s*第\s*\d+\s*章',
                r'^\s*(引言|结论|摘要)'
            ],
            "ar": [
                r'^\s*الفصل\s+\d+',
                r'^\s*(المقدمة|الخاتمة|الملخص)'
            ]
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language from text."""
        if not text or len(text.strip()) < 10:
            return "en"
        
        try:
            return detect(text)
        except (LangDetectError, Exception):
            return "en"
    
    def normalize_text(self, text: str, language: str) -> str:
        """Normalize text based on language."""
        if not text:
            return ""
        
        # Unicode normalization
        import unicodedata
        text = unicodedata.normalize('NFKC', text)
        
        # General cleanup
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def is_heading_by_pattern(self, text: str, language: str) -> bool:
        """Check if text matches heading patterns."""
        patterns = self.heading_patterns.get("universal", [])
        if language in self.heading_patterns:
            patterns.extend(self.heading_patterns[language])
        
        normalized_text = self.normalize_text(text, language)
        
        for pattern in patterns:
            if re.match(pattern, normalized_text, re.IGNORECASE | re.UNICODE):
                return True
        
        return False
    
    def extract_heading_number(self, text: str, language: str) -> str:
        """Extract heading number from text."""
        normalized_text = self.normalize_text(text, language)
        
        # Universal numeric patterns
        patterns = [
            r'^(\d+)\.?\s+',
            r'^(\d+\.\d+)\.?\s+',
            r'^(\d+\.\d+\.\d+)\.?\s+',
            r'^([IVX]+)\.?\s+',
            r'^([A-Z])\.?\s+'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, normalized_text)
            if match:
                return match.group(1)
        
        return ""
