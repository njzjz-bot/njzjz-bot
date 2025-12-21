#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""Update DeepModeling domain from deepmodeling.org to deepmodeling.com"""

import os

# Old and new domains
OLD_DOMAIN = "deepmodeling.org"
NEW_DOMAIN = "deepmodeling.com"

# Directories to skip during recursive search
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.tox', '.eggs', 
             'dist', 'build', '.pytest_cache', '.venv', 'venv'}

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
    
    # Replace all occurrences of the old domain with the new domain
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
    print(f"Searching for '{OLD_DOMAIN}' and replacing with '{NEW_DOMAIN}'...")
    updated = find_and_update_in_directory()
    
    if updated:
        print(f"\nUpdated {len(updated)} file(s):")
        for filepath in updated:
            print(f"  - {filepath}")
    else:
        print("No files found containing the old domain.")
