#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""Fix DeepModeling brand name from 'Deep Modeling' (with space) to 'DeepModeling' (no space)"""

import os
import re

# Brand name patterns to fix
OLD_NAME = "Deep Modeling"
NEW_NAME = "DeepModeling"

# Common file patterns to check
FILE_PATTERNS = [
    # Documentation files
    "README.md",
    "README.rst",
    "CONTRIBUTING.md",
    "CONTRIBUTING.rst",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "AUTHORS.md",
    "AUTHORS.rst",
    "CHANGELOG.md",
    "CHANGELOG.rst",
    "HISTORY.md",
    "HISTORY.rst",

    # Python files
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    
    # Documentation directories
    "doc/conf.py",
    "docs/conf.py",
    "documentation/conf.py",
    "doc/index.rst",
    "docs/index.rst",
    "doc/index.md",
    "docs/index.md",
    
    # Other config files
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/SECURITY.md",
    ".github/CODE_OF_CONDUCT.md",
    ".github/CONTRIBUTING.md",
]

# Directories to skip during recursive search
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.tox', '.eggs', 
             'dist', 'build', '.pytest_cache', '.venv', 'venv', '.mypy_cache',
             '.nox', '.coverage', 'htmlcov', '.hypothesis'}

# Characters that are valid in text files
# Includes: BEL(7), BS(8), HT(9), LF(10), FF(12), CR(13), ESC(27), and printable chars (0x20-0x7E, 0x80-0xFF)
TEXTCHARS = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})

def is_binary_file(filepath):
    """Check if a file is binary by reading the first 1024 bytes"""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            return bool(chunk.translate(None, TEXTCHARS))
    except (PermissionError, FileNotFoundError, IsADirectoryError, OSError):
        return True  # Treat inaccessible files as binary

def update_file(filepath):
    """Update brand name in a single file"""
    if not os.path.isfile(filepath):
        return False
    
    # Check if file is binary
    if is_binary_file(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError, FileNotFoundError, IsADirectoryError):
        # Skip files we can't read
        return False
    
    if OLD_NAME not in content:
        return False
    
    # Replace the old brand name with the new one
    new_content = content.replace(OLD_NAME, NEW_NAME)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except (PermissionError, OSError) as e:
        # Skip files we can't write to
        print(f"Warning: Could not update {filepath}: {e}")
        return False
    
    print(f"Updated: {filepath}")
    return True

def find_and_update_in_directory(directory="."):
    """Recursively search for files containing the old brand name and update them"""
    updated_files = []
    
    # Recursively search through all files
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for filename in files:
            filepath = os.path.join(root, filename)
            if update_file(filepath):
                updated_files.append(filepath)
    
    return updated_files

if __name__ == "__main__":
    print(f"Searching for '{OLD_NAME}' and replacing with '{NEW_NAME}'...")
    updated = find_and_update_in_directory()
    
    if updated:
        print(f"\nUpdated {len(updated)} file(s):")
        for filepath in updated:
            print(f"  - {filepath}")
    else:
        print("No files found containing the old brand name.")
