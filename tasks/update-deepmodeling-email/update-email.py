#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""Update DeepModeling email from contact@deepmodeling.org to deepmodeling@deepmodeling.com"""

import os

# Old and new email addresses
OLD_EMAIL = "contact@deepmodeling.org"
NEW_EMAIL = "deepmodeling@deepmodeling.com"

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
    
    # Python files
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    
    # Documentation directories
    "doc/conf.py",
    "docs/conf.py",
    "documentation/conf.py",
    
    # Other config files
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/SECURITY.md",
    ".github/CODE_OF_CONDUCT.md",
]

# Directories to skip during recursive search
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.tox', '.eggs', 
             'dist', 'build', '.pytest_cache', '.venv', 'venv'}

# File extensions to check during recursive search
TEXT_EXTENSIONS = [
    '.md', '.rst', '.txt', '.py', '.cfg', '.toml', '.yaml', '.yml',
    '.json', '.sh', '.bash', '.html', '.xml', '.ini', '.conf'
]

def update_file(filepath):
    """Update email in a single file"""
    if not os.path.isfile(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError, FileNotFoundError, IsADirectoryError):
        # Skip binary files, permission issues, or other file access errors
        return False
    
    if OLD_EMAIL not in content:
        return False
    
    new_content = content.replace(OLD_EMAIL, NEW_EMAIL)
    
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
    """Recursively search for files containing the old email and update them"""
    updated_files = set()  # Use set for O(1) membership checking to avoid duplicate processing
    
    # First, check common file patterns
    for pattern in FILE_PATTERNS:
        filepath = os.path.join(directory, pattern)
        if update_file(filepath):
            updated_files.add(filepath)
    
    # Then, recursively search through all text files
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for filename in files:
            # Only check text files (common extensions)
            if any(filename.endswith(ext) for ext in TEXT_EXTENSIONS):
                filepath = os.path.join(root, filename)
                # Skip files we already updated
                if filepath not in updated_files:
                    if update_file(filepath):
                        updated_files.add(filepath)
    
    return list(updated_files)  # Convert back to list for consistent return type

if __name__ == "__main__":
    print(f"Searching for '{OLD_EMAIL}' and replacing with '{NEW_EMAIL}'...")
    updated = find_and_update_in_directory()
    
    if updated:
        print(f"\nUpdated {len(updated)} file(s):")
        for filepath in updated:
            print(f"  - {filepath}")
    else:
        print("No files found containing the old email address.")
