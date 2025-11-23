# Agent Guide for njzjz-bot Tasks

This document provides guidance for agents (AI assistants) who need to create or modify tasks in this repository.

## Task Structure

Tasks are stored in the `tasks/` directory. Each task should have its own subdirectory with the following structure:

```
tasks/
└── task-name/
    ├── run.sh          # Main execution script (required)
    └── *.py            # Additional scripts (optional)
```

## Creating a New Task

To create a new task:

1. **Create a task directory** under `tasks/` with a descriptive name (e.g., `sphinx-book-theme`)

2. **Create a `run.sh` script** that:
   - Is executable (`chmod +x run.sh`)
   - Uses `multi-gitter` to run changes across multiple repositories
   - Includes proper author attribution:
     - `--author-email "48687836+njzjz-bot@users.noreply.github.com"`
     - `--author-name "njzjz-bot[bot]"`
   - Specifies target repositories with `-R` flag
   - Includes a descriptive commit message with `-m` flag
   - References the GitHub issue that generated the task

3. **Create supporting scripts** (e.g., Python scripts) that:
   - Perform the actual file modifications
   - Are called by the `run.sh` script
   - Handle missing files gracefully

4. **Update the workflow** by adding your task to `.github/workflows/run-tasks.yml`:
   - Add the task name to the `matrix.task` list

## Example Task

See `tasks/sphinx-book-theme/` for a complete example that:
- Replaces `sphinx-rtd-theme` with `sphinx-book-theme` in Python projects
- Updates multiple configuration and requirements files
- Uses regex patterns to handle different file formats

## multi-gitter Command Reference

The `multi-gitter` tool is used to apply changes across multiple repositories. Common flags:

- `run <script>` - Run a script in each repository
- `--author-email` - Git author email
- `--author-name` - Git author name
- `-B, --branch-name` - Name of the branch to create
- `--fork` - Create changes in a fork
- `-m, --commit-message` - Commit message
- `--git-type cmd` - Use command-line git
- `-R, --repo` - Target repository (can be repeated)
- `--conflict-strategy replace` - How to handle existing PRs
- `--dry-run` - Preview changes without making them (used in PRs)
- `--log-level=debug` - Verbose logging (used in PRs)

## Workflow Behavior

- **Pull Requests**: Tasks run with `--dry-run --log-level=debug` flags to preview changes
- **Main Branch**: After merging, tasks run with the `GITHUB_TOKEN` to create actual PRs

## Best Practices

1. **Test thoroughly**: Always test your task script locally before committing
2. **Handle errors gracefully**: Check if files exist before modifying them
3. **Use idempotent operations**: Scripts should be safe to run multiple times
4. **Document changes**: Include clear commit messages explaining what and why
5. **Reference issues**: Link back to the GitHub issue that requested the task
6. **Minimize scope**: Only modify files that need changes
7. **Follow conventions**: Use existing tasks as templates

## Requirements

Tasks may require additional Python packages. Common dependencies:
- `packaging` - For version parsing
- Standard library modules (`re`, `os`, etc.)

These should be installed in the GitHub Actions workflow.
