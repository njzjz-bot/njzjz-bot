#!/usr/bin/env python3
# /// script
# dependencies = [
#   "tomli>=2.0.0; python_version < '3.11'",
#   "tomli-w",
# ]
# ///
"""Update ruff settings: move tool.ruff to tool.ruff.lint"""

import os
import sys

# For Python 3.11+, use tomllib from stdlib, otherwise use tomli
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import tomli_w


# Settings that should be moved from tool.ruff to tool.ruff.lint
LINT_SETTINGS = {
    'ignore',
    'ignore-init-module-imports',
    'select',
    'pydocstyle',
    'per-file-ignores',
    'extend-ignore',
    'extend-select',
    'flake8-annotations',
    'flake8-quotes',
    'isort',
    'mccabe',
    'pycodestyle',
    'pyupgrade',
    'pep8-naming',
}


def update_ruff_config(filepath):
    """Update ruff configuration in a pyproject.toml file"""
    if not os.path.isfile(filepath):
        return False
    
    try:
        with open(filepath, 'rb') as f:
            data = tomllib.load(f)
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error reading {filepath}: {e}")
        return False
    
    # Check if tool.ruff exists
    if 'tool' not in data or 'ruff' not in data['tool']:
        return False
    
    ruff_config = data['tool']['ruff']
    
    # Find settings that need to be moved
    settings_to_move = {}
    for setting in ruff_config.keys():
        if setting in LINT_SETTINGS:
            settings_to_move[setting] = ruff_config[setting]
    
    # If no settings to move, no changes needed
    if not settings_to_move:
        return False
    
    # Create or update tool.ruff.lint
    if 'lint' not in ruff_config:
        ruff_config['lint'] = {}
    
    # Move settings to lint section
    for setting, value in settings_to_move.items():
        # Only move if not already in lint section
        if setting not in ruff_config['lint']:
            ruff_config['lint'][setting] = value
            del ruff_config[setting]
            print(f"  Moved '{setting}' to 'lint.{setting}'")
        else:
            # If it exists in both places, remove from top level
            del ruff_config[setting]
            print(f"  Removed duplicate '{setting}' (keeping 'lint.{setting}')")
    
    # Write back the updated TOML
    try:
        with open(filepath, 'wb') as f:
            tomli_w.dump(data, f)
    except (OSError, PermissionError) as e:
        print(f"Error writing {filepath}: {e}")
        return False
    
    return True


def main():
    """Main function to update ruff settings in pyproject.toml"""
    filepath = "pyproject.toml"
    
    print(f"Checking {filepath}...")
    
    if update_ruff_config(filepath):
        print(f"Updated ruff configuration in {filepath}")
    else:
        print(f"No ruff configuration updates needed in {filepath}")


if __name__ == "__main__":
    main()
