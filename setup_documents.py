#!/usr/bin/env python3
"""
Setup script for French cultural documents
Creates the document structure and provides guidance for adding cultural content.
"""

import os
import shutil
from pathlib import Path

def create_documents_structure():
    """Create the documents folder structure"""
    
    # Create main documents folder
    documents_folder = "Info for French"
    if not os.path.exists(documents_folder):
        os.makedirs(documents_folder)
        print(f"Created folder: {documents_folder}")
    
    # Create README with instructions
    readme_content = """# French Cultural Documents

This folder should contain your French cultural documents for the assistant to reference.

## Legal Sources to Use:

✅ **RECOMMENDED:**
- IMDb plot summaries
- Wikipedia film articles  
- Your own viewing notes
- Educational website analyses
- Book summaries and reviews
- Public domain texts

❌ **AVOID:**
- Full movie transcripts (copyrighted)
- Complete book texts (unless public domain)
- Any copyrighted material

## File Types Supported:
- PDF files (.pdf)
- Text files (.txt)

## Example Files:
- le_petit_prince.pdf (your book PDF)
- coco_avant_chanel_summary.txt (plot summary)
- la_mome_analysis.txt (film analysis)
- cyrano_plot.txt (story summary)

## Setup Instructions:
1. Add your legally obtained files to this folder
2. Run 'python setup_documents.py' again to process them
3. The assistant will automatically use this content for cultural context

## Note:
The assistant will only reference content you provide here. Make sure all content
is legally obtained and properly attributed.
"""
    
    readme_path = os.path.join(documents_folder, "README.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Created README: {readme_path}")
    
    # Create example documents folder
    example_folder = "example_documents"
    if not os.path.exists(example_folder):
        os.makedirs(example_folder)
        print(f"Created folder: {example_folder}")
    
    # Create example summary
    example_content = """Coco avant Chanel (2009) - Summary

This biographical film tells the story of Gabrielle "Coco" Chanel before she became famous.

The story begins with young Coco and her sister working as seamstresses and cabaret singers. 
Coco meets Etienne Balsan, a wealthy textile heir, who becomes her lover and introduces her 
to high society.

Through Balsan, Coco meets Arthur "Boy" Capel, an English businessman. She falls in love 
with Capel and he becomes her greatest supporter, helping her start her fashion business.

The film shows Coco's early struggles and how she developed her revolutionary fashion ideas, 
including her famous "little black dress" and rejection of corsets.

Key themes include independence, creativity, and breaking social conventions. Coco's journey 
from poverty to becoming a fashion icon is inspiring.

The film ends with Coco's first fashion show, marking the beginning of her legendary career.
"""
    
    example_path = os.path.join(example_folder, "coco_avant_chanel_summary.txt")
    with open(example_path, 'w', encoding='utf-8') as f:
        f.write(example_content)
    
    print(f"Created example: {example_path}")
    
    return documents_folder

def check_existing_documents(documents_folder):
    """Check what documents are already in the folder"""
    if not os.path.exists(documents_folder):
        return []
    
    documents = []
    for file_path in Path(documents_folder).rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt']:
            documents.append(str(file_path))
    
    return documents

def main():
    """Main setup function"""
    print("French Cultural Documents Setup")
    print("=" * 40)
    
    # Create folder structure
    documents_folder = create_documents_structure()
    
    # Check existing documents
    existing_docs = check_existing_documents(documents_folder)
    
    if existing_docs:
        print(f"\nFound {len(existing_docs)} existing documents:")
        for doc in existing_docs:
            print(f"  - {os.path.basename(doc)}")
        
        print("\nTo process these documents, run:")
        print("python multi_document_rag.py")
    else:
        print(f"\nNo documents found in '{documents_folder}'")
        print("\nNext steps:")
        print("1. Add your French cultural documents to the 'Info for French' folder")
        print("2. Use legal sources like plot summaries, analyses, or your own notes")
        print("3. Run this script again to process the documents")
        print("4. Start the assistant with: python french_vad_assistant.py")
    
    print(f"\nDocuments folder: {documents_folder}")
    print("Example folder: example_documents")

if __name__ == "__main__":
    main()