# Tasks

This directory contains automated tasks that are run by the njzjz-bot across multiple repositories using [multi-gitter](https://github.com/lindell/multi-gitter).

## Structure

Each task is stored in its own subdirectory with the following files:

- `run.sh` - Shell script that executes the task using multi-gitter (required)
- Additional scripts (e.g., Python files) that perform the actual modifications (optional)

## Available Tasks

### sphinx-book-theme

Replaces `sphinx-rtd-theme` with the more modern `sphinx-book-theme` in Python documentation projects.

**Files:**
- `run.sh` - Executes the multi-gitter command
- `sphinx-book-theme.py` - Python script that updates configuration and requirements files

**Target repositories:** Configured in `run.sh`

## How It Works

1. **On Pull Requests:** Tasks run with `--dry-run --log-level=debug` flags to preview changes without making actual commits
2. **On Main Branch:** After merging, tasks run in production mode using the `GITHUB_TOKEN` to create PRs in target repositories

## Adding New Tasks

See [AGENTS.md](../AGENTS.md) for detailed instructions on creating new tasks.

Quick steps:
1. Create a new directory under `tasks/`
2. Add a `run.sh` script with the multi-gitter command
3. Add any supporting scripts
4. Update `.github/workflows/run-tasks.yml` to include your task in the matrix

## Requirements

- Python 3.x
- multi-gitter CLI tool
- Required Python packages: `packaging`
