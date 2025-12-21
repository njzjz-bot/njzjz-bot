#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""Update DeepModeling domain from deepmodeling.org to deepmodeling.com"""

import os
import re

# Old and new domains
OLD_DOMAIN = "deepmodeling.org"
NEW_DOMAIN = "deepmodeling.com"

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
    ".github/FUNDING.yml",
    
    # Citation files
    "CITATION.cff",
    "codemeta.json",
]

# Directories to skip during recursive search
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.tox', '.eggs', 
             'dist', 'build', '.pytest_cache', '.venv', 'venv', '.mypy_cache',
             '.ruff_cache', 'htmlcov', 'site', '_build'}

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
    """Update domain in a single file"""
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
    
    if OLD_DOMAIN not in content:
        return False
    
    # Replace the domain - use word boundary to avoid partial replacements
    # This handles URLs, email addresses, and plain text references
    new_content = content.replace(OLD_DOMAIN, NEW_DOMAIN)
    
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
    """Recursively search for files containing the old domain and update them"""
    updated_files = set()  # Use set for O(1) membership checking to avoid duplicate processing
    
    # First, check common file patterns
    for pattern in FILE_PATTERNS:
        filepath = os.path.join(directory, pattern)
        if update_file(filepath):
            updated_files.add(filepath)
    
    # Then, recursively search through all files
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for filename in files:
            filepath = os.path.join(root, filename)
            # Skip files we already updated
            if filepath not in updated_files:
                if update_file(filepath):
                    updated_files.add(filepath)
    
    return list(updated_files)  # Convert back to list for consistent return type

if __name__ == "__main__":
    print(f"Searching for '{OLD_DOMAIN}' and replacing with '{NEW_DOMAIN}'...")
    updated = find_and_update_in_directory()
    
    if updated:
        print(f"\nUpdated {len(updated)} file(s):")
        for filepath in updated:
            print(f"  - {filepath}")
    else:
        print("No files found containing the old domain.")
