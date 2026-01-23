#!/bin/bash
# This script uses multi-gitter to update codecov-action to use OIDC
# across all repositories in the deepmodeling organization and njzjz personal account.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run for deepmodeling organization
multi-gitter run "uv run $SCRIPT_DIR/update-codecov.py" \
  --author-email "48687836+njzjz-bot@users.noreply.github.com" \
  --author-name "njzjz-bot[bot]" \
  -B codecov-oidc \
  --fork \
  -m 'ci: use OIDC for codecov-action

Replace token-based authentication with OIDC (OpenID Connect) for codecov-action.
This is more secure and eliminates the need to manage upload tokens.

Changes:
- Add use_oidc: true to codecov-action configuration
- Add id-token: write permission at workflow level
- Remove token parameter from codecov-action (ignored when using OIDC)

This improves security and follows codecov-action best practices.
' \
  --git-type cmd \
  -O deepmodeling \
  --repo-exclude deepmodeling/sciencepedia \
  --conflict-strategy replace \
  "$@"

# Run for njzjz user
# Note: This processes all repositories under njzjz.
# The script will only create PRs for repos that actually use codecov-action.
multi-gitter run "uv run $SCRIPT_DIR/update-codecov.py" \
  --author-email "48687836+njzjz-bot@users.noreply.github.com" \
  --author-name "njzjz-bot[bot]" \
  -B codecov-oidc \
  --fork \
  -m 'ci: use OIDC for codecov-action

Replace token-based authentication with OIDC (OpenID Connect) for codecov-action.
This is more secure and eliminates the need to manage upload tokens.

Changes:
- Add use_oidc: true to codecov-action configuration
- Add id-token: write permission at workflow level
- Remove token parameter from codecov-action (ignored when using OIDC)

This improves security and follows codecov-action best practices.
' \
  --git-type cmd \
  -O njzjz \
  --conflict-strategy replace \
  "$@"
