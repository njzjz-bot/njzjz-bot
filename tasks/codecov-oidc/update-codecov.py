#!/usr/bin/env python3
# /// script
# dependencies = [
#   "ruamel.yaml",
# ]
# ///
"""Update codecov-action to use OIDC instead of tokens"""

import os
from ruamel.yaml import YAML

def update_codecov_workflow(filepath):
    """Update a single workflow file to use OIDC for codecov-action"""
    if not os.path.isfile(filepath):
        return False
    
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096  # Prevent line wrapping
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            workflow = yaml.load(f)
    except Exception as e:
        print(f"Warning: Could not parse {filepath}: {e}")
        return False
    
    if not workflow or not isinstance(workflow, dict):
        return False
    
    modified = False
    
    # Check if workflow has jobs
    if 'jobs' not in workflow:
        return False
    
    jobs = workflow['jobs']
    if not isinstance(jobs, dict):
        return False
    
    # Track if we need to add id-token permission at any level
    needs_id_token_permission = False
    
    # Iterate through all jobs
    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue
        
        # Check if job has steps
        if 'steps' not in job_config:
            continue
        
        steps = job_config['steps']
        if not isinstance(steps, list):
            continue
        
        # Look for codecov-action usage in steps
        for step in steps:
            if not isinstance(step, dict):
                continue
            
            # Check if this step uses codecov-action
            if 'uses' not in step:
                continue
            
            uses = step['uses']
            if not isinstance(uses, str):
                continue
            
            # Check if it's codecov/codecov-action
            if not uses.startswith('codecov/codecov-action'):
                continue
            
            # This step uses codecov-action
            print(f"Found codecov-action in job '{job_name}' in {filepath}")
            
            # Ensure 'with' section exists
            if 'with' not in step:
                step['with'] = {}
            
            step_with = step['with']
            if not isinstance(step_with, dict):
                step['with'] = {}
                step_with = step['with']
            
            # Add use_oidc: true if not already present
            if 'use_oidc' not in step_with or step_with.get('use_oidc') is not True:
                step_with['use_oidc'] = True
                modified = True
                print(f"  Added use_oidc: true")
            
            # Remove token if present (it will be ignored anyway)
            if 'token' in step_with:
                del step_with['token']
                modified = True
                print(f"  Removed token parameter")
            
            # Mark that we need id-token permission
            needs_id_token_permission = True
    
    # If we modified any codecov-action steps, ensure id-token permission is set
    if needs_id_token_permission:
        # Check if there's already a workflow-level permissions section
        if 'permissions' not in workflow:
            workflow['permissions'] = {}
        
        permissions = workflow['permissions']
        if not isinstance(permissions, dict):
            workflow['permissions'] = {}
            permissions = workflow['permissions']
        
        # Add id-token: write if not present
        if 'id-token' not in permissions or permissions.get('id-token') != 'write':
            permissions['id-token'] = 'write'
            modified = True
            print(f"  Added id-token: write permission at workflow level")
    
    # If we made changes, write the file back
    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(workflow, f)
            print(f"Updated: {filepath}")
            return True
        except Exception as e:
            print(f"Warning: Could not write {filepath}: {e}")
            return False
    
    return False

def find_and_update_workflows(directory="."):
    """Find all GitHub Actions workflow files and update them"""
    workflows_dir = os.path.join(directory, ".github", "workflows")
    
    if not os.path.isdir(workflows_dir):
        print("No .github/workflows directory found")
        return []
    
    updated_files = []
    
    # Search for YAML files in .github/workflows
    for filename in os.listdir(workflows_dir):
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            filepath = os.path.join(workflows_dir, filename)
            if update_codecov_workflow(filepath):
                updated_files.append(filepath)
    
    return updated_files

if __name__ == "__main__":
    print("Searching for codecov-action usage in GitHub Actions workflows...")
    updated = find_and_update_workflows()
    
    if updated:
        print(f"\nUpdated {len(updated)} workflow file(s):")
        for filepath in updated:
            print(f"  - {filepath}")
    else:
        print("No workflow files found using codecov-action or no changes needed.")
