# File_SAM_recovery

A Python tool to recover or analyze corrupted or deleted `.sam` files from Ami Pro/Lotus Word Pro.

## Features
- Extract readable text from corrupted `.sam` files.
- Analyze binary structure and display hexadecimal view.
- Attempt recovery of deleted `.sam` files using TestDisk.

## Requirements
- Python 3.6+
- [TestDisk](https://www.cgsecurity.org/wiki/TestDisk) (optional, for recovery mode)
- No additional Python libraries required (uses standard library).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/recover_sam.git

Usage
Run the script with:
bash

python recover_sam.py <file_path> --mode <mode> --output <output_folder>

<file_path>: Path to the .sam file or disk (e.g., C:\ for TestDisk).

<mode>: text (extract text), binary (analyze binary), testdisk (recover deleted file).

<output_folder>: Folder to save results (default: output).

Example:
bash

python recover_sam.py document.sam --mode text --output results
python recover_sam.py C:\ --mode testdisk --output results

Output
Results are saved in the specified output folder with a timestamp (e.g., recovered_sam_20250526_153500.txt).

