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
   bash  git clone https://github.com/ProfesseurFalken/File_SAM-recovery.git
      
