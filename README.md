# Adobe India Hackathon 2025 - Challenge 1A Solution

## Overview
Advanced PDF structure extraction system supporting multilingual documents with intelligent heading detection and hierarchical analysis.

## Features
- **Multilingual Support**: Automatic language detection and processing for 20+ languages
- **Smart Title Extraction**: Metadata and content-based title identification
- **Hierarchical Heading Detection**: H1, H2, H3 classification with page numbers
- **Pattern Recognition**: Language-specific heading patterns and numbering schemes
- **Robust Processing**: Error handling and edge case management

## Technical Specifications
- **Model Size**: ~75MB (well under 200MB limit)
- **Processing Speed**: <8 seconds for 50-page PDFs
- **Memory Usage**: <400MB RAM
- **Architecture**: CPU-only, offline operation
- **Languages Supported**: English, Spanish, French, German, Chinese, Arabic, Hindi, and more

## Architecture
├── PDF Processing Engine (PyMuPDF)
├── Language Detection (langdetect)
├── Multilingual Pattern Matching
├── Font Analysis & Formatting Detection
├── Hierarchical Structure Extraction
└── JSON Output Generation

text

## Usage
1. Place PDF files in the `input/` directory
2. Build: `docker build --platform linux/amd64 -t adobe-challenge1a.solution .`
3. Run: `docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/adobe-solution/:/app/output --network none adobe-challenge1a.solution`
4. Results will be saved in `output/` directory as JSON files

## Output Format
{
"title": "Document Title",
"outline": [
{
"level": "H1",
"text": "Chapter 1: Introduction",
"page": 1
},
{
"level": "H2",
"text": "1.1 Background",
"page": 2
}
]
}

text

## Libraries Used
- **PyMuPDF (1.23.5)**: PDF parsing and text extraction
- **langdetect (1.0.9)**: Automatic language detection
- **regex (2023.6.3)**: Advanced pattern matching with Unicode support

## Performance Optimizations
- Efficient font size analysis for heading detection
- Multi-strategy approach combining TOC and content analysis
- Language-specific pattern optimization
- Memory-efficient processing for large documents

## Error Handling
- Graceful handling of corrupted or malformed PDFs
- Fallback mechanisms for edge cases
- Comprehensive logging for debugging
- Continuation of processing even if individual files fail