#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path

# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pdf_processor import PDFProcessor

def main():
    """Main entry point for PDF structure extraction."""
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize processor
    processor = PDFProcessor()
    
    # Process all PDF files in input directory
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    for pdf_file in pdf_files:
        try:
            print(f"Processing: {pdf_file.name}")
            result = processor.extract_structure(str(pdf_file))
            
            # Save output with same name as input
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
                
            print(f"Output saved: {output_file.name}")
            
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {str(e)}")
            # Continue processing other files instead of exiting
            continue

if __name__ == "__main__":
    main()
