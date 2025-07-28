"""
Data module for Adobe Hackathon Challenge 1A
Contains configuration files and patterns for multilingual processing
"""

import json
from pathlib import Path

def load_heading_patterns():
    """Load heading patterns configuration."""
    patterns_path = Path(__file__).parent / "heading_patterns.json"
    if patterns_path.exists():
        with open(patterns_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_language_config():
    """Load language configuration."""
    config_path = Path(__file__).parent / "language_config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

__all__ = ['load_heading_patterns', 'load_language_config']
