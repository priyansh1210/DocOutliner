import re

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove common artifacts
    text = re.sub(r'[^\w\s\-.,():]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def is_likely_heading(text: str) -> bool:
    """Check if text has structural indicators of being a heading."""
    text = text.strip()
    
    # Check for numbering patterns
    numbered_patterns = [
        r'^\d+\.?\s+',
        r'^\d+\.\d+\.?\s+',
        r'^[IVX]+\.?\s+',
        r'^[A-Z]\.?\s+'
    ]
    
    for pattern in numbered_patterns:
        if re.match(pattern, text):
            return True
    
    # Check for all caps (likely heading)
    if len(text) > 3 and text.isupper() and not text.endswith('.'):
        return True
    
    # Check for title case with specific keywords
    heading_keywords = ['introduction', 'conclusion', 'methodology', 'results', 
                       'discussion', 'background', 'literature', 'analysis']
    
    if any(keyword in text.lower() for keyword in heading_keywords):
        return True
    
    return False
