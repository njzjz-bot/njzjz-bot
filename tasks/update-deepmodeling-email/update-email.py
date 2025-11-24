#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""Update DeepModeling email from contact@deepmodeling.org to deepmodeling@deepmodeling.com"""

import os
import re

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

def update_file(filepath):
    """Update email in a single file"""
    if not os.path.isfile(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError):
        # Skip binary files or files we can't read
        return False
    
    if OLD_EMAIL not in content:
        return False
    
    new_content = content.replace(OLD_EMAIL, NEW_EMAIL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated: {filepath}")
    return True

def find_and_update_in_directory(directory="."):
    """Recursively search for files containing the old email and update them"""
    updated_files = []
    
    # First, check common file patterns
    for pattern in FILE_PATTERNS:
        filepath = os.path.join(directory, pattern)
        if update_file(filepath):
            updated_files.append(filepath)
    
    # Then, recursively search through all text files
    # (but skip common directories that shouldn't be modified)
    skip_dirs = {'.git', '__pycache__', 'node_modules', '.tox', '.eggs', 
                 'dist', 'build', '.pytest_cache', '.venv', 'venv'}
    
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for filename in files:
            # Only check text files (common extensions)
            if any(filename.endswith(ext) for ext in [
                '.md', '.rst', '.txt', '.py', '.cfg', '.toml', '.yaml', '.yml',
                '.json', '.sh', '.bash', '.html', '.xml', '.ini', '.conf'
            ]):
                filepath = os.path.join(root, filename)
                # Skip files we already updated
                if filepath not in updated_files:
                    if update_file(filepath):
                        updated_files.append(filepath)
    
    return updated_files

if __name__ == "__main__":
    print(f"Searching for '{OLD_EMAIL}' and replacing with '{NEW_EMAIL}'...")
    updated = find_and_update_in_directory()
    
    if updated:
        print(f"\nUpdated {len(updated)} file(s):")
        for filepath in updated:
            print(f"  - {filepath}")
    else:
        print("No files found containing the old email address.")
