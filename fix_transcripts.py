#!/usr/bin/env python3
import sys
import argparse
from typing import Dict, Optional
import re

"""
# To overwrite the input file
python fix_transcripts.py input.md

# To create a new output file
python fix_transcripts.py input.md -o output.md
"""

def create_fix_mapping(custom_mapping: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Creates a mapping dictionary for text replacements.
    Combines default mappings with any custom mappings provided.
    """
    default_mapping = {
        # ML orgs
        "noose": "Nous",
        "Dali": "DALL·E",
        "DeepSeq": "DeepSeek",

        # models
        " lama ": " Llama ",
        "Lama": "Llama",
        "LAMA": "Llama",
        "Lama 1": "Llama 1",
        "OMO2": "OLMo 2",
        "OMO1": "OLMo 1",
        "ALMO": "OLMo",
        "Allmo": "OLMo",

        # names
        "Swyggs": "Swyx",
        "Grenenfeld": "Groeneveld",
        "Kyle Lowe": "Kyle Lo",
        "Luca Soldini": "Luca Soldaini",
    }
    
    if custom_mapping:
        default_mapping.update(custom_mapping)
    
    return default_mapping

def fix_transcript(content: str, mapping: Dict[str, str]) -> str:
    """
    Applies text replacements to content based on the provided mapping.
    Uses regex word boundaries for whole word replacements where appropriate.
    """
    fixed_content = content
    
    for wrong, correct in mapping.items():
        # If the wrong text contains spaces, treat it as a phrase
        if ' ' in wrong:
            fixed_content = fixed_content.replace(wrong, correct)
        else:
            # Use word boundaries for single words to avoid partial replacements
            pattern = rf'\b{re.escape(wrong)}\b'
            fixed_content = re.sub(pattern, correct, fixed_content)
    
    return fixed_content

def process_file(input_file: str, output_file: Optional[str] = None, mapping: Optional[Dict[str, str]] = None) -> None:
    """
    Processes a markdown file, applying the text replacements and saving the result.
    If no output file is specified, overwrites the input file.
    """
    # Use default mapping if none provided
    fix_mapping = create_fix_mapping(mapping)
    
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply fixes
        fixed_content = fix_transcript(content, fix_mapping)
        
        # Determine output file
        output_path = output_file if output_file else input_file
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
            
        print(f"Successfully processed {input_file}")
        if output_file:
            print(f"Output written to {output_file}")
            
    except FileNotFoundError:
        print(f"Error: Could not find file {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Fix transcription errors in markdown files.')
    parser.add_argument('input_file', help='Input markdown file to process')
    parser.add_argument('-o', '--output', help='Output file (optional, defaults to overwriting input)')
    
    args = parser.parse_args()
    
    process_file(args.input_file, args.output)

if __name__ == "__main__":
    main()