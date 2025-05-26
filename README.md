# File_SAM_recovery

A Python tool to recover or analyze corrupted or deleted `.sam` files from Ami Pro/Lotus Word Pro.

## Features
- Extract readable text from corrupted `.sam` files.
- Analyze binary structure and display hexadecimal view.
- Extract potential images (JPEG, PNG) embedded in `.sam` files.
- Retrieve file metadata (creation and modification dates).
- Attempt recovery of deleted `.sam` files using TestDisk.
- Combined mode (`all`) for full analysis (text, binary, images, metadata).

## Requirements
- Python 3.6+
- [TestDisk](https://www.cgsecurity.org/wiki/TestDisk) (optional, for recovery mode)
- No additional Python libraries required (uses standard library).

## Installation
1. Clone the repository:
   bash
   git clone https://github.com/ProfesseurFalken/File_SAM-recovery.git
      
## Usage
   Run the script with:
   bash  
   git clone https://github.com/ProfesseurFalken/File_SAM-recovery.git

   <file_path>: Path to the .sam file or disk (e.g., C:\ for TestDisk).

   <mode>: 
      text: Extract readable text.
      binary: Analyze binary data and display hexadecimal view.
      images: Extract embedded images (JPEG, PNG).
      metadata: Retrieve file creation and modification dates.
      testdisk: Recover deleted files using TestDisk.
      all: Run text, binary, images, and metadata modes together.
      <output_folder>: Folder to save results (default: output).

# Examples:
   bash

   python recover_sam.py document.sam --mode text --output results
   python recover_sam.py document.sam --mode images --output results
   python recover_sam.py document.sam --mode all --output results
   python recover_sam.py C:\ --mode testdisk --output results

# Output
   Results are saved in the specified output folder with a timestamp (e.g., recovered_sam_20250526_153500.txt for text/metadata, extracted_image_20250526_153500_1.jpg for images).

