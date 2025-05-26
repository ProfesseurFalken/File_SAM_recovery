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

Run the script from the command line with the following syntax:

```bash
python File_SAM_recovery <file_path> --mode <mode> --output <output_folder>

### Arguments
- `<file_path>`: Path to the `.sam` file (e.g., `document.sam`) or disk (e.g., `C:\` for TestDisk mode).
- `<mode>`: Choose one of the following:
  - `text`: Extract readable text from a corrupted `.sam` file.
  - `binary`: Analyze binary data and display a hexadecimal view with readable segments.
  - `images`: Extract embedded images (JPEG, PNG) from the `.sam` file.
  - `metadata`: Retrieve file creation and modification dates.
  - `testdisk`: Recover deleted or overwritten `.sam` files using TestDisk (requires TestDisk installation).
  - `all`: Run `text`, `binary`, `images`, and `metadata` modes together (excludes `testdisk`).
- `<output_folder>`: Directory to save results (default: `output`). Results are saved with a timestamp (e.g., `recovered_sam_20250526_153500.txt`, `extracted_image_20250526_153500_1.jpg`).

### Examples
```bash
# Extract text from a .sam file
python File_SAM_recovery.py document.sam --mode text --output results

# Extract embedded images
python File_SAM_recovery.py document.sam --mode images --output results

# Retrieve file metadata (creation/modification dates)
python File_SAM_recovery.py document.sam --mode metadata --output results

# Analyze binary data
python File_SAM_recovery.py document.sam --mode binary --output results

# Run all analysis modes (text, binary, images, metadata)
python File_SAM_recovery.py document.sam --mode all --output results

# Recover deleted files using TestDisk
python File_SAM_recovery.py C:\ --mode testdisk --output results
